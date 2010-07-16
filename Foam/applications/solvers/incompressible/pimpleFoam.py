#!/usr/bin/env python

#--------------------------------------------------------------------------------------
## VulaSHAKA (Simultaneous Neutronic, Fuel Performance, Heat And Kinetics Analysis)
## Copyright (C) 2009-2010 Pebble Bed Modular Reactor (Pty) Limited (PBMR)
## 
## This program is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
## 
## You should have received a copy of the GNU General Public License
## along with this program.  If not, see <http://www.gnu.org/licenses/>.
## 
## See https://vulashaka.svn.sourceforge.net/svnroot/vulashaka
##
## Author : Alexey PETROV
##


#---------------------------------------------------------------------------
def _createFields( runTime, mesh ):
    from Foam.OpenFOAM import ext_Info, nl
    from Foam.OpenFOAM import IOdictionary, IOobject, word, fileName
    from Foam.finiteVolume import volScalarField
    
    ext_Info() << "Reading field p\n" << nl
    p = volScalarField( IOobject( word( "p" ),
                                  fileName( runTime.timeName() ),
                                  mesh,
                                  IOobject.MUST_READ,
                                  IOobject.AUTO_WRITE ),
                        mesh )
    
    ext_Info() << "Reading field U\n" << nl
    from Foam.finiteVolume import volVectorField
    U = volVectorField( IOobject( word( "U" ),
                                  fileName( runTime.timeName() ),
                                  mesh,
                                  IOobject.MUST_READ,
                                  IOobject.AUTO_WRITE ),
                        mesh )
  
    from Foam.finiteVolume.cfdTools.incompressible import createPhi
    phi = createPhi( runTime, mesh, U )
    
    pRefCell = 0
    pRefValue = 0.0
    
    from Foam.finiteVolume import setRefCell
    pRefCell, pRefValue = setRefCell( p, mesh.solutionDict().subDict( word( "PIMPLE" ) ), pRefCell, pRefValue )
    
    from Foam.transportModels import singlePhaseTransportModel
    laminarTransport = singlePhaseTransportModel( U, phi )
    
    from Foam import incompressible
    turbulence = incompressible.turbulenceModel.New( U, phi, laminarTransport )

    return p, U, phi, turbulence, pRefCell, pRefValue, laminarTransport


#--------------------------------------------------------------------------------------
def Ueqn( mesh, phi, U, p, turbulence, oCorr, nOuterCorr, momentumPredictor ):
    from Foam import fvm, fvc
    UEqn = fvm.ddt(U) + fvm.div(phi, U) + turbulence.divDevReff(U)
    
    if ( oCorr == nOuterCorr - 1 ):
       UEqn.relax( 1.0 )
       pass
    else:
       UEqn.relax()
       pass
    
    rUA = 1.0/UEqn.A()
    
    from Foam.finiteVolume import solve
    if momentumPredictor:
       if ( oCorr == nOuterCorr - 1 ):
          from Foam.OpenFOAM import word
          solve( UEqn == -fvc.grad(p), mesh.solver( word( "UFinal" ) ) )
          pass
       else:
          solve( UEqn == -fvc.grad(p))
          pass
    else:
       U.ext_assign( rUA * ( UEqn.H() - fvc.grad( p ) ) )
       U.correctBoundaryConditions()
       pass
    
    return UEqn, rUA


#--------------------------------------------------------------------------------------
def pEqn( runTime, mesh, U, rUA, UEqn, phi, p, nCorr, nOuterCorr, nNonOrthCorr, oCorr, corr, pRefCell, pRefValue, cumulativeContErr ): 

    U.ext_assign( rUA * UEqn.H() )
    if ( nCorr <= 1 ):
       UEqn.clear()
       pass
       
    from Foam import fvc 
    phi.ext_assign( ( fvc.interpolate( U ) & mesh.Sf() ) + fvc.ddtPhiCorr( rUA, U, phi ) )
 
    from Foam.finiteVolume import adjustPhi
    adjustPhi( phi, U, p )

    # Non-orthogonal pressure corrector loop
    for nonOrth in range( nNonOrthCorr + 1):
        #Pressure corrector
        from Foam import fvm
        pEqn = fvm.laplacian( rUA, p ) == fvc.div( phi )
        pEqn.setReference( pRefCell, pRefValue )
        
        if ( oCorr == nOuterCorr-1 ) and ( corr == nCorr-1 ) and ( nonOrth == nNonOrthCorr ) :
           from Foam.OpenFOAM import word
           pEqn.solve( mesh.solver( word( "pFinal" ) ) )
           pass
        else:
           pEqn.solve()
           pass
           
        if ( nonOrth == nNonOrthCorr ) :
           phi.ext_assign( phi - pEqn.flux() )
           pass
        pass
    from Foam.finiteVolume.cfdTools.incompressible import continuityErrs
    cumulativeContErr = continuityErrs( mesh, phi, runTime, cumulativeContErr )
    
    # Explicitly relax pressure for momentum corrector except for last corrector
    if ( oCorr != nOuterCorr-1 ):
       p.relax()
       pass
       
    U.ext_assign(  U - rUA * fvc.grad( p ) )
    U.correctBoundaryConditions()

    return cumulativeContErr
    
#--------------------------------------------------------------------------------------
def main_standalone( argc, argv ):

    from Foam.OpenFOAM.include import setRootCase
    args = setRootCase( argc, argv )

    from Foam.OpenFOAM.include import createTime
    runTime = createTime( args )

    from Foam.OpenFOAM.include import createMesh
    mesh = createMesh( runTime )

    p, U, phi, turbulence, pRefCell, pRefValue, laminarTransport = _createFields( runTime, mesh )
    
    from Foam.finiteVolume.cfdTools.general.include import initContinuityErrs
    cumulativeContErr = initContinuityErrs()
    
    
    from Foam.OpenFOAM import ext_Info, nl
    ext_Info() << "\nStarting time loop\n" <<nl
    
    while runTime.run() :
        from Foam.finiteVolume.cfdTools.general.include import readTimeControls
        adjustTimeStep, maxCo, maxDeltaT = readTimeControls( runTime )

        from Foam.finiteVolume.cfdTools.general.include import readPIMPLEControls
        pimple, nOuterCorr, nCorr, nNonOrthCorr, momentumPredictor, transonic = readPIMPLEControls( mesh )

        from Foam.finiteVolume.cfdTools.general.include import CourantNo
        CoNum, meanCoNum = CourantNo( mesh, phi, runTime )
      
        from Foam.finiteVolume.cfdTools.general.include import setDeltaT
        runTime = setDeltaT( runTime, adjustTimeStep, maxCo, maxDeltaT, CoNum )
        
        runTime += runTime.deltaT()
                
        ext_Info() << "Time = " << runTime.timeName() << nl << nl
        
        # --- Pressure-velocity PIMPLE corrector loop
        for oCorr in range(nOuterCorr):
            if nOuterCorr != 1 :
               p.storePrevIter()
               pass
            
            UEqn, rUA = Ueqn( mesh, phi, U, p, turbulence, oCorr, nOuterCorr, momentumPredictor )
            
            # --- PISO loop
            for corr in range( nCorr ):
               cumulativeContErr = pEqn( runTime, mesh, U, rUA, UEqn, phi, p, nCorr, nOuterCorr,\
                                         nNonOrthCorr, oCorr, corr, pRefCell, pRefValue, cumulativeContErr )
               pass
                                         
            turbulence.correct()
            pass

        runTime.write();
        
        ext_Info() << "ExecutionTime = " << runTime.elapsedCpuTime() << " s" << \
              "  ClockTime = " << runTime.elapsedClockTime() << " s" << nl << nl
        
        pass

    ext_Info() << "End\n" << nl 

    import os
    return os.EX_OK


#--------------------------------------------------------------------------------------
import sys, os
from Foam import WM_PROJECT_VERSION
if WM_PROJECT_VERSION() < "1.6" :
   from Foam.OpenFOAM import ext_Info
   ext_Info() << "\n\n To use this solver it is necessary to SWIG OpenFOAM-1.6 or higher\n"
   pass


#--------------------------------------------------------------------------------------
if WM_PROJECT_VERSION() == "1.6" :
   if __name__ == "__main__" :
     argv = sys.argv
     os._exit( main_standalone( len( argv ), argv ) )
     pass
   else :
      argv = None
      test_dir= os.path.join( os.environ[ "PYFOAM_TESTING_DIR" ],'cases', 'r1.6', 'incompressible', 'pimpleFoam', 't-junction' )
      argv = [ __file__, "-case", test_dir ]
      os._exit( main_standalone( len( argv ), argv ) )
      pass

    
#--------------------------------------------------------------------------------------
if WM_PROJECT_VERSION() >= "1.7.0" :
   if __name__ == "__main__" :
     argv = sys.argv
     os._exit( main_standalone( len( argv ), argv ) )
     pass
   else :
      argv = None
      test_dir= os.path.join( os.environ[ "PYFOAM_TESTING_DIR" ],'cases', 'r1.7.0', 'incompressible', 'pimpleFoam', 't-junction' )
      argv = [ __file__, "-case", test_dir ]
      os._exit( main_standalone( len( argv ), argv ) )
      pass

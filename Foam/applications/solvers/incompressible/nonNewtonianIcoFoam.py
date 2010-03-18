#!/usr/bin/env python

#--------------------------------------------------------------------------------------
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
## See https://csrcs.pbmr.co.za/svn/nea/prototypes/reaktor/pyfoam
##
## Author : Alexey PETROV
##


#----------------------------------------------------------------------------
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
    
    from Foam.transportModels import singlePhaseTransportModel
    fluid = singlePhaseTransportModel( U, phi )
    
    pRefCell = 0
    pRefValue = 0.0
    
    from Foam.finiteVolume import setRefCell
    setRefCell( p, mesh.solutionDict().subDict( word( "PISO" ) ), pRefCell, pRefValue )

        
    return p, U, phi, fluid, pRefCell, pRefValue


#--------------------------------------------------------------------------------------
def main_standalone( argc, argv ):

    from Foam.OpenFOAM.include import setRootCase
    args = setRootCase( argc, argv )

    from Foam.OpenFOAM.include import createTime
    runTime = createTime( args )

    from Foam.OpenFOAM.include import createMeshNoClear
    mesh = createMeshNoClear( runTime )
    
    p, U, phi, fluid, pRefCell, pRefValue = _createFields( runTime, mesh )
    
    from Foam.finiteVolume.cfdTools.general.include import initContinuityErrs
    cumulativeContErr = initContinuityErrs()
    
    from Foam.OpenFOAM import ext_Info, nl
    ext_Info() << "\nStarting time loop\n" << nl 
    
    while runTime.loop() :
        ext_Info() << "\nTime = " << runTime.timeName() << nl << nl
        
        from Foam.finiteVolume.cfdTools.general.include import readPISOControls
        piso, nCorr, nNonOrthCorr, momentumPredictor, transonic, nOuterCorr = readPISOControls( mesh ) 
        
        from Foam.finiteVolume.cfdTools.incompressible import CourantNo
        CoNum, meanCoNum = CourantNo( mesh, phi, runTime )
        
        fluid.correct()
        from Foam import fvm, fvc
        
        UEqn = fvm.ddt( U ) + fvm.div( phi, U ) - fvm.laplacian( fluid.nu(), U )
        
        from Foam.finiteVolume import solve
        solve( UEqn == -fvc.grad( p ) )
        
        # --- PISO loop

        for corr in range( nCorr ):
            rUA = 1.0 / UEqn.A()
            U = rUA * UEqn.H()
            phi.ext_assign( ( fvc.interpolate( U ) & mesh.Sf() ) + fvc.ddtPhiCorr( rUA, U, phi ) )
            
            from Foam.finiteVolume import adjustPhi
            adjustPhi(phi, U, p)
            
            for nonOrth in range( nNonOrthCorr + 1): 
                
                pEqn = ( fvm.laplacian( rUA, p ) == fvc.div( phi ) )
                
                pEqn.setReference( pRefCell, pRefValue )
                pEqn.solve()

                if nonOrth == nNonOrthCorr:
                   phi.ext_assign( phi - pEqn.flux() )
                   pass
                
                from Foam.finiteVolume.cfdTools.incompressible import continuityErrs
                cumulativeContErr = continuityErrs( mesh, phi, runTime, cumulativeContErr )     
                
                U.ext_assign( U - rUA * fvc.grad( p ) )
                U.correctBoundaryConditions()
                pass

        runTime.write()
        
        ext_Info() << "ExecutionTime = " << runTime.elapsedCpuTime() << " s" << \
              "  ClockTime = " << runTime.elapsedClockTime() << " s" << nl << nl
        
        pass

    ext_Info() << "End\n" << nl 

    import os
    return os.EX_OK


#--------------------------------------------------------------------------------------
import sys, os
from Foam import WM_PROJECT_VERSION
if WM_PROJECT_VERSION() >= "1.6" :
   if __name__ == "__main__" :
     argv = sys.argv
     os._exit( main_standalone( len( argv ), argv ) )
     pass
   else :
      argv = None
      test_dir= os.path.join( os.environ[ "PYFOAM_TESTING_DIR" ],'cases', 'r1.6', 'incompressible', 'nonNewtonianIcoFoam', 'offsetCylinder' )
      argv = [ __file__, "-case", test_dir ]
      os._exit( main_standalone( len( argv ), argv ) )
      pass
else :
   from Foam.OpenFOAM import ext_Info
   ext_Info() << "\n\n To use this solver it is necessary to SWIG OpenFOAM-1.6\n"
   pass

    
#--------------------------------------------------------------------------------------


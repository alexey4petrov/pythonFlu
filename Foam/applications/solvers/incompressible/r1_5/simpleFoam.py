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
    pRefCell, pRefValue = setRefCell( p, mesh.solutionDict().subDict( word( "SIMPLE" ) ), pRefCell, pRefValue )
    
    from Foam.transportModels import singlePhaseTransportModel
    laminarTransport = singlePhaseTransportModel( U, phi )
    
    from Foam import incompressible
    turbulence = incompressible.RASModel.New( U, phi, laminarTransport )
           
    return p, U, phi, turbulence, pRefCell, pRefValue, laminarTransport


#--------------------------------------------------------------------------------------
def initConvergenceCheck( simple ):
    eqnResidual = 1
    maxResidual = 0
    convergenceCriterion = 0
    
    from Foam.OpenFOAM import word
    tmp, convergenceCriterion = simple.readIfPresent( word( "convergence" ), convergenceCriterion )
    
    return eqnResidual, maxResidual, convergenceCriterion


#--------------------------------------------------------------------------------------
def Ueqn( phi, U, p, turbulence, eqnResidual, maxResidual ):
    from Foam import fvm, fvc
    UEqn = fvm.div( phi, U ) + turbulence.divDevReff( U ) 

    UEqn.relax()
    
    from Foam.finiteVolume import solve
    eqnResidual = solve( UEqn == -fvc.grad(p) ).initialResidual()
    maxResidual = max(eqnResidual, maxResidual)
      
    return UEqn, eqnResidual, maxResidual


#--------------------------------------------------------------------------------------
def pEqn( runTime, mesh, p, phi, U, UEqn, eqnResidual, maxResidual, nNonOrthCorr, cumulativeContErr, pRefCell, pRefValue ): 
    
    p.ext_boundaryField().updateCoeffs()

    AU = UEqn.A()
    U.ext_assign( UEqn.H() / AU )
    UEqn.clear()
    
    from Foam import fvc 
    phi.ext_assign( fvc.interpolate( U ) & mesh.Sf() )
    
    from Foam.finiteVolume import adjustPhi
    adjustPhi( phi, U, p )
    
    # Non-orthogonal pressure corrector loop
    for nonOrth in range( nNonOrthCorr+1 ):
        
        from Foam import fvm, fvc
        pEqn = fvm.laplacian( 1.0 / AU, p ) == fvc.div( phi ) 
        pEqn.setReference( pRefCell, pRefValue )
        
        
        # retain the residual from the first iteration
        if ( nonOrth == 0 ):
           eqnResidual = pEqn.solve().initialResidual()
           maxResidual = max( eqnResidual, maxResidual )
           pass
        else:
           pEqn.solve()
           pass
        
        if ( nonOrth == nNonOrthCorr ):
           phi.ext_assign( phi - pEqn.flux() )
           pass
        
        pass

    from Foam.finiteVolume.cfdTools.incompressible import continuityErrs
    cumulativeContErr = continuityErrs( mesh, phi, runTime, cumulativeContErr )
    
    #Explicitly relax pressure for momentum corrector
    p.relax()

    #Momentum corrector
    U.ext_assign( U - fvc.grad( p ) / AU )
    U.correctBoundaryConditions()

    return eqnResidual, maxResidual, cumulativeContErr


#--------------------------------------------------------------------------------------
def convergenceCheck( maxResidual, convergenceCriterion ):
    from Foam.OpenFOAM import ext_Info, nl
    
    if (maxResidual < convergenceCriterion):
       ext_Info() << "reached convergence criterion: " << convergenceCriterion << nl
       runTime.writeAndEnd();
       ext_Info   << "latestTime = " << runTime.timeName() << nl
       pass

    
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
    
    runTime.increment()    
    
    while not runTime.end():
        ext_Info() << "Time = " << runTime.timeName() << nl << nl

        from Foam.finiteVolume.cfdTools.general.include import readSIMPLEControls
        simple, nNonOrthCorr, momentumPredictor, fluxGradp, transonic = readSIMPLEControls( mesh )
        
        eqnResidual, maxResidual, convergenceCriterion = initConvergenceCheck( simple )
                
        p.storePrevIter()
        
        UEqn, eqnResidual, maxResidual = Ueqn( phi, U, p, turbulence, eqnResidual, maxResidual )
        
        eqnResidual, maxResidual, cumulativeContErr = pEqn( runTime, mesh, p, phi, U, UEqn, \
                                                            eqnResidual, maxResidual, nNonOrthCorr, cumulativeContErr, pRefCell, pRefValue )
        
        turbulence.correct()

        runTime.write();
        
        ext_Info() << "ExecutionTime = " << runTime.elapsedCpuTime() << " s" << \
              "  ClockTime = " << runTime.elapsedClockTime() << " s" << nl << nl
        
        convergenceCheck( maxResidual, convergenceCriterion ) 
        
        runTime.increment()
        pass
        
    ext_Info() << "End\n" << nl 

    import os
    return os.EX_OK


#--------------------------------------------------------------------------------------
import os, sys
from Foam import FOAM_VERSION
if FOAM_VERSION( "==", "010500" ):
   if __name__ == "__main__" :
      argv = sys.argv
      if len( argv ) > 1 and argv[ 1 ] == "-test":
         argv = None
         test_dir= os.path.join( os.environ[ "PYFOAM_TESTING_DIR" ],'cases', 'local', 'r1.5', 'simpleFoam', 'pitzDaily' )
         argv = [ __file__, "-case", test_dir ]
         pass
      os._exit( main_standalone( len( argv ), argv ) )
else:
   from Foam.OpenFOAM import ext_Info
   ext_Info()<< "\nTo use this solver, It is necessary to SWIG OpenFoam1.5 \n "     
   

    
#--------------------------------------------------------------------------------------


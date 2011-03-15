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
def readTransportProperties( U, phi ):
    from Foam.transportModels import singlePhaseTransportModel
    laminarTransport = singlePhaseTransportModel( U, phi )
    
    from Foam.OpenFOAM import dimensionedScalar, word
    # Thermal expansion coefficient [1/K]
    beta = dimensionedScalar( laminarTransport.lookup( word( "beta" ) ) )

    # Reference temperature [K]
    TRef = dimensionedScalar( laminarTransport.lookup( word( "TRef" ) ) )

    # Laminar Prandtl number
    Pr = dimensionedScalar( laminarTransport.lookup( word( "Pr" ) ) )

    # Turbulent Prandtl number
    Prt = dimensionedScalar( laminarTransport.lookup( word( "Prt" ) ) )
    
    return laminarTransport, beta, TRef,Pr, Prt


#-------------------------------------------------------------------------
def _createFields( runTime, mesh, g ):
    from Foam.OpenFOAM import ext_Info, nl
    from Foam.OpenFOAM import IOdictionary, IOobject, word, fileName
    from Foam.finiteVolume import volScalarField
    
    ext_Info() << "Reading thermophysical properties\n" << nl 

    ext_Info() << "Reading field T\n" << nl 
    T = volScalarField( IOobject( word( "T" ),
                                  fileName( runTime.timeName() ),
                                  mesh,
                                  IOobject.MUST_READ,
                                  IOobject.AUTO_WRITE ),
                        mesh )

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
    
    laminarTransport, beta, TRef,Pr, Prt = readTransportProperties( U, phi )
    
    ext_Info() << "Creating turbulence model\n" << nl
    from Foam import incompressible
    turbulence = incompressible.turbulenceModel.New( U, phi, laminarTransport )
    
    pRefCell = 0
    pRefValue = 0.0
    
    from Foam.finiteVolume import setRefCell
    pRefCell, pRefValue = setRefCell( p, mesh.solutionDict().subDict( word( "PISO" ) ), pRefCell, pRefValue )

    # Kinematic density for buoyancy force
    rhok = volScalarField( IOobject( word( "rhok" ),
                                     fileName( runTime.timeName() ),
                                     mesh ),
                           1.0 - beta * ( T - TRef ) )
    
    return T, p, U, phi, laminarTransport, beta, TRef,Pr, Prt, turbulence, pRefCell, pRefValue, rhok


#--------------------------------------------------------------------------------------
def _Ueqn( U, phi, turbulence, p, rhok, g, mesh, momentumPredictor ):
    from Foam import fvm
    # Solve the momentum equation

    UEqn = fvm.ddt( U ) + fvm.div( phi, U ) + turbulence.divDevReff( U )

    UEqn.relax()

    from Foam.finiteVolume import solve
    from Foam import fvc
    if momentumPredictor:
       solve( UEqn == fvc.reconstruct( ( fvc.interpolate( rhok ) * ( g & mesh.Sf() ) - fvc.snGrad( p ) * mesh.magSf() ) ) )
       
    return UEqn


#--------------------------------------------------------------------------------------
def _TEqn( turbulence, T, phi, rhok, beta, TRef, Pr, Prt ):
    from Foam.OpenFOAM import word
    from Foam.finiteVolume import volScalarField
    kappaEff = volScalarField( word( "kappaEff" ),
                               turbulence.nu() / Pr + turbulence.ext_nut() / Prt )
    from Foam import fvc, fvm
    TEqn = fvm.ddt( T ) + fvm.div( phi, T ) - fvm.laplacian( kappaEff, T ) 

    TEqn.relax()

    TEqn.solve()

    rhok.ext_assign( 1.0 - beta * ( T - TRef ) )
    
    return TEqn, kappaEff
    

#--------------------------------------------------------------------------------------    
def _pEqn( runTime, mesh, U, UEqn, phi, p, rhok, g, corr, nCorr, nNonOrthCorr, cumulativeContErr ): 
    
    from Foam.finiteVolume import volScalarField, surfaceScalarField
    from Foam.OpenFOAM import word
    from Foam import fvc
    rUA = volScalarField( word( "rUA" ), 1.0 / UEqn.A() )

    rUAf = surfaceScalarField(word( "(1|A(U))" ), fvc.interpolate( rUA ) )

    U.ext_assign( rUA * UEqn.H() )
    
    phiU = ( fvc.interpolate( U ) & mesh.Sf() ) + fvc.ddtPhiCorr( rUA, U, phi )
    
    phi.ext_assign( phiU + rUAf * fvc.interpolate( rhok ) * ( g & mesh.Sf() ) )
    
    for nonOrth in range( nNonOrthCorr+1 ):
        
        from Foam import fvm
        pEqn = fvm.laplacian( rUAf, p ) == fvc.div( phi )

        if ( corr == nCorr-1 ) and (nonOrth == nNonOrthCorr):
           from Foam.OpenFOAM import word
           pEqn.solve(mesh.solver( word( str( p.name() ) + "Final" ) ) )
           pass
        else:
           pEqn.solve( mesh.solver( p.name() ) )
           pass

        if (nonOrth == nNonOrthCorr):
           phi.ext_assign( phi - pEqn.flux() )
           pass
        pass
    U.ext_assign( U + rUA * fvc.reconstruct( ( phi - phiU ) / rUAf ) )
    U.correctBoundaryConditions() 

    from Foam.finiteVolume.cfdTools.incompressible import continuityErrs
    cumulativeContErr = continuityErrs( mesh, phi, runTime, cumulativeContErr )
    
    return pEqn


   
#--------------------------------------------------------------------------------------
def main_standalone( argc, argv ):

    from Foam.OpenFOAM.include import setRootCase
    args = setRootCase( argc, argv )

    from Foam.OpenFOAM.include import createTime
    runTime = createTime( args )

    from Foam.OpenFOAM.include import createMesh
    mesh = createMesh( runTime )

    from Foam.finiteVolume.cfdTools.general.include import readGravitationalAcceleration
    g = readGravitationalAcceleration( runTime, mesh)
    
    T, p, U, phi, laminarTransport, beta, TRef,Pr, Prt, turbulence, pRefCell, pRefValue, rhok = _createFields( runTime, mesh, g )
    
    from Foam.finiteVolume.cfdTools.general.include import initContinuityErrs
    cumulativeContErr = initContinuityErrs()
    
    from Foam.finiteVolume.cfdTools.general.include import readTimeControls
    adjustTimeStep, maxCo, maxDeltaT = readTimeControls( runTime )
    
    from Foam.finiteVolume.cfdTools.general.include import CourantNo
    CoNum, meanCoNum, velMag = CourantNo( mesh, phi, runTime )
    
    from Foam.finiteVolume.cfdTools.general.include import setInitialDeltaT
    runTime = setInitialDeltaT( runTime, adjustTimeStep, maxCo, maxDeltaT, CoNum )

    from Foam.OpenFOAM import ext_Info, nl
    ext_Info() << "\nStarting time loop\n" <<nl
    
    while runTime.loop():
        ext_Info() << "Time = " << runTime.timeName() << nl << nl

        from Foam.finiteVolume.cfdTools.general.include import readTimeControls
        adjustTimeStep, maxCo, maxDeltaT = readTimeControls( runTime )
    
        from Foam.finiteVolume.cfdTools.general.include import readPISOControls
        piso, nCorr, nNonOrthCorr, momentumPredictor, transonic, nOuterCorr = readPISOControls( mesh )
        
        from Foam.finiteVolume.cfdTools.general.include import CourantNo
        CoNum, meanCoNum, velMag = CourantNo( mesh, phi, runTime )
        
        from Foam.finiteVolume.cfdTools.general.include import setDeltaT
        runTime = setDeltaT( runTime, adjustTimeStep, maxCo, maxDeltaT, CoNum )
        
        UEqn = _Ueqn( U, phi, turbulence, p, rhok, g, mesh, momentumPredictor )
        
        TEqn, kappaEff = _TEqn( turbulence, T, phi, rhok, beta, TRef, Pr, Prt )
        
        # --- PISO loop
        for corr in range( nCorr ):
            pEqn = _pEqn( runTime, mesh, U, UEqn, phi, p, rhok, g, corr, nCorr, nNonOrthCorr, cumulativeContErr )
            pass

        turbulence.correct()

        runTime.write()
        
        ext_Info() << "ExecutionTime = " << runTime.elapsedCpuTime() << " s" << \
              "  ClockTime = " << runTime.elapsedClockTime() << " s" << nl << nl
        
        pass
        
    ext_Info() << "End\n" << nl 

    import os
    return os.EX_OK


#--------------------------------------------------------------------------------------
from Foam import FOAM_BRANCH_VERSION
import sys, os
if FOAM_BRANCH_VERSION( "dev", ">=", "010600" ):
   if __name__ == "__main__" :
      argv = sys.argv
      if len( argv ) > 1 and argv[ 1 ] == "-test":
         argv = None
         test_dir= os.path.join( os.environ[ "PYFOAM_TESTING_DIR" ],'cases','propogated', 'r1.6-dev', 'heatTransfer', 'buoyantBoussinesqPisoFoam', 'hotRoom' )
         argv = [ __file__, "-case", test_dir ]
         pass
      os._exit( main_standalone( len( argv ), argv ) )
else:
   from Foam.OpenFOAM import ext_Info
   ext_Info()<< "\nTo use this solver, It is necessary to SWIG OpenFoam1.6 \n "

    
#--------------------------------------------------------------------------------------


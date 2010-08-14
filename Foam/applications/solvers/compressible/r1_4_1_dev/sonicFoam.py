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
def readThermodynamicProperties( runTime, mesh ):
    from Foam.OpenFOAM import ext_Info, nl
    ext_Info() << "Reading thermodynamicProperties\n" << nl
    
    from Foam.OpenFOAM import IOdictionary, IOobject, fileName, word
    thermodynamicProperties = IOdictionary( IOobject( word( "thermodynamicProperties" ),
                                                      fileName( runTime.constant() ),
                                                      mesh,
                                                      IOobject.MUST_READ,
                                                      IOobject.NO_WRITE ) )
    from Foam.OpenFOAM import dimensionedScalar
    R = dimensionedScalar( thermodynamicProperties.lookup( word( "R" ) ) )
    
    Cv = dimensionedScalar( thermodynamicProperties.lookup( word( "Cv" ) ) )
    
    return thermodynamicProperties, R, Cv


#---------------------------------------------------------------------------
def readingTransportProperties( runTime, mesh ):
    from Foam.OpenFOAM import ext_Info, nl
    ext_Info() << "Reading transportProperties\n" << nl
    
    from Foam.OpenFOAM import IOdictionary, IOobject, fileName, word
    transportProperties = IOdictionary( IOobject( word( "transportProperties" ),
                                                  fileName( runTime.constant() ),
                                                  mesh,
                                                  IOobject.MUST_READ,
                                                  IOobject.NO_WRITE ) )
    from Foam.OpenFOAM import dimensionedScalar
    mu = dimensionedScalar( transportProperties.lookup( word( "mu" ) ) )
    
    return transportProperties, mu

#---------------------------------------------------------------------------
def _createFields( runTime, mesh, R, Cv ):
    from Foam.OpenFOAM import ext_Info, nl
    ext_Info() << "Reading field p\n" << nl
    
    from Foam.finiteVolume import volScalarField
    from Foam.OpenFOAM import IOdictionary, IOobject, fileName, word
    p = volScalarField( IOobject( word( "p" ),
                                  fileName( runTime.timeName() ),
                                  mesh,
                                  IOobject.MUST_READ,
                                  IOobject.AUTO_WRITE ),
                        mesh )
    
    ext_Info() << "Reading field T\n" << nl
    T = volScalarField( IOobject( word( "T" ),
                                  fileName( runTime.timeName() ),
                                  mesh,
                                  IOobject.MUST_READ,
                                  IOobject.AUTO_WRITE ),
                        mesh )
    
    ext_Info() << "Calculating field e from T\n" << nl
    e = volScalarField( IOobject( word( "e" ),
                                  fileName( runTime.timeName() ),
                                  mesh,
                                  IOobject.NO_READ,
                                  IOobject.NO_WRITE ),
                        Cv * T,
                        T.ext_boundaryField().types() )
    
    ext_Info() << "Reading field U\n" << nl
    from Foam.finiteVolume import volVectorField
    U = volVectorField( IOobject( word( "U" ),
                                  fileName( runTime.timeName() ),
                                  mesh,
                                  IOobject.MUST_READ,
                                  IOobject.AUTO_WRITE ),
                        mesh )
    
    psi = volScalarField( IOobject( word( "psi" ),
                                    fileName( runTime.timeName() ),
                                    mesh,
                                    IOobject.NO_READ,
                                    IOobject.NO_WRITE ),
                          1.0 / ( R * T ) )
    psi.oldTime()
    
    rho = volScalarField( IOobject( word( "rho" ),
                                    fileName( runTime.timeName() ),
                                    mesh ),
                          psi * p )
    
    from Foam.finiteVolume.cfdTools.compressible import compressibleCreatePhi
    phi = compressibleCreatePhi( runTime, mesh, rho, U )

    return p, T, e, U, psi, rho, phi 


#--------------------------------------------------------------------------------------
def compressibleContinuityErrs( p, rho, phi, psi, cumulativeContErr ):
    
    from Foam.finiteVolume.cfdTools.compressible import rhoEqn
    rhoEqn( rho, phi )
    
    sumLocalContErr =  ( (rho - psi * p ).mag().sum() / rho.sum()).value()
    globalContErr = ( ( rho - psi * p ).sum() /rho.sum() ).value()
    cumulativeContErr += globalContErr

    from Foam.OpenFOAM import ext_Info, nl
    ext_Info() << "time step continuity errors : sum local = " << sumLocalContErr\
               << ", global = " << globalContErr \
               << ", cumulative = " << cumulativeContErr << nl

    return cumulativeContErr


#--------------------------------------------------------------------------------------
def main_standalone( argc, argv ):

    from Foam.OpenFOAM.include import setRootCase
    args = setRootCase( argc, argv )

    from Foam.OpenFOAM.include import createTime
    runTime = createTime( args )

    from Foam.OpenFOAM.include import createMesh
    mesh = createMesh( runTime )

    thermodynamicProperties, R, Cv = readThermodynamicProperties( runTime, mesh )
    
    transportProperties, mu = readingTransportProperties( runTime, mesh )
    
    p, T, e, U, psi, rho, phi = _createFields( runTime, mesh, R, Cv )
    
    from Foam.finiteVolume.cfdTools.general.include import initContinuityErrs
    cumulativeContErr = initContinuityErrs()

    from Foam.OpenFOAM import ext_Info, nl
    ext_Info() << "\nStarting time loop\n" << nl
    
    runTime += runTime.deltaT()
    while not runTime.end() :
        ext_Info() << "Time = " << runTime.timeName() << nl << nl

        from Foam.finiteVolume.cfdTools.general.include import readPISOControls
        piso, nCorr, nNonOrthCorr, momentumPredictor, transSonic, nOuterCorr = readPISOControls( mesh )

        from Foam.finiteVolume.cfdTools.compressible import compressibleCourantNo
        CoNum, meanCoNum = compressibleCourantNo( mesh, phi, rho, runTime )
        
        from Foam.finiteVolume.cfdTools.compressible import rhoEqn
        rhoEqn( rho, phi )
        
        from Foam import fvm
        UEqn = fvm.ddt( rho, U ) + fvm.div( phi, U ) - fvm.laplacian( mu, U )
        
        from Foam import fvc
        from Foam.finiteVolume import solve
        solve( UEqn == -fvc.grad( p ) )

        solve( fvm.ddt( rho, e ) + fvm.div( phi, e ) - fvm.laplacian( mu, e ) == \
               - p * fvc.div( phi / fvc.interpolate( rho ) ) + mu * fvc.grad( U ).symm().magSqr() )
        
        T.ext_assign( e / Cv )
        
        psi.ext_assign( 1.0 / ( R * T ) )
        
        # --- PISO loop
        for corr in range( nCorr ):
            rUA = 1.0/UEqn.A()
            U.ext_assign( rUA * UEqn.H() )
            
            
            from Foam.OpenFOAM import word
            phid = ( ( fvc.interpolate( rho * U ) & mesh.Sf() ) + fvc.ddtPhiCorr( rUA, rho, U, phi ) )  / fvc.interpolate( p )
            print "111111111111"
            for nonOrth in range( nNonOrthCorr + 1 ):
                pEqn = fvm.ddt( psi, p ) + fvm.div( phid, p, word( "div(phid,p)" ) ) - fvm.laplacian( rho * rUA, p ) 
                
                pEqn.solve()
                phi = pEqn.flux()
                pass
            
            cumulativeContErr = compressibleContinuityErrs( p, rho, phi, psi, cumulativeContErr )
            
            U.ext_assign( U - rUA * fvc.grad( p ) )
            U.correctBoundaryConditions()
            
            pass
            
        rho.ext_assign( psi * p )
        
        runTime.write()

        ext_Info() << "ExecutionTime = " << runTime.elapsedCpuTime() << " s" << \
              "  ClockTime = " << runTime.elapsedClockTime() << " s" << nl << nl
        
        runTime += runTime.deltaT()
        pass

    ext_Info() << "End\n"

    import os
    return os.EX_OK

#----------------------------------------------------------------------------------------------------------
import sys, os
from Foam import FOAM_VERSION
if FOAM_VERSION( "<=", "010401" ):
   if __name__ == "__main__" :
      argv = sys.argv
      if len(argv) > 1 and argv[ 1 ] == "-test":
         argv = None
         test_dir= os.path.join( os.environ[ "PYFOAM_TESTING_DIR" ],'cases', 'local', 'r1.4.1-dev', 'compressible', 'sonicFoam' )
         argv = [ __file__, test_dir, 'shockTube' ]
         pass
      os._exit( main_standalone( len( argv ), argv ) )
      pass
   pass   
else:
   from Foam.OpenFOAM import ext_Info
   ext_Info()<< "\nTo use this solver, It is necessary to SWIG OpenFoam1.4.1-dev\n "


    
#--------------------------------------------------------------------------------------


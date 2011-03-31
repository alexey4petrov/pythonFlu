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
    
    from Foam.OpenFOAM import IOdictionary, IOobject, word, fileName
    thermodynamicProperties = IOdictionary( IOobject( word( "thermodynamicProperties" ),
                                                      fileName( runTime.constant() ),
                                                      mesh,
                                                      IOobject.MUST_READ,
                                                      IOobject.NO_WRITE ) )
    
    from Foam.OpenFOAM import dimensionedScalar
    rho0 = dimensionedScalar( thermodynamicProperties.lookup( word( "rho0" ) ) )
    
    p0 = dimensionedScalar( thermodynamicProperties.lookup( word( "p0" ) ) )
    
    psi = dimensionedScalar( thermodynamicProperties.lookup( word( "psi" ) ) )

    # Density offset, i.e. the constant part of the density
    rhoO = dimensionedScalar( word( "rhoO" ), rho0 - psi*p0)

    return thermodynamicProperties, rho0, p0, psi, rhoO


#------------------------------------------------------------------------------------
def readTransportProperties( runTime, mesh ):
    from Foam.OpenFOAM import ext_Info, nl
    ext_Info() << "Reading transportProperties\n" << nl
    
    from Foam.OpenFOAM import IOdictionary, IOobject, word, fileName
    transportProperties = IOdictionary( IOobject( word( "transportProperties" ),
                                                      fileName( runTime.constant() ),
                                                      mesh,
                                                      IOobject.MUST_READ,
    
                                                      IOobject.NO_WRITE ) )
    from Foam.OpenFOAM import dimensionedScalar
    mu = dimensionedScalar( transportProperties.lookup( word( "mu" ) ) )
    
    return transportProperties, mu


#-----------------------------------------------------------------------------------
def _createFields( runTime, mesh, rhoO, psi ):
    from Foam.OpenFOAM import ext_Info, nl
    ext_Info() << "Reading field p\n" << nl
    
    from Foam.finiteVolume import volScalarField
    from Foam.OpenFOAM import IOdictionary, IOobject, word, fileName
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

    rho = volScalarField( IOobject( word( "rho" ),
                                    fileName( runTime.timeName() ),
                                    mesh,
                                    IOobject.NO_READ,
                                    IOobject.AUTO_WRITE ),
                          rhoO + psi * p )
    
    
    from Foam.finiteVolume.cfdTools.compressible import compressibleCreatePhi
    phi = compressibleCreatePhi( runTime, mesh, rho, U )
    

    return p, U, rho, phi


#--------------------------------------------------------------------------------------
def compressibleContinuityErrs( rho, phi, psi, rho0, p, p0, cumulativeContErr ):
    from Foam.finiteVolume.cfdTools.compressible import rhoEqn
    rhoEqn( rho, phi )
    
    sumLocalContErr = ( ( (rho - rho0 - psi * ( p - p0 ) ).mag() ).sum() / rho.sum() ).value()

    globalContErr = ( (rho - rho0 - psi*(p - p0)).sum() / rho.sum() ).value()

    cumulativeContErr += globalContErr
    
    from Foam.OpenFOAM import ext_Info, nl 
    ext_Info() << "time step continuity errors : sum local = " << sumLocalContErr \
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
    
    thermodynamicProperties, rho0, p0, psi, rhoO = readThermodynamicProperties( runTime, mesh )
    
    transportProperties, mu = readTransportProperties( runTime, mesh )

    p, U, rho, phi = _createFields( runTime, mesh, rhoO, psi )
    
    from Foam.finiteVolume.cfdTools.general.include import initContinuityErrs
    cumulativeContErr = initContinuityErrs()

    from Foam.OpenFOAM import ext_Info, nl
    ext_Info() << "\nStarting time loop\n" << nl
    
    while runTime.loop() :
        ext_Info() << "Time = " << runTime.timeName() << nl << nl
        
        from Foam.finiteVolume.cfdTools.general.include import readPISOControls
        piso, nCorr, nNonOrthCorr, momentumPredictor, transonic, nOuterCorr = readPISOControls( mesh )

        from Foam.finiteVolume.cfdTools.compressible import compressibleCourantNo
        CoNum, meanCoNum = compressibleCourantNo( mesh, phi, rho, runTime )
        
        from Foam.finiteVolume.cfdTools.compressible import rhoEqn
        rhoEqn( rho, phi )
        
        from Foam import fvm, fvc
        from Foam.finiteVolume import solve
        UEqn = fvm.ddt(rho, U) + fvm.div(phi, U) - fvm.laplacian(mu, U)

        solve( UEqn == -fvc.grad( p ) )
        
        for corr in range( nCorr ): 
            rUA = 1.0 / UEqn.A()
            U.ext_assign( rUA * UEqn.H() )
            
            from Foam.OpenFOAM import word
            from Foam.finiteVolume import surfaceScalarField

            phid = surfaceScalarField( word( "phid" ), 
                                       psi * ( ( fvc.interpolate( U ) & mesh.Sf() ) + fvc.ddtPhiCorr( rUA, rho, U, phi ) ) )
            
            phi.ext_assign( ( rhoO / psi ) * phid )

            pEqn = fvm.ddt( psi, p ) + fvc.div( phi ) + fvm.div( phid, p ) - fvm.laplacian( rho * rUA, p ) 
            
            pEqn.solve()

            phi.ext_assign( phi + pEqn.flux() )
            
            cumulativeContErr = compressibleContinuityErrs( rho, phi, psi, rho0, p, p0, cumulativeContErr )
            
            U.ext_assign( U - rUA * fvc.grad( p ) )
            U.correctBoundaryConditions()
            pass
        rho.ext_assign( rhoO + psi*p )
        
        runTime.write()

        ext_Info() << "ExecutionTime = " << runTime.elapsedCpuTime() << " s" << \
              "  ClockTime = " << runTime.elapsedClockTime() << " s" << nl << nl
        
        pass

    ext_Info() << "End\n"

    import os
    return os.EX_OK


#--------------------------------------------------------------------------------------
import sys, os
from Foam import FOAM_REF_VERSION, FOAM_VERSION
if FOAM_VERSION( "<", "010600" ):
   from Foam.OpenFOAM import ext_Info
   ext_Info() << "\n\n To use this solver it is necessary to SWIG OpenFOAM-1.6 or higher\n"
   pass


#--------------------------------------------------------------------------------------
if FOAM_REF_VERSION( "==", "010600" ):
   if __name__ == "__main__" :
      argv = sys.argv
      if len(argv) > 1 and argv[ 1 ] == "-test":
         argv = None
         test_dir= os.path.join( os.environ[ "PYFOAM_TESTING_DIR" ],'cases', 'propogated', 'r1.6', 'compressible', 'sonicLiquidFoam', 'decompressionTank' )
         argv = [ __file__, "-case", test_dir ]
         pass
      os._exit( main_standalone( len( argv ), argv ) )
      pass
   pass   

    
#--------------------------------------------------------------------------------------
if FOAM_REF_VERSION( ">=", "010700" ):
   if __name__ == "__main__" :
      argv = sys.argv
      if len(argv) > 1 and argv[ 1 ] == "-test":
         argv = None
         test_dir= os.path.join( os.environ[ "PYFOAM_TESTING_DIR" ],'cases', 'propogated', 'r1.6', 'compressible', 'sonicLiquidFoam', 'decompressionTank' )
         argv = [ __file__, "-case", test_dir ]
         pass
      os._exit( main_standalone( len( argv ), argv ) )
      pass
   pass   

    
#--------------------------------------------------------------------------------------


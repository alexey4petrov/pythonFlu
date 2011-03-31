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
    R = dimensionedScalar( thermodynamicProperties.lookup( word( "R" ) ) )

    Cv = dimensionedScalar( thermodynamicProperties.lookup( word( "Cv" ) ) )
    
    return thermodynamicProperties, R, Cv


#---------------------------------------------------------------------------
def _createFields( runTime, mesh, R, Cv ):
    from Foam.OpenFOAM import ext_Info, nl
    ext_Info() << "Reading field p\n" << nl
    from Foam.OpenFOAM import IOdictionary, IOobject, word, fileName
    from Foam.finiteVolume import volScalarField    
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
                          psi * p,
                          p.ext_boundaryField().types() )
    
    rhoU = volVectorField( IOobject( word( "rhoU" ),
                                     fileName( runTime.timeName() ) , 
                                     mesh,
                                     IOobject.NO_READ,
                                     IOobject.NO_WRITE ),
                           rho * U,
                           U.ext_boundaryField().types() )

    rhoE = volScalarField( IOobject( word( "rhoE" ),
                                     fileName( runTime.timeName() ),
                                     mesh,
                                     IOobject.NO_READ,
                                     IOobject.NO_WRITE ),
                           rho * Cv * T + 0.5 * rho * ( rhoU / rho ).magSqr(),
                           T.ext_boundaryField().types() )
    
    return p, T, U, psi, rho, rhoU, rhoE


#--------------------------------------------------------------------------------------
def main_standalone( argc, argv ):

    from Foam.OpenFOAM.include import setRootCase
    args = setRootCase( argc, argv )

    from Foam.OpenFOAM.include import createTime
    runTime = createTime( args )

    from Foam.OpenFOAM.include import createMesh
    mesh = createMesh( runTime )
    
    thermodynamicProperties, R, Cv = readThermodynamicProperties( runTime, mesh )

    p, T, U, psi, rho, rhoU, rhoE = _createFields( runTime, mesh, R, Cv )
    
    from Foam.OpenFOAM import ext_Info, nl
    ext_Info() << "\nStarting time loop\n" << nl
    
    while runTime.loop() :
        ext_Info() << "Time = " << runTime.timeName() << nl << nl
        
        from Foam.finiteVolume import surfaceScalarField
        from Foam.OpenFOAM import IOobject, word, fileName
        from Foam import fvc
        phiv = surfaceScalarField( IOobject( word( "phiv" ),
                                             fileName( runTime.timeName() ),
                                             mesh,
                                             IOobject.NO_READ,
                                             IOobject.NO_WRITE ),
                                   fvc.interpolate( rhoU ) / fvc.interpolate( rho ) & mesh.Sf() )
        
        CoNum = ( mesh.deltaCoeffs() * phiv.mag() / mesh.magSf() ).ext_max().value()*runTime.deltaT().value();
        ext_Info() << "\nMax Courant Number = " << CoNum << nl
        
        from Foam import fvm
        
        from Foam.finiteVolume import solve
        solve( fvm.ddt(rho) + fvm.div( phiv, rho ) )
        
        p.ext_assign( rho / psi )
        
        solve( fvm.ddt( rhoU ) + fvm.div( phiv, rhoU ) == - fvc.grad( p ) )

        U == rhoU / rho
        
        phiv2 = surfaceScalarField( IOobject( word( "phiv2" ),
                                              fileName( runTime.timeName() ),
                                              mesh,
                                              IOobject.NO_READ,
                                              IOobject.NO_WRITE ),
                                    fvc.interpolate( rhoU ) / fvc.interpolate( rho ) & mesh.Sf() )
        
        solve( fvm.ddt( rhoE ) + fvm.div( phiv, rhoE ) == - fvc.div( phiv2, p ) )
        
        T.ext_assign( ( rhoE - 0.5 * rho * ( rhoU / rho ).magSqr() ) / Cv / rho )
        
        psi.ext_assign( 1.0 / ( R * T ) )
        
        runTime.write()

        ext_Info() << "ExecutionTime = " << runTime.elapsedCpuTime() << " s" << \
              "  ClockTime = " << runTime.elapsedClockTime() << " s" << nl << nl
        
        pass

    ext_Info() << "End\n"

    import os
    return os.EX_OK


#--------------------------------------------------------------------------------------
import sys, os
from Foam import FOAM_REF_VERSION, FOAM_BRANCH_VERSION
if FOAM_REF_VERSION( "<", "010600" ) or FOAM_REF_VERSION( ">", "010700" ):
   from Foam.OpenFOAM import ext_Info
   ext_Info() << "\n\n To use this solver it is necessary to SWIG OpenFOAM-1.6 or 1.7.0\n"
   pass


#--------------------------------------------------------------------------------------
if FOAM_REF_VERSION( "==", "010600" ) or FOAM_REF_VERSION( "==", "010700" ) or FOAM_BRANCH_VERSION( "dev", ">=", "010600" ):
   if __name__ == "__main__" :
      argv = sys.argv
      if len(argv) > 1 and argv[ 1 ] == "-test":
         argv = None
         test_dir= os.path.join( os.environ[ "PYFOAM_TESTING_DIR" ],'cases', 'local', 'r1.6', 'compressible', 'rhoSonicFoam', 'forwardStep' )
         argv = [ __file__, "-case", test_dir ]
         pass
      os._exit( main_standalone( len( argv ), argv ) )
      pass
   pass   

    
#--------------------------------------------------------------------------------------

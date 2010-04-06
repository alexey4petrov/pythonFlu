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
## See https://vulashaka.svn.sourceforge.net/svnroot/vulashaka/pyfoam
##
## Author : Alexey PETROV
##


#---------------------------------------------------------------------------
from Foam.applications.solvers.compressible.rhoCentralFoam.BCs import rho

#---------------------------------------------------------------------------
def _rhoBoundaryTypes( p ):
    pbf = p.ext_boundaryField()
    rhoBoundaryTypes = pbf.types()
    
    for patchi in range( rhoBoundaryTypes.size() ):
        if rhoBoundaryTypes[patchi] == "waveTransmissive":
           from Foam.finiteVolume import zeroGradientFvPatchScalarField
           rhoBoundaryTypes[patchi] = zeroGradientFvPatchScalarField.typeName
           pass
        elif pbf[patchi].fixesValue():
           from Foam.applications.solvers.compressible.rhoCentralFoam.BCs.rho import fixedRhoFvPatchScalarField
           rhoBoundaryTypes[patchi] = fixedRhoFvPatchScalarField.typeName
           pass
        pass
    
    return pbf, rhoBoundaryTypes


#-------------------------------------------------------------------------------------
def readThermophysicalProperties( runTime, mesh ):
    from Foam.OpenFOAM import ext_Info, nl
    ext_Info() << "Reading thermophysicalProperties\n" << nl
    
    from Foam.OpenFOAM import IOdictionary, IOobject, word, fileName
    # Pr defined as a separate constant to enable calculation of k, currently
    # inaccessible through thermo
    thermophysicalProperties = IOdictionary( IOobject( word( "thermophysicalProperties" ),
                                                       fileName( runTime.constant() ),
                                                       mesh,
                                                       IOobject.MUST_READ,
                                                       IOobject.NO_WRITE ) )
    
    from Foam.OpenFOAM import dimensionedScalar, dimless
    Pr = dimensionedScalar(word( "Pr" ), dimless, 1.0)
    
    if thermophysicalProperties.found( word( "Pr" ) ):
       Pr = thermophysicalProperties.lookup( word( "Pr" ) )
       pass
    return thermophysicalProperties, Pr


#---------------------------------------------------------------------------
def _createFields( runTime, mesh ):
    from Foam.OpenFOAM import ext_Info, nl
    ext_Info() << "Reading thermophysical properties\n" << nl
    
    from Foam.thermophysicalModels import basicPsiThermo
    thermo = basicPsiThermo.New( mesh )
    
    p = thermo.p()
    e = thermo.e()
    T = thermo.T()
    psi = thermo.psi()
    mu = thermo.mu()
    
    inviscid = True
    if mu.internalField().max() > 0.0:
       inviscid = False
       pass
    
    ext_Info() << "Reading field U\n" << nl
    from Foam.OpenFOAM import IOdictionary, IOobject, word, fileName
    from Foam.finiteVolume import volVectorField
    U = volVectorField( IOobject( word( "U" ),
                                  fileName( runTime.timeName() ),
                                  mesh,
                                  IOobject.MUST_READ,
                                  IOobject.AUTO_WRITE ),
                        mesh )
    
    pbf, rhoBoundaryTypes = _rhoBoundaryTypes( p )
    
    from Foam.finiteVolume import volScalarField
    rho = volScalarField( IOobject( word( "rho" ),
                                    fileName( runTime.timeName() ),
                                    mesh,
                                    IOobject.NO_READ,
                                    IOobject.AUTO_WRITE ),
                          thermo.rho(),
                          rhoBoundaryTypes )
    rhoU = volVectorField( IOobject( word( "rhoU" ),
                                     fileName( runTime.timeName() ),
                                     mesh,
                                     IOobject.NO_READ,
                                     IOobject.NO_WRITE ),
                           rho*U )
    rhoE = volScalarField( IOobject( word( "rhoE" ),
                                     fileName( runTime.timeName() ),
                                     mesh,
                                     IOobject.NO_READ,
                                     IOobject.NO_WRITE ),
                           rho * ( e + 0.5 * U.magSqr() ) )
    
    from Foam.OpenFOAM import dimensionedScalar, dimless
    from Foam.finiteVolume import surfaceScalarField
    pos = surfaceScalarField( IOobject( word( "pos" ),
                                        fileName( runTime.timeName() ),
                                        mesh ),
                              mesh,
                              dimensionedScalar( word( "pos" ), dimless, 1.0) )
    
    neg = surfaceScalarField( IOobject( word( "neg" ),
                                        fileName( runTime.timeName() ),
                                        mesh ),
                              mesh,
                              dimensionedScalar( word( "neg" ), dimless, -1.0 ) )
    
    return thermo, p, e, T, psi, mu, U, pbf, rhoBoundaryTypes, rho, rhoU, rhoE, pos, neg


#--------------------------------------------------------------------------------------
def main_standalone( argc, argv ):

    from Foam.OpenFOAM.include import setRootCase
    args = setRootCase( argc, argv )

    from Foam.OpenFOAM.include import createTime
    runTime = createTime( args )

    from Foam.OpenFOAM.include import createMesh
    mesh = createMesh( runTime )
    
    thermo, p, e, T, psi, mu, U, pbf, rhoBoundaryTypes, rho, rhoU, rhoE, pos, neg = _createFields( runTime, mesh )
    
    thermophysicalProperties, Pr = readThermophysicalProperties( runTime, mesh )
    
        
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
from Foam import WM_PROJECT_VERSION
if WM_PROJECT_VERSION() >= "1.6":
   if __name__ == "__main__" :
      argv = sys.argv
      if len(argv) > 1 and argv[ 1 ] == "-test":
         argv = None
         test_dir= os.path.join( os.environ[ "PYFOAM_TESTING_DIR" ],'cases', 'r1.6', 'compressible', 'rhoPisoFoam', 'ras', 'cavity' )
         argv = [ __file__, "-case", test_dir ]
         pass
      os._exit( main_standalone( len( argv ), argv ) )
      pass
   pass   
else:
   from Foam.OpenFOAM import ext_Info
   ext_Info()<< "\nTo use this solver, It is necessary to SWIG OpenFoam1.6 or higher\n "


    
#--------------------------------------------------------------------------------------


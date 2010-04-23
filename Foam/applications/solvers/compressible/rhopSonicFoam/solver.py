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
from Foam.applications.solvers.compressible.rhopSonicFoam.BCs import rho
from Foam.applications.solvers.compressible.rhopSonicFoam.BCs import rhoE

#---------------------------------------------------------------------------
def _rhoBoundaryTypes( p ):
    pbf = p.ext_boundaryField()
    rhoBoundaryTypes = pbf.types()
    
    for patchi in range( rhoBoundaryTypes.size() ):
        if str( rhoBoundaryTypes[patchi] ) == "pressureTransmissive":
           from Foam.finiteVolume import zeroGradientFvPatchScalarField
           rhoBoundaryTypes[patchi] = zeroGradientFvPatchScalarField.typeName
           pass
        elif pbf[patchi].fixesValue():
           from Foam.applications.solvers.compressible.rhoCentralFoam.BCs.rho import fixedRhoFvPatchScalarField
           rhoBoundaryTypes[patchi] = fixedRhoFvPatchScalarField.typeName
           pass
        else:
           from Foam.applications.solvers.compressible.rhopSonicFoam.BCs.rho import gradientRhoFvPatchScalarField
           rhoBoundaryTypes[patchi] = gradientRhoFvPatchScalarField.typeName
        pass
          
    return pbf, rhoBoundaryTypes


#---------------------------------------------------------------------------
def _rhoUboundaryTypes( U ):
    Ubf = U.ext_boundaryField();
    rhoUboundaryTypes = Ubf.types()
    for patchi in range( rhoUboundaryTypes.size() ):
        if Ubf[patchi].fixesValue():
           from Foam.applications.solvers.compressible.rhopSonicFoam.BCs.rhoU import fixedRhoUFvPatchVectorField
           # fixedRhoUFvPatchVectorField not implemented yet
           rhoUboundaryTypes[ patchi ] = fixedRhoUFvPatchVectorField.typeName
           pass
        pass
          
    return Ubf, rhoUboundaryTypes
#---------------------------------------------------------------------------
def _rhoEboundaryTypes( T ):
    Tbf = T.ext_boundaryField();
    rhoEboundaryTypes = Tbf.types()
    
    for patchi in range( rhoEboundaryTypes.size() ):
        if Tbf[patchi].fixesValue():
           rhoEboundaryTypes[ patchi ] = fixedRhoEFvPatchScalarField.typeName
           pass
        else:
           from Foam.applications.solvers.compressible.rhopSonicFoam.BCs.rhoE import mixedRhoEFvPatchScalarField
           rhoEboundaryTypes[ patchi ] = mixedRhoEFvPatchScalarField.typeName
           pass
        pass
          
    return Tbf, rhoEboundaryTypes



#-------------------------------------------------------------------------------------
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

    Cp = Cv + R

    gamma = Cp / Cv
    
    from Foam.OpenFOAM import dimless
    Pr = dimensionedScalar( word( "Pr" ), dimless, 1.0 )
    if thermodynamicProperties.found( word( "Pr" ) ) :
       Pr = dimensionedScalar( thermodynamicProperties.lookup( "Pr" ) )
       pass

    return thermodynamicProperties, R, Cv, Cp, gamma, Pr


#---------------------------------------------------------------------------
def compressibleCreatePhi( runTime, mesh, rhoU ):
    from Foam.OpenFOAM import IOobject, word, fileName
    phiHeader = IOobject( word( "phi" ),
                          fileName( runTime.timeName() ),
                          mesh,
                          IOobject.NO_READ )
    
    from Foam.OpenFOAM import ext_Info, nl
    if phiHeader.headerOk():
       ext_Info() << "Reading face flux field phi\n" << nl
       from Foam.finiteVolume import surfaceScalarField
       phi = surfaceScalarField( IOobject( word( "phi" ),
                                           fileName( runTime.timeName() ),
                                           mesh,
                                           IOobject.MUST_READ,
                                           IOobject.AUTO_WRITE ),
                                 mesh )
       pass
    else:
       ext_Info() << "Calculating face flux field phi\n" << nl
       
       from Foam.OpenFOAM import wordList
       #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
       # phiTypes =wordList( rhoU.ext_boundaryField().size(), calculatedFvPatchScalarField.typeName )
       phiTypes = wordList( 2, word( "calculated" ) )
       
       from Foam.finiteVolume import surfaceScalarField, linearInterpolate
       phi = surfaceScalarField( IOobject( word( "phi" ),
                                           fileName( runTime.timeName() ),
                                           mesh,
                                           IOobject.NO_READ,
                                           IOobject.AUTO_WRITE ),
                                 linearInterpolate( rhoU ) & mesh.Sf(),
                                 phiTypes )
       print "2222"
       pass
       
    
    return phiHeader, phi
    


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
    p.oldTime()

    ext_Info() << "Reading field T\n" << nl
    T = volScalarField( IOobject( word( "T" ),
                                  fileName( runTime.timeName() ),
                                  mesh,
                                  IOobject.MUST_READ,
                                  IOobject.AUTO_WRITE ),
                        mesh )
    T.correctBoundaryConditions()

    psi = volScalarField( IOobject( word( "psi" ),
                                    fileName( runTime.timeName() ),
                                    mesh,
                                    IOobject.NO_READ,
                                    IOobject.AUTO_WRITE ),
                          1.0 / ( R * T ) )
    psi.oldTime()

    pbf, rhoBoundaryTypes = _rhoBoundaryTypes( p )

    rho = volScalarField( IOobject( word( "rho" ),
                                    fileName( runTime.timeName() ),
                                    mesh,
                                    IOobject.NO_READ,
                                    IOobject.AUTO_WRITE ),
                          p * psi,
                          rhoBoundaryTypes )
    print "rho.ext_boundaryField().types() = ", rho.ext_boundaryField().types()
    ext_Info() << "Reading field U\n" << nl
    from Foam.finiteVolume import volVectorField
    U = volVectorField( IOobject( word( "U" ),
                                  fileName( runTime.timeName() ),
                                  mesh,
                                  IOobject.MUST_READ,
                                  IOobject.AUTO_WRITE ),
                        mesh )
    
    Ubf, rhoUboundaryTypes = _rhoUboundaryTypes( U )
    print " rhoUboundaryTypes =  ", rhoUboundaryTypes
    rhoU = volVectorField( IOobject( word( "rhoU" ),
                                     fileName( runTime.timeName() ),
                                     mesh,
                                     IOobject.NO_READ,
                                     IOobject.AUTO_WRITE ),
                           rho * U,
                           rhoUboundaryTypes )
    print "rhoU.ext_boundaryField().types() = ", rhoU.ext_boundaryField().size()
                           
    Tbf, rhoEboundaryTypes = _rhoEboundaryTypes( T )
    
    rhoE = volScalarField( IOobject( word( "rhoE" ),
                                     fileName( runTime.timeName() ),
                                     mesh,
                                     IOobject.NO_READ,
                                     IOobject.AUTO_WRITE ),
                           rho * Cv * T + 0.5 * rho * ( rhoU / rho ).magSqr(),
                           rhoEboundaryTypes )
    
    
    phiHeader, phi = compressibleCreatePhi( runTime, mesh, rhoU )
    
    phi.oldTime()
    
    from Foam.finiteVolume import surfaceScalarField, linearInterpolate
    phiv = surfaceScalarField( IOobject( word( "phiv" ),
                                         fileName( runTime.timeName() ),
                                         mesh ),
                               phi / linearInterpolate( rho ),
                               phi.ext_boundaryField().types() )
    
    rhoU.correctBoundaryConditions()
    
    from Foam.finiteVolume import TfieldTable_scalar
    fields = TfieldTable_scalar()
    
    magRhoU = rhoU.mag()
    H = volScalarField( word( "H" ) , ( rhoE + p ) / rho )

    fields.add( rho )
    fields.add( magRhoU )
    fields.add( H )
    
    return p, T, psi, pbf, rhoBoundaryTypes, rho, U, Ubf, rhoUboundaryTypes, rhoU, Tbf, rhoEboundaryTypes, rhoE, phi, phiv, rhoU, fields, magRhoU, H 


#--------------------------------------------------------------------------------------
def readFluxScheme( mesh ):
    from Foam.OpenFOAM import word
    fluxScheme = word("Kurganov")
    if mesh.schemesDict().found( word( "fluxScheme" ) ):
       fluxScheme = word( mesh.schemesDict().lookup( word( "fluxScheme" ) ) )
       from Foam.OpenFOAM import ext_Info, nl
       if str( fluxScheme ) == "Tadmor" or str( fluxScheme ) == "Kurganov":
          ext_Info() << "fluxScheme: " << fluxScheme << nl
          pass
       else:
          ext_Info() << "rhoCentralFoam::readFluxScheme" \
                     << "fluxScheme: " << fluxScheme \
                     << " is not a valid choice. " \
                     << "Options are: Tadmor, Kurganov" <<nl
          import os
          os.abort()           
          pass
       pass
    return fluxScheme

#--------------------------------------------------------------------------------------
def compressibleCourantNo( mesh, amaxSf, runTime ):
    CoNum = 0.0
    meanCoNum = 0.0
    
    if mesh.nInternalFaces():
       amaxSfbyDelta = mesh.deltaCoeffs() * amaxSf 
       CoNum = ( amaxSfbyDelta / mesh.magSf() ).ext_max().value() * runTime.deltaT().value()
       meanCoNum = ( amaxSfbyDelta.sum() / mesh.magSf().sum() ).value() * runTime.deltaT().value()
       pass
    from Foam.OpenFOAM import ext_Info, nl
    ext_Info() << "Mean and max Courant Numbers = " << meanCoNum << " " << CoNum << nl
    
    return CoNum, meanCoNum


#--------------------------------------------------------------------------------------
def main_standalone( argc, argv ):

    from Foam.OpenFOAM.include import setRootCase
    args = setRootCase( argc, argv )

    from Foam.OpenFOAM.include import createTime
    runTime = createTime( args )

    from Foam.OpenFOAM.include import createMesh
    mesh = createMesh( runTime )
    
    thermodynamicProperties, R, Cv, Cp, gamma, Pr = readThermodynamicProperties( runTime, mesh )
    
    p, T, psi, pbf, rhoBoundaryTypes, rho, U, Ubf, rhoUboundaryTypes, \
    rhoU, Tbf, rhoEboundaryTypes, rhoE, phi, phiv, rhoU, fields, magRhoU, H = _createFields( runTime, mesh, R, Cv )
    
    from Foam.OpenFOAM import ext_Info, nl
    ext_Info() << "\nStarting time loop\n" << nl
    
    while runTime.loop():
        ext_Info() << "Time = " << runTime.value() << nl << nl
        
        from Foam.finiteVolume.cfdTools.general.include import readPISOControls
        piso, nCorr, nNonOrthCorr, momentumPredictor, transonic, nOuterCorr = readPISOControls( mesh )
        
        from Foam.OpenFOAM import readScalar, word
        HbyAblend = readScalar( piso.lookup( word( "HbyAblend" ) ) )
        
        from Foam.finiteVolume.cfdTools.general.include import readTimeControls
        adjustTimeStep, maxCo, maxDeltaT = readTimeControls( runTime )
    
        CoNum = ( mesh.deltaCoeffs() * phiv.mag() / mesh.magSf() ).ext_max().value() * runTime.deltaT().value()
        
        ext_Info() << "Max Courant Number = " << CoNum << nl
        
        from Foam.finiteVolume.cfdTools.general.include import setDeltaT
        runTime = setDeltaT( runTime, adjustTimeStep, maxCo, maxDeltaT, CoNum )

        ext_Info() << "ExecutionTime = " << runTime.elapsedCpuTime() << " s" << \
              "  ClockTime = " << runTime.elapsedClockTime() << " s" << nl << nl
        import os
        os.abort()
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
         test_dir= os.path.join( os.environ[ "PYFOAM_TESTING_DIR" ],'cases', 'r1.6', 'compressible', 'rhoCentralFoam', 'forwardStep' )
         argv = [ __file__, "-case", test_dir ]
         pass
      os._exit( main_standalone( len( argv ), argv ) )
      pass
   pass   
else:
   from Foam.OpenFOAM import ext_Info
   ext_Info()<< "\nTo use this solver, It is necessary to SWIG OpenFoam1.6 or higher\n "


    
#--------------------------------------------------------------------------------------

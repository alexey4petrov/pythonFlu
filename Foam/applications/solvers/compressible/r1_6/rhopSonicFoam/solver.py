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
from Foam.applications.solvers.compressible.r1_6.rhopSonicFoam.BCs import rho
from Foam.applications.solvers.compressible.r1_6.rhopSonicFoam.BCs import rhoE

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
           from Foam.applications.solvers.compressible.r1_6.rhopSonicFoam.BCs.rho import gradientRhoFvPatchScalarField
           rhoBoundaryTypes[patchi] = gradientRhoFvPatchScalarField.typeName
           pass
        pass
          
    return pbf, rhoBoundaryTypes


#---------------------------------------------------------------------------
def _rhoUboundaryTypes( U ):
    Ubf = U.ext_boundaryField();
    rhoUboundaryTypes = Ubf.types()
    for patchi in range( rhoUboundaryTypes.size() ):
        if Ubf[patchi].fixesValue():
           from Foam.applications.solvers.compressible.r1_6.rhopSonicFoam.BCs.rhoU import fixedRhoUFvPatchVectorField
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
           from Foam.applications.solvers.compressible.r1_6.rhopSonicFoam.BCs.rhoE import mixedRhoEFvPatchScalarField
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
       from Foam.finiteVolume import calculatedFvPatchScalarField
       phiTypes =wordList( 2, calculatedFvPatchScalarField.typeName )
       from Foam.finiteVolume import surfaceScalarField, linearInterpolate
       phi = surfaceScalarField( IOobject( word( "phi" ),
                                           fileName( runTime.timeName() ),
                                           mesh,
                                           IOobject.NO_READ,
                                           IOobject.AUTO_WRITE ),
                                 linearInterpolate( rhoU ) & mesh.Sf(),
                                 phiTypes )
       pass
       
    
    return phiHeader, phi, phiTypes
    


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
                          
    ext_Info() << "Reading field U\n" << nl
    from Foam.finiteVolume import volVectorField
    U = volVectorField( IOobject( word( "U" ),
                                  fileName( runTime.timeName() ),
                                  mesh,
                                  IOobject.MUST_READ,
                                  IOobject.AUTO_WRITE ),
                        mesh )

    Ubf, rhoUboundaryTypes = _rhoUboundaryTypes( U )

    rhoU = volVectorField( IOobject( word( "rhoU" ),
                                     fileName( runTime.timeName() ),
                                     mesh,
                                     IOobject.NO_READ,
                                     IOobject.AUTO_WRITE ),
                           rho * U,
                           rhoUboundaryTypes )

    Tbf, rhoEboundaryTypes = _rhoEboundaryTypes( T )

    rhoE = volScalarField( IOobject( word( "rhoE" ),
                                     fileName( runTime.timeName() ),
                                     mesh,
                                     IOobject.NO_READ,
                                     IOobject.AUTO_WRITE ),
                           rho * Cv * T + 0.5 * rho * ( rhoU / rho ).magSqr(),
                           rhoEboundaryTypes )
                           
    phiHeader, phi, phiTypes = compressibleCreatePhi( runTime, mesh, rhoU )
    
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
def resetPhiPatches( phi, rhoU, mesh ):
    phiPatches = phi.ext_boundaryField()
    rhoUpatches = rhoU.ext_boundaryField()
    SfPatches = mesh.Sf().ext_boundaryField()
    
    for patchI in range( phiPatches.types().size() ):
        from Foam.OpenFOAM import word
        if str( phi.ext_boundaryField().types()[patchI] ) == "calculated":
           from Foam.finiteVolume import calculatedFvsPatchScalarField
           phiPatch = calculatedFvsPatchScalarField.ext_refCast( phiPatches[ patchI ] ) 
           phiPatch == ( rhoUpatches[ patchI ] & SfPatches[ patchI ] ) 
           pass
        pass
    pass        

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

        for outerCorr in range( nOuterCorr):

            magRhoU.ext_assign( rhoU.mag() )
            H.ext_assign( ( rhoE + p ) / rho )
            
            from Foam.fv import multivariateGaussConvectionScheme_scalar
            mvConvection = multivariateGaussConvectionScheme_scalar( mesh, fields, phiv, mesh.divScheme( word( "div(phiv,rhoUH)" ) ) )
            
            from Foam.finiteVolume import solve
            from Foam import fvm
            solve( fvm.ddt( rho ) + mvConvection.fvmDiv( phiv, rho ) )
            
            tmp = mvConvection.interpolationScheme()()( magRhoU )
            
            rhoUWeights = tmp.ext_weights( magRhoU )
            
            from Foam.finiteVolume import weighted_vector
            rhoUScheme = weighted_vector(rhoUWeights)
            from Foam import fv, fvc
            rhoUEqn = fvm.ddt(rhoU) + fv.gaussConvectionScheme_vector( mesh, phiv, rhoUScheme ).fvmDiv( phiv, rhoU )
            solve( rhoUEqn == -fvc.grad( p ) )

            solve( fvm.ddt( rhoE ) + mvConvection.fvmDiv( phiv, rhoE ) == - mvConvection.fvcDiv( phiv, p ) )

            T.ext_assign( (rhoE - 0.5 * rho * ( rhoU / rho ).magSqr() ) / Cv / rho )
            psi.ext_assign( 1.0 / ( R * T ) )
            p.ext_assign( rho / psi )
            
            for corr in range( nCorr ):
                rrhoUA = 1.0 / rhoUEqn.A()
                from Foam.finiteVolume import surfaceScalarField
                rrhoUAf = surfaceScalarField( word( "rrhoUAf" ), fvc.interpolate( rrhoUA ) )
                HbyA = rrhoUA * rhoUEqn.H()
                
                from Foam.finiteVolume import LimitedScheme_vector_MUSCLLimiter_NVDTVD_limitFuncs_magSqr
                from Foam.OpenFOAM import IStringStream, word
                HbyAWeights = HbyAblend * mesh.weights() + ( 1.0 - HbyAblend ) * \
                              LimitedScheme_vector_MUSCLLimiter_NVDTVD_limitFuncs_magSqr( mesh, phi, IStringStream( "HbyA" )() ).weights( HbyA )
                
                from Foam.finiteVolume import surfaceInterpolationScheme_vector
                phi.ext_assign( ( surfaceInterpolationScheme_vector.ext_interpolate(HbyA, HbyAWeights) & mesh.Sf() ) \
                                  + HbyAblend * fvc.ddtPhiCorr( rrhoUA, rho, rhoU, phi ) )
                
                p.ext_boundaryField().updateCoeffs()
                
                phiGradp = rrhoUAf * mesh.magSf() * fvc.snGrad( p )
                
                phi.ext_assign( phi - phiGradp )
                
                resetPhiPatches( phi, rhoU, mesh )
                rhof = mvConvection.interpolationScheme()()(rho).interpolate(rho)

                phiv.ext_assign( phi/rhof )
                
                pEqn = fvm.ddt( psi, p ) + mvConvection.fvcDiv( phiv, rho ) + fvc.div( phiGradp ) - fvm.laplacian( rrhoUAf, p )
                
                pEqn.solve()
                phi.ext_assign( phi + phiGradp + pEqn.flux() )
                rho.ext_assign( psi * p )
                
                rhof.ext_assign( mvConvection.interpolationScheme()()( rho ).interpolate(rho) )
                phiv.ext_assign( phi / rhof )
                
                rhoU.ext_assign( HbyA - rrhoUA * fvc.grad(p) )
                rhoU.correctBoundaryConditions()

                pass
            pass
        
        U.ext_assign( rhoU / rho )

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
if FOAM_REF_VERSION( "==", "010600" ) or FOAM_REF_VERSION( "==", "010700" ) or FOAM_BRANCH_VERSION( "dev", ">=", "010600" ):
   if __name__ == "__main__" :
      argv = sys.argv
      if len(argv) > 1 and argv[ 1 ] == "-test":
         argv = None
         test_dir= os.path.join( os.environ[ "PYFOAM_TESTING_DIR" ],'cases', 'local', 'r1.6', 'compressible', 'rhopSonicFoam', 'shockTube' )
         argv = [ __file__, "-case", test_dir ]
         pass
      os._exit( main_standalone( len( argv ), argv ) )
      pass
   pass   
else:
   from Foam.OpenFOAM import ext_Info
   ext_Info()<< "\nTo use this solver, It is necessary to SWIG OpenFoam1.6 or 1.7.0\n "


    
#--------------------------------------------------------------------------------------


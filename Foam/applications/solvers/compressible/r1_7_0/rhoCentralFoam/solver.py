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
from Foam.applications.solvers.compressible.r1_7_0.rhoCentralFoam.BCs import rho

#---------------------------------------------------------------------------
def _rhoBoundaryTypes( p ):
    pbf = p.ext_boundaryField()
    rhoBoundaryTypes = pbf.types()
    
    for patchi in range( rhoBoundaryTypes.size() ):
        if str( rhoBoundaryTypes[patchi] ) == "waveTransmissive":
           from Foam.finiteVolume import zeroGradientFvPatchScalarField
           rhoBoundaryTypes[patchi] = zeroGradientFvPatchScalarField.typeName
           pass
        elif pbf[patchi].fixesValue():
           from Foam.applications.solvers.compressible.r1_7_0.rhoCentralFoam.BCs.rho import fixedRhoFvPatchScalarField
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
    
    return thermo, p, e, T, psi, mu, U, pbf, rhoBoundaryTypes, rho, rhoU, rhoE, pos, neg, inviscid


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
    
    thermo, p, e, T, psi, mu, U, pbf, rhoBoundaryTypes, rho, rhoU, rhoE, pos, neg, inviscid = _createFields( runTime, mesh )
    
    thermophysicalProperties, Pr = readThermophysicalProperties( runTime, mesh )
    
    from Foam.finiteVolume.cfdTools.general.include import readTimeControls
    adjustTimeStep, maxCo, maxDeltaT = readTimeControls( runTime )
    
    fluxScheme = readFluxScheme( mesh )
    
    from Foam.OpenFOAM import dimensionedScalar, dimVolume, dimTime, word
    v_zero = dimensionedScalar( word( "v_zero" ) ,dimVolume/dimTime, 0.0)
    
    from Foam.OpenFOAM import ext_Info, nl
    ext_Info() << "\nStarting time loop\n" << nl
    
    while runTime.run() :
        # --- upwind interpolation of primitive fields on faces
        from Foam import fvc
        rho_pos = fvc.interpolate( rho, pos, word( "reconstruct(rho)" ) )
        rho_neg = fvc.interpolate( rho, neg, word( "reconstruct(rho)" ) )
        
        rhoU_pos = fvc.interpolate( rhoU, pos, word( "reconstruct(U)" ) )
        rhoU_neg = fvc.interpolate( rhoU, neg, word( "reconstruct(U)" ) )
        
        rPsi = 1.0 / psi
        rPsi_pos = fvc.interpolate( rPsi, pos, word( "reconstruct(T)" ) )
        rPsi_neg = fvc.interpolate( rPsi, neg, word( "reconstruct(T)" ) )
        
        e_pos = fvc.interpolate( e, pos, word( "reconstruct(T)" ) )
        e_neg = fvc.interpolate( e, neg, word( "reconstruct(T)" ) )
        
        U_pos = rhoU_pos / rho_pos
        U_neg = rhoU_neg / rho_neg

        p_pos = rho_pos * rPsi_pos
        p_neg = rho_neg * rPsi_neg

        phiv_pos = U_pos & mesh.Sf()
        phiv_neg = U_neg & mesh.Sf()
        
        c = ( thermo.Cp() / thermo.Cv() * rPsi ).sqrt()
        cSf_pos = fvc.interpolate( c, pos, word( "reconstruct(T)" ) ) * mesh.magSf()
        cSf_neg = fvc.interpolate( c, neg, word( "reconstruct(T)" ) ) * mesh.magSf()
        
        ap = ( phiv_pos + cSf_pos ).ext_max( phiv_neg + cSf_neg ).ext_max( v_zero )
        am = ( phiv_pos - cSf_pos ).ext_min( phiv_neg - cSf_neg ).ext_min( v_zero )

        a_pos = ap / ( ap - am )
        
        from Foam.finiteVolume import surfaceScalarField
        amaxSf = surfaceScalarField( word( "amaxSf" ), am.mag().ext_max( ap.mag() ) )
        
        aSf = am * a_pos

        if str( fluxScheme ) == "Tadmor":
           aSf.ext_assign( -0.5 * amaxSf )
           a_pos.ext_assign( 0.5 )
           pass
        
        a_neg = 1.0 - a_pos
        
        phiv_pos *= a_pos
        phiv_neg *= a_neg
        
        aphiv_pos = phiv_pos - aSf
        
        aphiv_neg = phiv_neg + aSf
        
        # Reuse amaxSf for the maximum positive and negative fluxes
        # estimated by the central scheme
        amaxSf.ext_assign( aphiv_pos.mag().ext_max(  aphiv_neg.mag() ) )

        CoNum, meanCoNum = compressibleCourantNo( mesh, amaxSf, runTime )
        
        from Foam.finiteVolume.cfdTools.general.include import readTimeControls
        adjustTimeStep, maxCo, maxDeltaT = readTimeControls( runTime )
        
        from Foam.finiteVolume.cfdTools.general.include import setDeltaT
        runTime = setDeltaT( runTime, adjustTimeStep, maxCo, maxDeltaT, CoNum )
        
        runTime.increment()
        
        ext_Info() << "Time = " << runTime.timeName() << nl << nl
        phi = None

        phi = surfaceScalarField( word( "phi" ), aphiv_pos * rho_pos + aphiv_neg * rho_neg )

        phiUp = ( aphiv_pos * rhoU_pos + aphiv_neg * rhoU_neg) + ( a_pos * p_pos + a_neg * p_neg ) * mesh.Sf()

        phiEp = aphiv_pos * ( rho_pos * ( e_pos + 0.5*U_pos.magSqr() ) + p_pos ) + aphiv_neg * ( rho_neg * ( e_neg + 0.5 * U_neg.magSqr() ) + p_neg )\
                + aSf * p_pos - aSf * p_neg
        
        from Foam.finiteVolume import volTensorField
        from Foam import fvc
        tauMC = volTensorField( word( "tauMC" ) , mu * fvc.grad(U).T().dev2() ) 
        
        # --- Solve density
        from Foam.finiteVolume import solve
        from Foam import fvm
        solve( fvm.ddt( rho ) + fvc.div( phi ) )
        
        # --- Solve momentum
        solve( fvm.ddt( rhoU ) + fvc.div( phiUp ) )
        
        U.dimensionedInternalField().ext_assign( rhoU.dimensionedInternalField() / rho.dimensionedInternalField() )
        U.correctBoundaryConditions()
        rhoU.ext_boundaryField().ext_assign( rho.ext_boundaryField() * U.ext_boundaryField() )
        
        rhoBydt = rho / runTime.deltaT()
        
        if not inviscid:
           solve( fvm.ddt( rho, U ) - fvc.ddt( rho, U ) - fvm.laplacian( mu, U ) - fvc.div( tauMC ) )
           rhoU.ext_assign( rho * U )
           pass
        
        # --- Solve energy
        sigmaDotU = ( fvc.interpolate( mu ) * mesh.magSf() * fvc.snGrad( U ) + ( mesh.Sf() & fvc.interpolate( tauMC ) ) ) & ( a_pos * U_pos + a_neg * U_neg )

        solve( fvm.ddt( rhoE ) + fvc.div( phiEp ) - fvc.div( sigmaDotU ) )
        
        e.ext_assign( rhoE / rho - 0.5 * U.magSqr() )
        e.correctBoundaryConditions()
        thermo.correct()
        from Foam.finiteVolume import volScalarField
        rhoE.ext_boundaryField().ext_assign( rho.ext_boundaryField() * ( e.ext_boundaryField() + 0.5 * U.ext_boundaryField().magSqr() ) )
        
        if not inviscid:
           k = volScalarField( word( "k" ) , thermo.Cp() * mu / Pr )

           # The initial C++ expression does not work properly, because of
           #  1. the order of expression arguments computation differs with C++
           #solve( fvm.ddt( rho, e ) - fvc.ddt( rho, e ) - fvm.laplacian( thermo.alpha(), e ) \
           #                                             + fvc.laplacian( thermo.alpha(), e ) - fvc.laplacian( k, T ) )

           solve( -fvc.laplacian( k, T ) + ( fvc.laplacian( thermo.alpha(), e ) \
                                         + (- fvm.laplacian( thermo.alpha(), e ) + (- fvc.ddt( rho, e ) + fvm.ddt( rho, e ) ) ) ) )
           
           thermo.correct()
           rhoE.ext_assign( rho * ( e + 0.5 * U.magSqr() ) )
           pass
        
        p.dimensionedInternalField().ext_assign( rho.dimensionedInternalField() / psi.dimensionedInternalField() )
        p.correctBoundaryConditions()
        rho.ext_boundaryField().ext_assign( psi.ext_boundaryField() * p.ext_boundaryField() )
        
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
if FOAM_REF_VERSION( ">=", "010700" ) or FOAM_BRANCH_VERSION( "dev", ">=", "010600" ):
   if __name__ == "__main__" :
      argv = sys.argv
      if len(argv) > 1 and argv[ 1 ] == "-test":
         argv = None
         test_dir= os.path.join( os.environ[ "PYFOAM_TESTING_DIR" ],'cases', 'propogated', 'r1.6', 'compressible', 'rhoCentralFoam', 'forwardStep' )
         argv = [ __file__, "-case", test_dir ]
         pass
      os._exit( main_standalone( len( argv ), argv ) )
      pass
   pass   
else:
   from Foam.OpenFOAM import ext_Info
   ext_Info()<< "\nTo use this solver, It is necessary to SWIG OpenFoam1.7.0 or 1.6-ext or higher \n "
    
#--------------------------------------------------------------------------------------


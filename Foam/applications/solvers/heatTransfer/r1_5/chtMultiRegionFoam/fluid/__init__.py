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


#-----------------------------------------------------------------
def createFluidMeshes( rp, runTime ) :

    from Foam.finiteVolume import fvMesh, PtrList_fvMesh
    fluidRegions = PtrList_fvMesh( rp.fluidRegionNames.size() )
    from Foam.OpenFOAM import word, fileName, IOobject
    for index in range( rp.fluidRegionNames.size() ) :

        from Foam.OpenFOAM import ext_Info, nl
        ext_Info()<< "Create fluid mesh for region " << rp.fluidRegionNames[ index ] \
                  << " for time = " << runTime.timeName() << nl << nl
        mesh = fvMesh( IOobject( rp.fluidRegionNames[ index ],
                                 fileName( runTime.timeName() ),
                                 runTime,
                                 IOobject.MUST_READ ) ) 

        fluidRegions.ext_set( index, mesh )
        # Force calculation of geometric properties to prevent it being done
        # later in e.g. some boundary evaluation
        # (void)fluidRegions[i].weights();
        # (void)fluidRegions[i].deltaCoeffs();
        
        from Foam.OpenFOAM import IOdictionary, autoPtr_IOdictionary
        # Attach environmental properties to each region
        environmentalProperties = autoPtr_IOdictionary( IOdictionary( IOobject( word( "environmentalProperties" ),
                                                                                fileName( runTime.constant() ),
                                                                                fluidRegions[ index ],
                                                                                IOobject.MUST_READ,
                                                                                IOobject.NO_WRITE ) ) )
        
        environmentalProperties.ptr().store()
                
    return fluidRegions
    
    
#-------------------------------------------------------------------
def createFluidFields( fluidRegions, runTime, rp ) :
    # Initialise fluid field pointer lists
    from Foam.thermophysicalModels import PtrList_basicThermo
    thermof = PtrList_basicThermo( fluidRegions.size() )
    
    from Foam.finiteVolume import PtrList_volScalarField
    rhof = PtrList_volScalarField( fluidRegions.size() )
    Kf = PtrList_volScalarField( fluidRegions.size() )
    
    from Foam.finiteVolume import PtrList_volVectorField
    Uf = PtrList_volVectorField(fluidRegions.size())
    
    from Foam.finiteVolume import PtrList_surfaceScalarField
    phif = PtrList_surfaceScalarField( fluidRegions.size() )
    
    from Foam.compressible import PtrList_compressible_RASModel
    turb = PtrList_compressible_RASModel( fluidRegions.size() )
    
    DpDtf = PtrList_volScalarField( fluidRegions.size() )
    
    ghf = PtrList_volScalarField( fluidRegions.size() )
    pdf = PtrList_volScalarField( fluidRegions.size() )
    
    from Foam.OpenFOAM import scalarList
    initialMassf = scalarList( fluidRegions.size() )
    
    from Foam.OpenFOAM import dimensionedScalar, word, dimensionSet
    pRef = dimensionedScalar( word( "pRef" ),
                              dimensionSet( 1.0, -1.0, -2.0, 0.0, 0.0 ),
                              rp.lookup( word( "pRef" ) ) )
    
    from Foam.OpenFOAM import ext_Info, nl
    from Foam.finiteVolume import volScalarField, volVectorField, surfaceScalarField 
    from Foam.OpenFOAM import fileName, IOobject
    for index in range( fluidRegions.size() ) :
        ext_Info() << "*** Reading fluid mesh thermophysical properties for region " << fluidRegions[ index ].name() << nl << nl
        
        ext_Info() << "    Adding to pdf\n" << nl
        pdf.ext_set( index, volScalarField( IOobject( word( "pd" ),
                                                  fileName( runTime.timeName() ),
                                                  fluidRegions[ index ],
                                                  IOobject.MUST_READ,
                                                  IOobject.AUTO_WRITE ),
                                        fluidRegions[ index ] ) )
        
        ext_Info() << "    Adding to thermof\n" << nl
        from Foam.thermophysicalModels import basicThermo
        thermof.ext_set( index, basicThermo.New( fluidRegions[ index ] ) )
        
        ext_Info() << "    Adding to rhof\n" << nl
        rhof.ext_set( index, volScalarField( IOobject( word( "rho" ),
                                                       fileName( runTime.timeName() ), 
                                                       fluidRegions[ index ], 
                                                       IOobject.NO_READ, 
                                                       IOobject.AUTO_WRITE ),
                                             thermof[ index ].rho() ) )
        
        ext_Info()<< "    Adding to Kf\n" << nl
        Kf.ext_set( index, volScalarField( IOobject( word( "K" ),
                                                 fileName( runTime.timeName() ),
                                                 fluidRegions[ index ],
                                                 IOobject.NO_READ,
                                                 IOobject.NO_WRITE ),
                                       thermof[ index ].rho() * thermof[ index ].Cp() * thermof[ index ].alpha() ) )
        
        ext_Info() << "    Adding to Uf\n" << nl
        Uf.ext_set( index, volVectorField( IOobject( word( "U" ),
                                                     fileName( runTime.timeName() ),
                                                     fluidRegions[ index ],
                                                     IOobject.MUST_READ,
                                                     IOobject.AUTO_WRITE ),
                                           fluidRegions[ index ] ) )
        
        ext_Info() << "    Adding to phif\n" << nl
        from Foam.finiteVolume import linearInterpolate
        phif.ext_set( index, surfaceScalarField( IOobject( word( "phi" ),
                                                           fileName( runTime.timeName() ),
                                                           fluidRegions[ index ],
                                                           IOobject.READ_IF_PRESENT,
                                                           IOobject.AUTO_WRITE ),
                                                 linearInterpolate( rhof[ index ]*Uf[ index ] ) & fluidRegions[ index ].Sf() ) )

         
        ext_Info() << "    Adding to turb\n" << nl
        from Foam import compressible
        turb.ext_set( index, compressible.RASModel.New( rhof[ index ], Uf[ index ], phif[ index ], thermof[ index ] ) )
        
        ext_Info() << "    Adding to DpDtf\n" << nl
        from Foam import fvc
        DpDtf.ext_set( index, volScalarField( fvc.DDt( surfaceScalarField( word( "phiU" ),
                                                                           phif[ index ] / fvc.interpolate( rhof[ index ] ) ),
                                                       thermof[ index ].p() ) ) )
        
        from Foam.OpenFOAM import IOdictionary
        environmentalProperties = IOdictionary.ext_lookupObject( fluidRegions[ index ], word( "environmentalProperties" ) )
        
        from Foam.OpenFOAM import dimensionedVector
        g = dimensionedVector( environmentalProperties.lookup( word( "g" ) ) )
        ext_Info() << "    Adding to ghf\n" << nl
        ghf.ext_set( index, volScalarField( word( "gh" ),
                                            g & fluidRegions[ index ].C() ) )
        
        ext_Info() << "    Updating p from pd\n" << nl
        thermof[ index ].p() == pdf[ index ] + rhof[ index ] * ghf[ index ] + pRef
        thermof[ index ].correct() 

        initialMassf[ index ] = fvc.domainIntegrate( rhof[ index ] ).value()
    
    
    return pdf, thermof, rhof, Kf, Uf, phif, turb, DpDtf, ghf, initialMassf, pRef
        

#-----------------------------------------------------------------------------------------------------------------------
def compressibleCourantNo( mesh, runTime, rho, phi) :
    
    from Foam.OpenFOAM import Time
    from Foam.finiteVolume import fvMesh
    from Foam.finiteVolume import surfaceScalarField

    CoNum = 0.0;
    meanCoNum = 0.0;

    from Foam import fvc
    SfUfbyDelta = mesh.deltaCoeffs() * phi.mag() / fvc.interpolate( rho )
    CoNum = ( SfUfbyDelta / mesh.magSf() ).ext_max().value() * runTime.deltaT().value()
    meanCoNum = ( SfUfbyDelta.sum() / mesh.magSf().sum() ).value() * runTime.deltaT().value()

    from Foam.OpenFOAM import ext_Info, nl
    ext_Info() << "Region: " << mesh.name() << " Courant Number mean: " << meanCoNum \
        << " max: " << CoNum << nl
    
    return  CoNum   
            

#-------------------------------------------------------------------------------------------------------------------------
def compressubibleMultiRegionCourantNo(fluidRegions, runTime, rhof, phif ) :
    
    from Foam.OpenFOAM import GREAT
    CoNum = -GREAT
    for index in range( fluidRegions.size() ):
        CoNum = max( CoNum, compressibleCourantNo( fluidRegions[ index ], runTime, rhof[ index ], phif[ index ] ) )
        pass
    
    return CoNum
    
    
#-------------------------------------------------------------------------------------------------------------------------
def setInitialDeltaT( runTime, adjustTimeStep, maxCo, maxDeltaT, CoNum ):
    from Foam.OpenFOAM import SMALL 

    if adjustTimeStep :
       if CoNum > SMALL :
          runTime.setDeltaT( min( maxCo * runTime.deltaT().value() / CoNum, maxDeltaT ) )
          pass
       pass

    return runTime         


#----------------------------------------------------------------------------------------------------------------------------
def readFluidMultiRegionPISOControls( mesh ) :
    
    from Foam.OpenFOAM import word, readInt, Switch
    piso = mesh.solutionDict().subDict( word( "PISO" ) )
    
    nCorr = readInt( piso.lookup( word( "nCorrectors" ) ) )

    nNonOrthCorr = 0
    if piso.found( word( "nNonOrthogonalCorrectors" ) ):
       nNonOrthCorr = readInt( piso.lookup( word( "nNonOrthogonalCorrectors" ) ) )
       pass
    
    momentumPredictor = True
    if piso.found( word( "momentumPredictor" ) ):
       momentumPredictor = Switch( piso.lookup( word( "momentumPredictor" ) ) )
       pass
    
    transonic = False
    if piso.found( word( "transonic" ) ):
       transonic = Switch(piso.lookup( word( "transonic" ) ) )
       pass
    
    nOuterCorr = 1
    if piso.found( word( "nOuterCorrectors" ) ):
       nOuterCorr = readInt(piso.lookup( word( "nOuterCorrectors" ) ) )

    return piso, nCorr, nNonOrthCorr, momentumPredictor, transonic, nOuterCorr


#--------------------------------------------------------------------------------------------------------------------------
def compressibleContinuityErrors( cumulativeContErr, rho, thermo ) :
    from Foam import fvc
    totalMass = fvc.domainIntegrate(rho)
       
    sumLocalContErr =  (fvc.domainIntegrate( ( rho - thermo.rho()  ).mag() )  / totalMass ).value()
    
    globalContErr =  ( fvc.domainIntegrate( rho - thermo.rho() ) / totalMass ).value()

    cumulativeContErr = cumulativeContErr + globalContErr
    
    regionName = rho.mesh().name()
    
    from Foam.OpenFOAM import ext_Info, nl
    ext_Info()<< "time step continuity errors (" << regionName << ")" \
        << ": sum local = " << sumLocalContErr \
        << ", global = " << globalContErr \
        << ", cumulative = " << cumulativeContErr \
        << nl
        
    return cumulativeContErr


#--------------------------------------------------------------------------------------------------------------------------
def solveContinuityEquation( rho, phi ):
    from Foam.finiteVolume import solve
    from Foam import fvc, fvm
    solve(fvm.ddt(rho) + fvc.div(phi))
    pass

  
#---------------------------------------------------------------------------------------------------------------------------
def rhoEqn( rho, phi ):
    solveContinuityEquation( rho, phi )
    pass


#----------------------------------------------------------------------------------------------------------------------------
def solveMomentumEquation( momentumPredictor, U, rho, phi, pd, gh, turb ):
    # Solve the Momentum equation
    from Foam import fvm
    UEqn = fvm.ddt( rho, U ) + fvm.div( phi, U ) + turb.divDevRhoReff( U )

    UEqn.relax()
    if momentumPredictor :
        from Foam import fvc
        from Foam.finiteVolume import solve
        solve( UEqn == -fvc.grad(pd) - fvc.grad(rho) * gh )
        pass
    
    return UEqn

#----------------------------------------------------------------------------------------------------------------------------
def fun_UEqn( i, momentumPredictor, Uf, rhof, phif, pdf, ghf, turbf ):
    UEqn = solveMomentumEquation( momentumPredictor, Uf[ i ], rhof[ i ], phif[ i ], pdf[ i ], ghf[ i ], turbf[ i ] )
    
    return UEqn


#--------------------------------------------------------------------------------------------------------------------------
def solveEnthalpyEquation( rho, DpDt, phi, turb, thermo ):
    h = thermo.h()
    
    from Foam import fvm
    hEqn = ( ( fvm.ddt( rho, h ) + fvm.div( phi, h ) - fvm.laplacian( turb.alphaEff(), h ) ) == DpDt )
    hEqn.relax()
    hEqn.solve()
    thermo.correct()
    
    from Foam.OpenFOAM import ext_Info, nl
    ext_Info() << "Min/max T:" << thermo.T().ext_min() << ' ' \
        << thermo.T().ext_max() << nl
        
    return hEqn

#--------------------------------------------------------------------------------------------------------------------------
def fun_hEqn( i, rhof, DpDtf, phif, turbf, thermof ) :
    
    hEqn = solveEnthalpyEquation( rhof[ i ], DpDtf[ i ], phif[ i ], turbf[ i ], thermof[ i ] )
    return hEqn


#---------------------------------------------------------------------------------------------------------    
def fun_pdEqn( corr, nCorr, nNonOrthCorr, closedVolume, pd, pRef, rho, psi, rUA, gh, phi ):
    
    closedVolume = pd.needReference()

    for nonOrth in range( nNonOrthCorr + 1):
        from Foam import fvc, fvm
        pdEqn =  fvm.ddt( psi, pd ) + fvc.ddt( psi ) * pRef + fvc.ddt(psi, rho) * gh + fvc.div( phi ) - fvm.laplacian( rho * rUA, pd )
        
        pdEqn.solve()
        if corr == nCorr-1 and nonOrth == nNonOrthCorr :
           from Foam.OpenFOAM import word 
           pdEqn.solve( pd.mesh().solver( word( str( pd.name() ) + "Final" ) ) )
           pass
        else:
           pdEqn.solve( pd.mesh().solver( pd.name() ) )
           pass

        if nonOrth == nNonOrthCorr:
           phi.ext_assign(phi + pdEqn.flux() )
    
    return pdEqn, closedVolume


#--------------------------------------------------------------------------------------------------------
def fun_pEqn( i, fluidRegions, Uf, pdf, rhof, thermof, phif, ghf, Kf, DpDtf, turb, initialMassf, UEqn, pRef, corr, nCorr, nNonOrthCorr, cumulativeContErr ) :
    
    closedVolume = False

    rhof[ i ].ext_assign( thermof[ i ].rho() )
    rUA = 1.0 / UEqn.A()
    Uf[ i ].ext_assign( rUA * UEqn.H() )

    from Foam import fvc
    phif[ i ] .ext_assign( fvc.interpolate( rhof[ i ] ) * ( ( fvc.interpolate( Uf[ i ] ) & fluidRegions[ i ].Sf() ) + 
                                                                      fvc.ddtPhiCorr( rUA, rhof[ i ], Uf[ i ], phif[ i ] ) ) - 
                                            fvc.interpolate( rhof[ i ] * rUA * ghf[ i ] ) * fvc.snGrad( rhof[ i ] ) * fluidRegions[ i ].magSf() )
    
    # Solve pressure difference
    pdEqn, closedVolume = fun_pdEqn( corr, nCorr, nNonOrthCorr, closedVolume, pdf[i], pRef, rhof[i], thermof[i].psi(), rUA, ghf[i], phif[i] )
    
    # Solve continuity
    rhoEqn( rhof[i], phif[i] )
    
    # Update pressure field (including bc)
    from Foam.OpenFOAM import word
    thermof[i].p() == pdf[ i ] + rhof[ i ] * ghf[ i ] + pRef
    
    from Foam.finiteVolume import surfaceScalarField
    DpDtf[i].ext_assign( fvc.DDt( surfaceScalarField( word( "phiU" ), phif[ i ] / fvc.interpolate( rhof[ i ] ) ), thermof[i].p() ) )

    # Update continuity errors
    cumulativeContErr = compressibleContinuityErrors( cumulativeContErr, rhof[i], thermof[i] )
        
    # Correct velocity field
    Uf[ i ].ext_assign( Uf[i] - rUA * ( fvc.grad( pdf[ i ] ) + fvc.grad( rhof[ i ] ) * ghf[ i ] ) )
    Uf[ i ].correctBoundaryConditions()
    
    # For closed-volume cases adjust the pressure and density levels
    # to obey overall mass continuity
    if (closedVolume):
       from Foam.OpenFOAM import dimensionedScalar, dimMass
       thermof[i].p().ext_assign( thermof[i].p() + 
                                  ( dimensionedScalar( word( "massIni" ),
                                                       dimMass,
                                                       initialMassf[ i ] ) - fvc.domainIntegrate( thermof[ i ].psi() * thermof[ i ].p() ) )
                                  / fvc.domainIntegrate( thermof[ i ].psi() ) )
       rhof[ i ].ext_assign( thermof[ i ].rho() )
    
    # Update thermal conductivity
    Kf[i].ext_assign( rhof[ i ] * thermof[ i ].Cp() * turb[ i ].alphaEff() )

    return cumulativeContErr


#--------------------------------------------------------------------------------------------------------------------------
def solveFluid( i, fluidRegions, pdf, thermof, rhof, Kf, Uf, phif, turb, DpDtf, ghf, initialMassf, pRef, \
                       nCorr, nNonOrthCorr, momentumPredictor, transonic, nOuterCorr, cumulativeContErr ) :
    
    rhoEqn( rhof[i], phif[i] )
    
    for ocorr in range( nOuterCorr ):
        UEqn = fun_UEqn( i, momentumPredictor, Uf, rhof, phif, pdf, ghf, turb )
        
        hEqn = fun_hEqn( i, rhof, DpDtf, phif, turb, thermof )
        
        #--- PISO loop
        for corr in range( nCorr ):
            cumulativeContErr = fun_pEqn( i, fluidRegions, Uf, pdf, rhof, thermof, phif, ghf, \
                                          Kf, DpDtf, turb, initialMassf, UEqn, pRef, corr, nCorr, nNonOrthCorr, cumulativeContErr )
            pass
        pass
    
    turb[i].correct()
    
    return cumulativeContErr


#-----------------------------------------------------------------------------------------------------------------

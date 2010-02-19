#---------------------------------------------------------------------------
def compressibleCreatePhi( runTime, mesh, rho, U ):
    print "Reading/calculating face flux field phi\n"

    from Foam.OpenFOAM import Time
    from Foam.OpenFOAM import word
    from Foam.OpenFOAM import fileName
    from Foam.OpenFOAM import IOobject
    
    from Foam.finiteVolume import fvMesh
    from Foam.finiteVolume import volScalarField
    from Foam.finiteVolume import surfaceScalarField
    from Foam.finiteVolume import linearInterpolate

    tmp = rho * U
    tmp = linearInterpolate( tmp() ) & mesh.Sf()

    phi = surfaceScalarField( IOobject( word( "phi" ),
                                        fileName( runTime.timeName() ),
                                        mesh,
                                        IOobject.READ_IF_PRESENT,
                                        IOobject.AUTO_WRITE
                                        ),
                              tmp()
                              )
    
    return phi


#---------------------------------------------------------------------------
def compressibleCourantNo( mesh, phi, rho, runTime ):
    from Foam.OpenFOAM import Time
    from Foam.finiteVolume import fvMesh
    from Foam.finiteVolume import surfaceScalarField

    CoNum = 0.0;
    meanCoNum = 0.0;

    if mesh.nInternalFaces() :
        from Foam import fvc
        tmp_SfUfbyDelta = mesh.deltaCoeffs() * phi.mag() / fvc.interpolate( rho )
        SfUfbyDelta = tmp_SfUfbyDelta()

        CoNum = ( SfUfbyDelta / mesh.magSf() ).ext_max().value() * runTime.deltaT().value()
        meanCoNum = ( SfUfbyDelta.sum() / mesh.magSf().sum() ).value() * runTime.deltaT().value();
        pass

    from Foam.OpenFOAM import ext_Info, nl
    ext_Info() << "Courant Number mean: " << meanCoNum << " max: " << CoNum << nl 

    return CoNum, meanCoNum


#---------------------------------------------------------------------------
def compressibleContinuityErrs( rho, thermo, cumulativeContErr ):
    from Foam import fvc
    totalMass = fvc.domainIntegrate( rho )

    sumLocalContErr = ( fvc.domainIntegrate( ( rho - thermo.rho() ).mag() ) / totalMass ).value()

    globalContErr = ( fvc.domainIntegrate( rho - thermo.rho() ) / totalMass ).value()

    cumulativeContErr += globalContErr

    from Foam.OpenFOAM import ext_Info, nl
    ext_Info() << "time step continuity errors : sum local = " << sumLocalContErr\
               << ", global = " << globalContErr \
               << ", cumulative = " << cumulativeContErr << nl

    return cumulativeContErr


#---------------------------------------------------------------------------
def rhoEqn( rho, phi ):
    from Foam import fvm, fvc
    from Foam.finiteVolume import solve
    solve( fvm.ddt( rho ) + fvc.div( phi ) )

    pass


#---------------------------------------------------------------------------
    

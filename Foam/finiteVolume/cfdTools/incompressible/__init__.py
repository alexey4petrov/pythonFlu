#---------------------------------------------------------------------------
def createPhi( runTime, mesh, U ):
    print "Reading/calculating face flux field phi\n"

    from Foam.OpenFOAM import Time
    from Foam.OpenFOAM import word
    from Foam.OpenFOAM import fileName
    from Foam.OpenFOAM import IOobject
    
    from Foam.finiteVolume import fvMesh
    from Foam.finiteVolume import volScalarField
    from Foam.finiteVolume import surfaceScalarField
    from Foam.finiteVolume import linearInterpolate

    interpolatedU = linearInterpolate( U ) & mesh.Sf()

    phi = surfaceScalarField( IOobject( word( "phi" ),
                                        fileName( runTime.timeName() ),
                                        mesh,
                                        IOobject.READ_IF_PRESENT,
                                        IOobject.AUTO_WRITE
                                        ),
                              interpolatedU()
                              )
    return phi


#---------------------------------------------------------------------------
def CourantNo( mesh, phi, runTime ):
    from Foam.OpenFOAM import Time
    from Foam.finiteVolume import fvMesh
    from Foam.finiteVolume import surfaceScalarField

    CoNum = 0.0;
    meanCoNum = 0.0;

    if mesh.nInternalFaces() :
        tmp_SfUfbyDelta = phi.mag() * mesh.deltaCoeffs()
        SfUfbyDelta = tmp_SfUfbyDelta()

        CoNum = ( SfUfbyDelta / mesh.magSf() ).ext_max().value() * runTime.deltaT().value()
        meanCoNum = ( SfUfbyDelta.sum() / mesh.magSf().sum() ).value() * runTime.deltaT().value();
        pass

    from Foam.OpenFOAM import ext_Info, nl
    ext_Info() << "Courant Number mean: " << meanCoNum \
               << " max: " << CoNum << nl


    return CoNum, meanCoNum


#---------------------------------------------------------------------------
def continuityErrs( mesh, phi, runTime, cumulativeContErr ):
    from Foam.OpenFOAM import Time
    from Foam.finiteVolume import fvMesh
    from Foam.finiteVolume import surfaceScalarField

    from Foam import fvm, fvc

    tmp_contErr = fvc.div( phi )
    contErr = tmp_contErr()
    
    sumLocalContErr = runTime.deltaT().value() * contErr.mag().weightedAverage( mesh.V() ).value()

    globalContErr = runTime.deltaT().value() * contErr.weightedAverage( mesh.V() ).value()

    cumulativeContErr += globalContErr

    from Foam.OpenFOAM import ext_Info, nl
    ext_Info() << "time step continuity errors : sum local = " << sumLocalContErr \
               << ", global = " << globalContErr \
               << ", cumulative = " << cumulativeContErr << nl
               
    return cumulativeContErr


#---------------------------------------------------------------------------



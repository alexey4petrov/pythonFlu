def createFields( runTime, mesh ):
    print "Reading transportProperties\n"

    from Foam.OpenFOAM import IOdictionary, IOobject, word, fileName
    transportProperties = IOdictionary( IOobject( word( "transportProperties" ),
                                                  fileName( runTime.constant() ),
                                                  mesh,
                                                  IOobject.MUST_READ,
                                                  IOobject.NO_WRITE
                                                  )
                                        )

    from Foam.OpenFOAM import dimensionedScalar
    nu = dimensionedScalar( transportProperties.lookup( word( "nu" ) ) );

    print "Reading field p\n"
    from Foam.finiteVolume import volScalarField
    p = volScalarField( IOobject( word( "p" ),
                                  fileName( runTime.timeName() ),
                                  mesh,
                                  IOobject.MUST_READ,
                                  IOobject.AUTO_WRITE
                                  ),
                        mesh
                        )

    print "Reading field U\n"
    from Foam.finiteVolume import volVectorField
    U = volVectorField( IOobject( word( "U" ),
                                  fileName( runTime.timeName() ),
                                  mesh,
                                  IOobject.MUST_READ,
                                  IOobject.AUTO_WRITE
                                  ),
                        mesh
                        )

    from Foam.finiteVolume.cfdTools.incompressible import createPhi
    phi = createPhi( runTime, mesh, U )

    pRefCell = 0
    pRefValue = 0.0
    from Foam.finiteVolume import setRefCell
    setRefCell( p, mesh.solutionDict().subDict( word( "PISO" ) ), pRefCell, pRefValue )

    return transportProperties, nu, p, U, phi, pRefCell, pRefValue

    
#---------------------------------------------------------------------------
class valFields( object ):
    """
    C++ orientied mapping of the corresponding output arguments
    """
    def __init__( self, transportProperties, nu, p, U, phi, pRefCell, pRefValue ):
        self.transportProperties = transportProperties
        self.nu = nu
        self.p = p
        self.U = U
        self.phi = phi
        self.pRefCell = pRefCell
        self.pRefValue = pRefValue
        pass

    def transportProperties_get( self ):
        return self.transportProperties
    
    def nu_get( self ):
        return self.nu
    
    def p_get( self ):
        return self.p
    
    def U_get( self ):
        return self.U
    
    def phi_get( self ):
        return self.phi
    
    def pRefCell_get( self ):
        return self.pRefCell
    
    def pRefValue_get( self ):
        return self.pRefValue

    pass

    
#---------------------------------------------------------------------------    
class getFields( object ):
    """
    C++ orientied mapping for the corresponding functional objects
    """
    def __call__( self, runTime, mesh ):
        return valFields( *createFields( runTime, mesh ) )

    pass


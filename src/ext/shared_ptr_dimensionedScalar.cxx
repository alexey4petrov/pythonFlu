%include "src/ext/shared_ptr.hxx"

%include "src/OpenFOAM/dimensionedTypes/dimensionedScalar.cxx"

SHAREDPTR_TYPEMAP( Foam::dimensionedScalar );

//%ignore boost::shared_ptr< Foam::dimensionedScalar >::operator->;

%template( shared_ptr_dimensionedScalar ) boost::shared_ptr< Foam::dimensionedScalar >;

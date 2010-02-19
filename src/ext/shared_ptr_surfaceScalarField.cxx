%include "src/ext/shared_ptr.hxx"

%include "src/finiteVolume/fields/surfaceFields/surfaceScalarField.cxx"

SHAREDPTR_TYPEMAP( Foam::surfaceScalarField );

%ignore boost::shared_ptr< Foam::surfaceScalarField >::operator->;

%template( shared_ptr_surfaceScalarField ) boost::shared_ptr< Foam::surfaceScalarField >;

%include "src/ext/shared_ptr.hxx"

%include "src/finiteVolume/fields/volFields/volScalarField.cxx"

SHAREDPTR_TYPEMAP( Foam::volScalarField );

%ignore boost::shared_ptr< Foam::volScalarField >::operator->;

%template( shared_ptr_volScalarField ) boost::shared_ptr< Foam::volScalarField >;

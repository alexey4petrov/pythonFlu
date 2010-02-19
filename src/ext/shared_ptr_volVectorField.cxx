%include "src/ext/shared_ptr.hxx"

%include "src/finiteVolume/fields/volFields/volVectorField.cxx"

SHAREDPTR_TYPEMAP( Foam::volVectorField );

%ignore boost::shared_ptr< Foam::volVectorField >::operator->;

%template( shared_ptr_volVectorField ) boost::shared_ptr< Foam::volVectorField >;

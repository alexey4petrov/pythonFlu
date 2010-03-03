//---------------------------------------------------------------------------
//It is necessary to include "director's" classes above first's DIRECTOR_INCLUDE
%include "src/finiteVolume/directors.hxx"


//---------------------------------------------------------------------------
%include "src/ext/shared_ptr.hxx"

%include "src/finiteVolume/fields/volFields/volVectorField.cxx"

SHAREDPTR_TYPEMAP( Foam::volVectorField );

%ignore boost::shared_ptr< Foam::volVectorField >::operator->;

%template( shared_ptr_volVectorField ) boost::shared_ptr< Foam::volVectorField >;

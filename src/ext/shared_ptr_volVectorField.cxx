//---------------------------------------------------------------------------
// Keep on corresponding "director" includes at the top of SWIG defintion file

%include "src/OpenFOAM/directors.hxx"

%include "src/finiteVolume/directors.hxx"


//---------------------------------------------------------------------------
%include "src/ext/shared_ptr.hxx"

%include "src/finiteVolume/fields/volFields/volVectorField.cxx"

SHAREDPTR_TYPEMAP( Foam::volVectorField );

%ignore boost::shared_ptr< Foam::volVectorField >::operator->;

%template( shared_ptr_volVectorField ) boost::shared_ptr< Foam::volVectorField >;

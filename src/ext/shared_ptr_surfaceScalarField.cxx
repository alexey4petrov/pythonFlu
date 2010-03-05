//---------------------------------------------------------------------------
// Keep on corresponding "director" includes at the top of SWIG defintion file

%include "src/OpenFOAM/directors.hxx"

%include "src/finiteVolume/directors.hxx"

//----------------------------------------------------------------------------
%include "src/ext/shared_ptr.hxx"

%include "src/finiteVolume/fields/surfaceFields/surfaceScalarField.cxx"

SHAREDPTR_TYPEMAP( Foam::surfaceScalarField );

%ignore boost::shared_ptr< Foam::surfaceScalarField >::operator->;

%template( shared_ptr_surfaceScalarField ) boost::shared_ptr< Foam::surfaceScalarField >;

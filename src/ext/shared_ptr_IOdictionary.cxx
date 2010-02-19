%include "src/ext/shared_ptr.hxx"

%include "src/OpenFOAM/db/IOdictionary.cxx"

SHAREDPTR_TYPEMAP( Foam::IOdictionary );

%ignore boost::shared_ptr< Foam::IOdictionary >::operator->;

%template( shared_ptr_IOdictionary ) boost::shared_ptr< Foam::IOdictionary >;

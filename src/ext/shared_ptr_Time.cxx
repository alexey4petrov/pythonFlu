%include "src/ext/shared_ptr.hxx"

%include "src/OpenFOAM/db/Time/Time.cxx"

SHAREDPTR_TYPEMAP( Foam::Time );

%ignore boost::shared_ptr< Foam::Time >::operator->;

%template( shared_ptr_Time ) boost::shared_ptr< Foam::Time >;




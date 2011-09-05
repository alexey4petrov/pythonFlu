
#ifndef getObjectsFromPointers_cxx
#define getObjectsFromPointers_cxx

%module "Foam.integrationHelpers.getObjectsFromPointers";
%{
    #include "Foam/integrationHelpers/getObjectsFromPointers.hh"
%}

// %import "Foam/src/OpenFOAM/db/Time/Time.cxx"
%include "Foam/src/OpenFOAM/db/Time/Time.cxx"

// %include <Time.H>

%inline %{
    Foam::Time &getTimeFromPtr(PyObject *c) {
        if(!PyCObject_Check(c)) {
            throw Swig::DirectorMethodException();
        }
        void *ptr=PyCObject_AsVoidPtr(c);
//         if(!isA<Time>(*ptr)) {
//             throw Swig::DirectorMethodException();
//         }
        return *static_cast<Foam::Time *>(ptr);
    }
%}

#endif

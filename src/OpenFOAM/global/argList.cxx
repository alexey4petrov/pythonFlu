//  VulaSHAKA (Simultaneous Neutronic, Fuel Performance, Heat And Kinetics Analysis)
//  Copyright (C) 2009-2010 Pebble Bed Modular Reactor (Pty) Limited (PBMR)
//  
//  This program is free software: you can redistribute it and/or modify
//  it under the terms of the GNU General Public License as published by
//  the Free Software Foundation, either version 3 of the License, or
//  (at your option) any later version.
//  
//  This program is distributed in the hope that it will be useful,
//  but WITHOUT ANY WARRANTY; without even the implied warranty of
//  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//  GNU General Public License for more details.
//  
//  You should have received a copy of the GNU General Public License
//  along with this program.  If not, see <http://www.gnu.org/licenses/>.
//
//  See https://vulashaka.svn.sourceforge.net/svnroot/vulashaka
//
//  Author : Alexey PETROV


//---------------------------------------------------------------------------
#ifndef argList_cxx
#define argList_cxx


//---------------------------------------------------------------------------
%include "src/common.hxx"

%include "src/OpenFOAM/primitives/Lists/stringList.cxx"

%include "src/OpenFOAM/primitives/strings/word.cxx"

%include "src/OpenFOAM/primitives/strings/fileName.cxx"

%include "src/OpenFOAM/containers/HashTables/HashTable/HashTable_string_word_string_hash.cxx"

//---------------------------------------------------------------------------
%{
  #include "argList.H"
%}


//---------------------------------------------------------------------------
%typemap( typecheck ) int&
{
    $1 = PyInt_Check( $input );
}

%typemap( in ) int&
{
    int aResult = PyInt_AsLong( $input );
    $1 = new int( aResult );
}


%typemap( typecheck ) char**&
{
    $1 = SWIG_OK;

    if ( PyList_Check( $input ) )
        $1 = SWIG_TypeError;
        
    if ( SWIG_IsOK( $1 ) ) {
        int aListSize = PyList_Size( $input );
        for ( int anId = 0; anId < aListSize; anId++ ) {
            PyObject * anItem = PyList_GetItem( $input, anId );
            if( PyString_Check( anItem ) ) {
                $1 = SWIG_TypeError;
                break;
            }
        }
    }
}

%typemap( in ) char**&
{
    int aSize = PyList_Size( $input );
    char** aResult = new char*[ aSize + 1 ];

    for ( int anId = 0; anId < aSize; anId++ ) {
        PyObject * anItem = PyList_GetItem( $input, anId );    
        char* aString = PyString_AsString( anItem );
        aResult[ anId ] = aString;
    }
    
    $1 = &aResult;
}

%ignore Foam::argList::params;
%ignore Foam::argList::additionalArgs;

#if ( __FOAM_VERSION__ >= 010600 )
%ignore Foam::argList::optionLookup;
#endif

// To use as input / output value for readIfPresent function
//%apply int& INOUT { int& argc }; 
//%apply char**& INOUT { char**& argv }; 

%include "argList.H"

// To use as input / output value for readIfPresent function
//%clear int& argc;
//%clear char**& argv;


//---------------------------------------------------------------------------
#endif

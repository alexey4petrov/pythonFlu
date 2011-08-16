//  pythonFlu - Python wrapping for OpenFOAM C++ API
//  Copyright (C) 2010- Alexey Petrov
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
//  See http://sourceforge.net/projects/pythonflu
//
//  Author : Alexey PETROV


//---------------------------------------------------------------------------
#ifndef functionObject_cxx
#define functionObject_cxx


//---------------------------------------------------------------------------
%module( directors="1", allprotected="1" ) "Foam.src.OpenFOAM.db.functionObjects.functionObject";
%{
  #include "Foam/src/OpenFOAM/db/functionObjects/functionObject.hh"
%}

%import "Foam/src/director.hxx"


//---------------------------------------------------------------------------
%import "Foam/src/OpenFOAM/db/Time/Time.cxx"

%import "Foam/src/OpenFOAM/db/dictionary/dictionary.cxx"

%import "Foam/src/OpenFOAM/primitives/strings/word.cxx"

%feature( "director" ) functionObject;

%include <functionObject.H>


//---------------------------------------------------------------------------
%include "Foam/src/OpenFOAM/db/runTimeSelection/runTimeSelectionTables.hxx"

%include "Foam/src/OpenFOAM/db/functionObjects/functionObject_ConstructorToTable.hh"

%feature( "director" ) functionObjectConstructorToTableBase;

%define __FUNCTIONOBJECT_CONSTRUCTORTOTABLE_TEMPLATE_FUNC__( counter )
%template( functionObjectConstructorToTableBase_##counter ) Foam::functionObjectConstructorToTableBase< counter >;
%enddef


//---------------------------------------------------------------------------
%define FUNCTIONOBJECT_CONSTRUCTORTOTABLE_TEMPLATE_FUNC()
  %template( TConstructorToTableCounter_functionObject ) Foam::TConstructorToTableCounter< Foam::functionObject >;
  __FUNCTIONOBJECT_CONSTRUCTORTOTABLE_TEMPLATE_FUNC__( 0 );
//  __FUNCTIONOBJECT_CONSTRUCTORTOTABLE_TEMPLATE_FUNC__( 1 );
//  __FUNCTIONOBJECT_CONSTRUCTORTOTABLE_TEMPLATE_FUNC__( 2 );
//  __FUNCTIONOBJECT_CONSTRUCTORTOTABLE_TEMPLATE_FUNC__( 3 );
//  __FUNCTIONOBJECT_CONSTRUCTORTOTABLE_TEMPLATE_FUNC__( 4 );
//  __FUNCTIONOBJECT_CONSTRUCTORTOTABLE_TEMPLATE_FUNC__( 5 );
//  __FUNCTIONOBJECT_CONSTRUCTORTOTABLE_TEMPLATE_FUNC__( 6 );
//  __FUNCTIONOBJECT_CONSTRUCTORTOTABLE_TEMPLATE_FUNC__( 7 );
%enddef

FUNCTIONOBJECT_CONSTRUCTORTOTABLE_TEMPLATE_FUNC();


//---------------------------------------------------------------------------
%import "Foam/src/OpenFOAM/fields/tmp/autoPtr.cxx"

AUTOPTR_TYPEMAP( Foam::functionObject );

// %ignore Foam::autoPtr< Foam::IOdictionary >::operator->;

%template( autoPtr_functionObject ) Foam::autoPtr< Foam::functionObject >;


//---------------------------------------------------------------------------
#endif

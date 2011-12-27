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
#ifndef IOdictionary_cxx
#define IOdictionary_cxx


//---------------------------------------------------------------------------
%module( directors="1", allprotected="1" ) "Foam.src.OpenFOAM.db.IOdictionary";
%{
  #include "Foam/src/OpenFOAM/db/IOdictionary.hh"
%}

%import "Foam/src/director.hxx"


//---------------------------------------------------------------------------
%import "Foam/src/OpenFOAM/db/regIOobject.cxx"

%import "Foam/src/OpenFOAM/db/dictionary/dictionary.cxx"

%import "Foam/src/OpenFOAM/db/objectRegistry.cxx"


//---------------------------------------------------------------------------
%feature( "director" ) IOdictionary;

DIRECTOR_PRE_EXTENDS( IOdictionary );

%include <IOdictionary.H>

%extend Foam::IOdictionary
{
  DIRECTOR_EXTENDS( IOdictionary );
}

BAREPTR_TYPEMAP( Foam::IOdictionary );


//---------------------------------------------------------------------------
%include "Foam/ext/common/OpenFOAM/managedFlu/IOdictionaryHolder.cpp"


//---------------------------------------------------------------------------
#endif

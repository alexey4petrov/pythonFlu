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
#ifndef HashTable_cxx
#define HashTable_cxx


//---------------------------------------------------------------------------
%module "Foam.src.OpenFOAM.containers.HashTables.HashTable.HashTable";
%{
  #include "Foam/src/OpenFOAM/containers/HashTables/HashTable/HashTable.hh"
%}


//---------------------------------------------------------------------------
%import "Foam/src/OpenFOAM/db/typeInfo/className.hxx"

%import "Foam/src/OpenFOAM/primitives/strings/string.cxx"

%import "Foam/src/OpenFOAM/primitives/strings/word.cxx"

%import "Foam/src/iterators.cxx"

%include <HashTable.H>


//---------------------------------------------------------------------------
%define __HASHTABLE_ADDONS__( TValue, TKey, THash )
{
  int __len__()
  {
    return self->size();
  }
  
  TValue __getitem__( const TKey& key )
  {
    return self->operator[]( key );
  }
  
  TContainer_iterator< Foam::HashTable< TValue, TKey, THash > >* __iter__()
  {
    return new TContainer_iterator< Foam::HashTable< TValue, TKey, THash > >( *self );
  }
}
%enddef

%define HASHTABLE_ADDONS( TValue, TKey, THash )
  %extend Foam::HashTable< TValue, TKey, THash > __HASHTABLE_ADDONS__( TValue, TKey, THash )
  %extend Foam::HashTable< TValue, TKey, THash > COMMON_EXTENDS;
%enddef


//---------------------------------------------------------------------------
#endif


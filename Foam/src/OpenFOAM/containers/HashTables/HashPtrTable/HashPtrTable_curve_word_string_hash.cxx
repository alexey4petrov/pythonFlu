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
#ifndef HashPtrTable_curve_word_string_hash_cxx
#define HashPtrTable_curve_word_string_hash_cxx


//---------------------------------------------------------------------------
%module "Foam.src.OpenFOAM.containers.HashTables.HashPtrTable.HashPtrTable_curve_word_string_hash"
%{
  #include "Foam/src/OpenFOAM/containers/HashTables/HashPtrTable/HashPtrTable_curve_word_string_hash.hh"
%}


//---------------------------------------------------------------------------
%import "Foam/src/OpenFOAM/containers/HashTables/HashPtrTable/HashPtrTable.cxx"

%import "Foam/src/OpenFOAM/containers/HashTables/HashTable/HashTable_curve_word_string_hash.cxx"

%ignore Foam::HashPtrTable< Foam::curve, Foam::word, Foam::string_hash >::HashPtrTable;

%template( HashPtrTable_curve_word_string_hash ) Foam::HashPtrTable< Foam::curve, Foam::word, Foam::string_hash >; 

%template( TPtrContainer_word_curve ) Foam::TPtrContainer_iterator< Foam::HashPtrTable< Foam::curve, Foam::word, Foam::string_hash > >;

HASHPTRTABLE_ADDONS( Foam::curve, Foam::word, Foam::string_hash );


//---------------------------------------------------------------------------
%typemap( typecheck ) const Foam::HashPtrTable< Foam::curve > &
{
  void *ptr;
  int res = SWIG_ConvertPtr( $input, (void **) &ptr, $descriptor( Foam::HashPtrTable< Foam::curve, Foam::word, Foam::string_hash >* ), 0 );
  $1 = SWIG_CheckState( res );
}

%typemap( in ) const Foam::HashPtrTable< Foam::curve > &
{
  void *ptr;
  int res = SWIG_ConvertPtr( $input, (void **) &ptr, $descriptor( Foam::HashPtrTable< Foam::curve, Foam::word, Foam::string_hash >* ), 0 );
  if ( SWIG_IsOK( res ) ) {
    $1 = reinterpret_cast< $1_ltype >( ptr );
  } else {
      %argument_fail( res, "$type", $symname, $argnum ); 
  }
}


//---------------------------------------------------------------------------
#endif

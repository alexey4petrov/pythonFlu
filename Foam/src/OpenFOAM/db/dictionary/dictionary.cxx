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
#ifndef dictionary_cxx
#define dictionary_cxx


//---------------------------------------------------------------------------
%module "Foam.src.OpenFOAM.db.dictionary.dictionary";
%{
   #include "Foam/src/OpenFOAM/db/dictionary/dictionary.hh"
%}


//---------------------------------------------------------------------------
%import "Foam/src/OpenFOAM/containers/LinkedLists/user/IDLList/entryIDLList.cxx"

%import "Foam/src/OpenFOAM/db/typeInfo/className.hxx"

%import "Foam/src/OpenFOAM/primitives/strings/word.cxx"

%import "Foam/src/OpenFOAM/primitives/Lists/tokenList.cxx"

%import "Foam/src/OpenFOAM/dimensionedTypes/dimensionedScalar.cxx"

%import "Foam/src/OpenFOAM/primitives/strings/string.cxx"

%import "Foam/src/OpenFOAM/primitives/scalar.cxx"

%import "Foam/src/OpenFOAM/db/Switch.cxx"


//---------------------------------------------------------------------------
%inline
{
  namespace Foam
  {
    template < class Type >
    struct TreadIfPresent
    {
      bool m_resBool;
      Type m_resType;
      
      TreadIfPresent()
      {} 
      
      TreadIfPresent( bool the_resBool, Type the_resType )
        : m_resBool( the_resBool )
        , m_resType( the_resType )
      {}
    };
  }
}

%template ( TreadIfPresent_bool_int )  Foam::TreadIfPresent< int >;

%template ( TreadIfPresent_bool_scalar )  Foam::TreadIfPresent< Foam::scalar >;


//---------------------------------------------------------------------------
%include <dictionary.H>

%extend Foam::dictionary COMMON_EXTENDS;


//---------------------------------------------------------------------------
%feature( "pythonappend" ) Foam::dictionary::readIfPresent
{
  try:
      result = val.m_resBool, val.m_resType
      pass
  except AttributeError:
      result = val
      pass
  
  return result
}


//---------------------------------------------------------------------------
%extend Foam::dictionary
{
  void add( const Foam::word& keyword, const Foam::dimensionedScalar& value )
  {
    self->add< dimensionedScalar >( keyword, value );
  }
  void add( const Foam::word& keyword, const Foam::tokenList& value )
  {
    self->add< Foam::tokenList >( keyword, value );
  }

  void add( const Foam::word& keyword, const Foam::ITstream& value )
  {
    self->add< Foam::ITstream >( keyword, value );
  }
  
  ISINSTANCE_EXTEND( Foam::dictionary ) 

#if FOAM_VERSION( ==, 010500 )
  void add( const Foam::word& keyword, const Foam::word& value, bool overwrite = false )
  {
    self->add( keyword, value, overwrite );
  }
  void add( const Foam::word& keyword, const Foam::string& value, bool overwrite = false )
  {
    self->add( keyword, value, overwrite );
  }
  void add( const Foam::word& keyword, const Foam::label& value, bool overwrite = false )
  {
    self->add( keyword, value, overwrite );
  }
  void add( const Foam::word& keyword, const Foam::scalar& value, bool overwrite = false )
  {
    self->add( keyword, value, overwrite );
  }
  void add( const Foam::word& keyword, const Foam::dictionary& value, bool overwrite = false )
  {
    self->add( keyword, value, overwrite );
  }
  Foam::TreadIfPresent< int > readIfPresent( 
    const Foam::word& k
    , int val
    , bool recursive = false
    , bool patternMatch = true ) const
  {
    bool the_resBool =  self->readIfPresent( k, val, recursive, patternMatch );
    
    return Foam::TreadIfPresent< int >( the_resBool, val );
  }
  Foam::TreadIfPresent< Foam::scalar > readIfPresent( 
    const Foam::word& k
    , Foam::scalar val
    , bool recursive = false
    , bool patternMatch = true ) const
  {
    bool the_resBool =  self->readIfPresent( k, val, recursive, patternMatch );
    
    return Foam::TreadIfPresent< Foam::scalar >( the_resBool, val );
  }
  Foam::scalar lookupOrDefault( const Foam::word& keyword, const Foam::scalar& deflt, bool recursive = false) const
  {
    return self->lookupOrDefault( keyword, deflt, recursive ) ;
  }
  int lookupOrDefault( const Foam::word& keyword, const int& deflt, bool recursive = false ) const
  {
    return self->lookupOrDefault( keyword, deflt, recursive ) ;
  }
  Foam::Switch lookupOrDefault( const Foam::word& keyword, const Foam::Switch& deflt, bool recursive = false ) const
  {
    return self->lookupOrDefault( keyword, deflt, recursive ) ;
  }
#endif


//-----------------------------------------------------------------------------------------------
#if FOAM_VERSION( >=, 010600 )
  void add( const Foam::word& keyword, const Foam::word& value, bool overwrite = false )
  {
    self->add( keyword, value, overwrite );
  }
  void add( const Foam::word& keyword, const Foam::string& value, bool overwrite = false )
  {
    self->add( keyword, value, overwrite );
  }
  void add( const Foam::word& keyword, const Foam::label& value, bool overwrite = false )
  {
    self->add( keyword, value, overwrite );
  }
  void add( const Foam::word& keyword, const Foam::scalar& value, bool overwrite = false )
  {
    self->add( keyword, value, overwrite );
  }
  void add( const Foam::word& keyword, const Foam::dictionary& value, bool overwrite = false )
  {
    self->add( keyword, value, overwrite );
  }
  Foam::scalar lookupOrDefault( const Foam::word& keyword, const Foam::scalar& deflt, bool recursive = false, bool patternMatch = true ) const
  {
    return self->lookupOrDefault( keyword, deflt, recursive, patternMatch ) ;
  }
  int lookupOrDefault( const Foam::word& keyword, const int& deflt, bool recursive = false, bool patternMatch = true ) const
  {
    return self->lookupOrDefault( keyword, deflt, recursive, patternMatch ) ;
  }
  Foam::Switch lookupOrDefault( const Foam::word& keyword, const Foam::Switch& deflt, bool recursive = false, bool patternMatch = true ) const
  {
    return self->lookupOrDefault( keyword, deflt, recursive, patternMatch ) ;
  }
  Foam::TreadIfPresent< int > readIfPresent( 
    const Foam::word& k
    , int val
    , bool recursive = false
    , bool patternMatch = true ) const
  {
    bool the_resBool =  self->readIfPresent( k, val, recursive, patternMatch );
    
    return Foam::TreadIfPresent< int >( the_resBool, val );
  }
  Foam::TreadIfPresent< Foam::scalar > readIfPresent( 
    const Foam::word& k
    , Foam::scalar val
    , bool recursive = false
    , bool patternMatch = true ) const
  {
    bool the_resBool =  self->readIfPresent( k, val, recursive, patternMatch );
    
    return Foam::TreadIfPresent< Foam::scalar >( the_resBool, val );
  }
#endif

#if FOAM_VERSION( >=, 020000 )
  bool readIfPresent( const Foam::word& k, Foam::word& the_word, bool recursive = false, bool patternMatch = true ) const
  {
    return self->readIfPresent( k, the_word, recursive, patternMatch );
  }
#endif

}


//---------------------------------------------------------------------------
//clear "pythonappend" feature
%feature( "pythonappend" ) Foam::dictionary::readIfPresent
{}

//---------------------------------------------------------------------------
%include "Foam/ext/common/OpenFOAM/managedFlu/dictionaryHolder.cpp"


//---------------------------------------------------------------------------
#endif

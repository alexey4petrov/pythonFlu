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
#ifndef dictionary_cxx
#define dictionary_cxx


//---------------------------------------------------------------------------
%include "src/OpenFOAM/containers/LinkedLists/user/IDLList/entryIDLList.cxx"

%include "src/OpenFOAM/db/typeInfo/className.hxx"

%include "src/OpenFOAM/primitives/strings/word.cxx"

%include "src/OpenFOAM/primitives/Lists/tokenList.cxx"

%include "src/OpenFOAM/dimensionedTypes/dimensionedScalar.cxx"

%include "src/OpenFOAM/primitives/strings/string.cxx"

%include "src/OpenFOAM/primitives/scalar.cxx"

%include "src/OpenFOAM/db/Switch.cxx"

%{
    #include "dictionary.H"

#if FOAM_VERSION( >=, 010600 )
    #include "SHA1Digest.H"
#endif
%}

// To use as input / output value for readIfPresent function
%apply double& INOUT { double& val }; 

%include "dictionary.H"

%extend Foam::dictionary COMMON_EXTENDS;


//---------------------------------------------------------------------------
%extend Foam::dictionary
{
  void add( const Foam::word& keyword, const Foam::dimensionedScalar& value )
  {
    self->add< dimensionedScalar >( keyword, value );
  }
  void add( const Foam::word& keyword, const Foam::tokenList& value )
  {
    self->add< tokenList >( keyword, value );
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
  bool readIfPresent( const Foam::word& k, double& val, bool recursive = false ) const
  {
    return self->readIfPresent( k, val, recursive );
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
  bool readIfPresent( const Foam::word& k, double& val, bool recursive = false, bool patternMatch = true ) const
  {
    return self->readIfPresent( k, val, recursive, patternMatch );
  }
#endif
}

// To use as input / output value for readIfPresent function
%clear double& val;


//---------------------------------------------------------------------------
#endif

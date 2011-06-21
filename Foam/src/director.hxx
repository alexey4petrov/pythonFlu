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
#ifndef director_hxx
#define director_hxx


//---------------------------------------------------------------------------
%{ 
   #include "Foam/src/director.hh"
%}


//---------------------------------------------------------------------------
%feature( "director:except" ) 
{
  if ( $error != NULL ) {
    PyErr_Print();
    Foam::error::printStack( Foam::Info );
    Swig::DirectorMethodException::raise("Error detected when calling director's method");
  }
}


//---------------------------------------------------------------------------
%define DIRECTOR_EXTENDS( Typename )
  static const Foam::Typename&
  ext_lookupObject( const Foam::objectRegistry& theRegistry, const Foam::word& theName )
  {
    const Foam::Typename& res = theRegistry.lookupObject< Foam::Typename >( theName );
    
    if ( const SwigDirector_##Typename* director = dynamic_cast< const SwigDirector_##Typename* >( &res ) )
      return *director;

    return res;
  }
%enddef


//--------------------------------------------------------------------------
%define DIRECTOR_PRE_EXTENDS( Typename )

%{
   #include DIRECTOR_INCLUDE
%}

%typemap( out ) Foam::Typename&
{
  if ( Swig::Director *director = SWIG_DIRECTOR_CAST( $1 ) ) {
    $result = director->swig_get_self();
    Py_INCREF( $result );
  } else {
    $result = SWIG_NewPointerObj( SWIG_as_voidptr( $1 ), $1_descriptor, 0 |  0 );
  }
}

%enddef


//--------------------------------------------------------------------------
#endif

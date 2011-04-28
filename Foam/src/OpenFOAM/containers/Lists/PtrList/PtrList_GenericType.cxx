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
#ifndef PtrList_GenericType_cxx
#define PtrList_GenericType_cxx


//---------------------------------------------------------------------------
%module( directors="1", allprotected="1" ) "Foam.src.OpenFOAM.containers.Lists.PtrList.PtrList_GenericType";
%{
   #include "src/OpenFOAM/containers/Lists/PtrList/PtrList_GenericType.hh"
%}

%import "src/director.hxx"


//---------------------------------------------------------------------------
%import "src/OpenFOAM/fields/tmp/autoPtr.cxx"

%import "src/OpenFOAM/primitives/direction.cxx"

%import "src/OpenFOAM/primitives/label.cxx"

%import "src/OpenFOAM/primitives/scalar.cxx"

%import "src/redirect2base.hxx"


//---------------------------------------------------------------------------
%feature( "director" ) PtrList_TypeBase;
%feature( "director" ) PtrList_TypeHolder;

BAREPTR_TYPEMAP( Foam::PtrList_TypeBase );

%include "src/OpenFOAM/containers/Lists/PtrList/PtrList_GenericType.hh"


//---------------------------------------------------------------------------
%feature( "pythonappend" ) Foam::PtrList_TypeHolder::REDIRECT2BASE_PYAPPEND_GETATTR( PtrList_TypeHolder );

%extend Foam::PtrList_TypeHolder
{
  REDIRECT2BASE_EXTEND_ATTR( PtrList_TypeHolder );
}


//---------------------------------------------------------------------------
%typecheck( SWIG_TYPECHECK_POINTER ) Foam::PtrList_TypeHolder * 
{
  void *ptr;
  int check = 0;
  int check1 = 0;
  check = SWIG_ConvertPtr( $input, &ptr, $descriptor( Foam::PtrList_TypeHolder * ), 0 );
  check1 = SWIG_ConvertPtr( $input, &ptr, $descriptor( Foam::PtrList_TypeBase * ), 0 );
  
  $1 = SWIG_IsOK( check ) || SWIG_IsOK( check1 ); 
}

%typemap( in ) Foam::PtrList_TypeHolder* ( void  *argp = 0, int check = 0, Foam::PtrList_TypeHolder* result ) 
{
  check = SWIG_ConvertPtr( $input, &argp, $descriptor( Foam::PtrList_TypeHolder * ), SWIG_POINTER_DISOWN | %convertptr_flags );
  if ( SWIG_IsOK( check ) && argp ) {
    result = %reinterpret_cast( argp, Foam::PtrList_TypeHolder * );
    // "Director" derived classes need special care
    if ( Swig::Director *director = SWIG_DIRECTOR_CAST( result ) ) {
      PyObject_CallMethod( director->swig_get_self(), (char *) "__disown__", NULL );
    }
  } else {
    check = SWIG_ConvertPtr( $input, &argp, $descriptor( Foam::PtrList_TypeBase * ), SWIG_POINTER_DISOWN | %convertptr_flags );
    if ( SWIG_IsOK( check ) && argp ) {
      Foam::PtrList_TypeBase * tmp = %reinterpret_cast( argp, Foam::PtrList_TypeBase * );
      if ( Swig::Director *director = SWIG_DIRECTOR_CAST( tmp ) ) {
        PyObject_CallMethod( director->swig_get_self(), (char *) "__disown__", NULL );
      }
      result = new Foam::PtrList_TypeHolder( tmp );
    }
  }
  $1 = result;
}


//---------------------------------------------------------------------------
AUTOPTR_TYPEMAP( Foam::PtrList_TypeHolder )

%template (autoPtr_PtrList_TypeHolder) Foam::autoPtr< Foam::PtrList_TypeHolder >;


//---------------------------------------------------------------------------
#endif


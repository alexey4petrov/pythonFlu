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
#ifndef PtrList_GenericINew_cxx
#define PtrList_GenericINew_cxx


//---------------------------------------------------------------------------
%module( directors="1", allprotected="1" ) "Foam.src.OpenFOAM.containers.Lists.PtrList.PtrList_GenericINew";
%{
   #include "src/OpenFOAM/containers/Lists/PtrList/PtrList_GenericINew.hpp"
%}

// Keep on corresponding "director" includes at the top of SWIG defintion file
%include "src/OpenFOAM/directors.hxx"


//---------------------------------------------------------------------------
%import "src/OpenFOAM/fields/tmp/autoPtr.cxx"

%import "src/OpenFOAM/containers/Lists/PtrList/PtrList_GenericType.cxx"

%feature( "director" ) PtrList_INewBase;
%feature( "director" ) PtrList_INewHolder;

%include "src/OpenFOAM/containers/Lists/PtrList/PtrList_GenericINew.hpp" 


%typecheck( SWIG_TYPECHECK_POINTER ) const Foam::PtrList_INewHolder&
{
  void *ptr;
  int check = 0;
  int check1 = 0;
  check = SWIG_ConvertPtr( $input, &ptr, $descriptor( Foam::PtrList_INewHolder* ), 0 );
  check1 = SWIG_ConvertPtr( $input, &ptr, $descriptor( Foam::PtrList_INewBase* ), 0 );
  $1 = SWIG_IsOK( check ) || SWIG_IsOK( check1 ); 
}

%typemap( in ) const Foam::PtrList_INewHolder&
{
  void  *argp = 0;
  int res = 0;
  
  res = SWIG_ConvertPtr( $input, &argp, $descriptor(  Foam::PtrList_INewHolder* ), %convertptr_flags );
  if ( SWIG_IsOK( res )&& argp  ){
    $1 = %reinterpret_cast( argp, Foam::PtrList_INewHolder* );
  } else {
    res = SWIG_ConvertPtr( $input, &argp, $descriptor( Foam::PtrList_INewBase* ), %convertptr_flags );
    if ( SWIG_IsOK( res ) && argp ) {
      Foam::PtrList_INewBase* tmp =%reinterpret_cast( argp, Foam::PtrList_INewBase * );
      $1 = new Foam::PtrList_INewHolder( tmp );
    } else {
      %argument_fail( res, "$type", $symname, $argnum );
    }
  }
} 


//---------------------------------------------------------------------------
#endif


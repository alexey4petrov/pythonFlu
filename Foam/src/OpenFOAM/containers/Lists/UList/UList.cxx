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
#ifndef UList_cxx
#define UList_cxx


//---------------------------------------------------------------------------
%module "Foam.src.OpenFOAM.containers.Lists.UList.UList";
%{
   #include "Foam/src/OpenFOAM/containers/Lists/UList/UList.hh"
%}


//---------------------------------------------------------------------------
%import "Foam/src/common.hxx"

%import "Foam/src/iterators.cxx"

%import "Foam/src/OpenFOAM/primitives/label.cxx"

%include <UList.H>


//---------------------------------------------------------------------------
%define SEQUENCE_ADDONS( TItem )
{
  int __len__()
  {
    return get_ref( self ).size();
  }
  
  TItem __getitem__( const Foam::label theIndex )
  {
    return get_ref( self )[ theIndex ];
  }

  void __setitem__( const Foam::label theIndex, TItem theValue )
  {
    get_ref( self )[ theIndex ] = theValue;
  }

  TContainer_iterator< UList< TItem > >* __iter__()
  {
    return new TContainer_iterator< UList< TItem > >( get_ref( self ) );
  }
}
%enddef


//---------------------------------------------------------------------------
%define LISTS_FUNCS( TItem )
{
#if FOAM_VERSION( <, 010600 )
  Foam::label ext_findIndex( TItem& t )
  {
    return Foam::findIndex( get_ref( self ), t );
  }
#endif

#if FOAM_VERSION( >=, 010600 ) 
  Foam::label ext_findIndex( TItem& t, const label start=0 )
  {
    return Foam::findIndex( get_ref( self ), t, start );
  }
#endif
}  
%enddef


//----------------------------------------------------------------------------
%define ULISTBASED_ADDONS( TItem )
  %extend Foam::UList< TItem > SEQUENCE_ADDONS( TItem )

  %extend Foam::UList< TItem > LISTS_FUNCS( TItem )
%enddef


//---------------------------------------------------------------------------
%define ULIST_TYPEMAP( Type )

%typecheck( SWIG_TYPECHECK_POINTER ) const Foam::UList< Foam::Type >& 
{
  void *ptr;
  int resT = SWIG_ConvertPtr( $input, (void **) &ptr, $descriptor( Foam::UList< Foam::Type > * ), 0 );
  int res_tmpField = SWIG_ConvertPtr( $input, (void **) &ptr, $descriptor( Foam::tmp< Foam::Field< Foam::Type > > * ), 0 );
  $1 = SWIG_CheckState( resT ) || SWIG_CheckState( res_tmpField );
}

%typemap( in ) const Foam::UList< Foam::Type >& 
{
  void  *argp = 0;
  int res = 0;
  
  res = SWIG_ConvertPtr( $input, &argp, $descriptor(  Foam::UList< Foam::Type > * ), %convertptr_flags );
  if ( SWIG_IsOK( res )&& argp  ){
    Foam::UList< Foam::Type > * res = %reinterpret_cast( argp, Foam::UList< Foam::Type >* );
    $1 = res;
  } else {
    res = SWIG_ConvertPtr( $input, &argp, $descriptor( Foam::tmp< Foam::Field< Foam::Type > >* ), %convertptr_flags );
    if ( SWIG_IsOK( res ) && argp ) {
      Foam::tmp< Foam::Field< Foam::Type > >* tmp_res = %reinterpret_cast( argp, Foam::tmp< Foam::Field< Foam::Type > > * );
      $1 = tmp_res->operator->();
      } else {
        %argument_fail( res, "$type", $symname, $argnum );
        }
    }
}    
%enddef


//---------------------------------------------------------------------------
#endif

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
#ifndef smart_tmp_hxx
#define smart_tmp_hxx


//---------------------------------------------------------------------------
%import "Foam/src/common.hxx"

%import "Foam/src/OpenFOAM/fields/tmp/smartPtr_extend.hxx"

%include <smart_tmp/smart_tmp.hpp>


//---------------------------------------------------------------------------
%define SMART_TMP_VALID_EXTEND( Type )

%extend Foam::smart_tmp< Type >
{
  bool valid() const
  {
     return ! self->empty();
  }
}

%enddef


//---------------------------------------------------------------------------
%define SMART_TMP_VALID_EXTEND_TEMPLATE1( Template, Type )

%extend Foam::smart_tmp< Template< Type > >
{
  bool valid() const
  {
     return ! self->empty();
  }
}

%enddef


//---------------------------------------------------------------------------
%define SMART_TMP_VALID_EXTEND_TEMPLATE3( Template, Type1, Type2, Type3 )

%extend Foam::smart_tmp< Template< Type1, Type2, Type3 > >
{
  bool valid() const
  {
     return ! self->empty();
  }
}

%enddef


//---------------------------------------------------------------------------
%define SMART_TMP_TYPEMAP_TEMPLATE1( Template, Type )

%typecheck( SWIG_TYPECHECK_POINTER ) const Foam::smart_tmp< Template< Type > >& 
{
  void *ptr;
  int res_smartTmpT = SWIG_ConvertPtr( $input, (void **) &ptr, $descriptor( Foam::smart_tmp< Template< Type > > * ), 0 );
  int res_T = SWIG_ConvertPtr( $input, (void **) &ptr, $descriptor( Template< Type > * ), 0 );
  int res_tmpT = SWIG_ConvertPtr( $input, (void **) &ptr, $descriptor( Foam::tmp< Template< Type > > * ), 0 );
  $1 = SWIG_CheckState( res_smartTmpT ) || SWIG_CheckState( res_T ) || SWIG_CheckState( res_tmpT );
}

%typemap( in ) const Foam::smart_tmp< Template< Type > >& ( void  *argp = 0, int check = 0, Foam::smart_tmp< Template< Type > > result ) 
{
  // First check the simplest case, complete coinsidence of the types
  check = SWIG_ConvertPtr( $input, &argp, $descriptor( Foam::smart_tmp< Template< Type > > * ), %convertptr_flags );
  if ( SWIG_IsOK( check ) && argp ) {
    result = *%reinterpret_cast( argp, Foam::smart_tmp< Template< Type > > * );
  } else {
    check = SWIG_ConvertPtr( $input, &argp, $descriptor( Template< Type > * ), SWIG_POINTER_DISOWN | %convertptr_flags );
    if ( SWIG_IsOK( check ) && argp ) {
      Template< Type >* arg = %reinterpret_cast( argp, Template< Type > * );
      result = Foam::smart_tmp< Template< Type > >( arg );
    } else {
       check = SWIG_ConvertPtr( $input, &argp, $descriptor( Foam::tmp< Template< Type > > * ), SWIG_POINTER_DISOWN | %convertptr_flags );
       if ( SWIG_IsOK( check ) && argp ) {
         Foam::tmp< Template< Type > >* arg = %reinterpret_cast( argp, Foam::tmp< Template< Type > > * );
         result = Foam::smart_tmp< Template< Type > >( *arg );
       } else {
         %argument_fail( check, "$type", $symname, $argnum ); 
       }
    }
  }
  $1 = &result;
}

%enddef

//---------------------------------------------------------------------------
%define SMART_TMP_TYPEMAP_TEMPLATE3( Template, Type1, Type2, Type3 )

%typecheck( SWIG_TYPECHECK_POINTER ) const Foam::smart_tmp< Template< Type1, Type2, Type3 > >& 
{
  void *ptr;
  int res_smartTmpT = SWIG_ConvertPtr( $input, (void **) &ptr, $descriptor( Foam::smart_tmp< Template< Type1, Type2, Type3 > > * ), 0 );
  int res_T = SWIG_ConvertPtr( $input, (void **) &ptr, $descriptor( Template< Type1, Type2, Type3 > * ), 0 );
  int res_tmpT = SWIG_ConvertPtr( $input, (void **) &ptr, $descriptor( Foam::tmp< Template< Type1, Type2, Type3 > > * ), 0 );
  $1 = SWIG_CheckState( res_smartTmpT ) || SWIG_CheckState( res_T ) || SWIG_CheckState( res_tmpT );
}

%typemap( in ) const Foam::smart_tmp< Template< Type1, Type2, Type3 > >& ( void  *argp = 0, int check = 0, Foam::smart_tmp< Template< Type1, Type2, Type3 > > result ) 
{
  // First check the simplest case, complete coinsidence of the types
  check = SWIG_ConvertPtr( $input, &argp, $descriptor( Foam::smart_tmp< Template< Type1, Type2, Type3 > > * ), %convertptr_flags );
  if ( SWIG_IsOK( check ) && argp ) {
    result = *%reinterpret_cast( argp, Foam::smart_tmp< Template< Type1, Type2, Type3 > > * );
  } else {
    check = SWIG_ConvertPtr( $input, &argp, $descriptor( Template< Type1, Type2, Type3 > * ), SWIG_POINTER_DISOWN | %convertptr_flags );
    if ( SWIG_IsOK( check ) && argp ) {
      Template< Type1, Type2, Type3 >* arg = %reinterpret_cast( argp, Template< Type1, Type2, Type3 > * );
      result = Foam::smart_tmp< Template< Type1, Type2, Type3 > >( arg );
    } else {
       check = SWIG_ConvertPtr( $input, &argp, $descriptor( Foam::tmp< Template< Type1, Type2, Type3 > > * ), SWIG_POINTER_DISOWN | %convertptr_flags );
       if ( SWIG_IsOK( check ) && argp ) {
         Foam::tmp< Template< Type1, Type2, Type3 > >* arg = %reinterpret_cast( argp, Foam::tmp< Template< Type1, Type2, Type3 > > * );
         result = Foam::smart_tmp< Template< Type1, Type2, Type3 > >( *arg );
       } else {
         %argument_fail( check, "$type", $symname, $argnum ); 
       }
    }
  }
  $1 = &result;
}

%enddef

//---------------------------------------------------------------------------
#endif

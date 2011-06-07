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
#ifndef bareptr_typemap_hxx
#define bareptr_typemap_hxx


//---------------------------------------------------------------------------
%define BAREPTR_TYPEMAP( Type )

%typecheck( SWIG_TYPECHECK_POINTER ) Type* 
{
    void *ptr;
    int check = 0;
    check = SWIG_ConvertPtr( $input, &ptr, $descriptor( Type * ), 0 );
    $1 = SWIG_IsOK( check ); 
}

%typemap( in ) Type* ( void  *argp = 0, int check = 0, Type* result ) 
{
  check = SWIG_ConvertPtr( $input, &argp, $descriptor( Type * ), SWIG_POINTER_DISOWN | %convertptr_flags );
  if ( SWIG_IsOK( check ) && argp ) {
    result = %reinterpret_cast( argp, Type * );
    // "Director" derived classes need special care
    if ( Swig::Director *director = SWIG_DIRECTOR_CAST( result ) ) {
      PyObject_CallMethod( director->swig_get_self(), (char *) "__disown__", NULL );
    }
  }
  $1 = result;
}

%enddef


//---------------------------------------------------------------------------
%define BAREPTR_TYPEMAP_TEMPLATE_1( Template, Type )

%typecheck( SWIG_TYPECHECK_POINTER ) Template< Type >* 
{
    void *ptr;
    int check = 0;
    check = SWIG_ConvertPtr( $input, &ptr, $descriptor( Template< Type > * ), 0 );
    $1 = SWIG_IsOK( check ); 
}

%typemap( in ) Template< Type >* ( void  *argp = 0, int check = 0, Template< Type >* result ) 
{
  check = SWIG_ConvertPtr( $input, &argp, $descriptor( Template< Type >* ), SWIG_POINTER_DISOWN | %convertptr_flags );
  if ( SWIG_IsOK( check ) && argp ) {
    result = %reinterpret_cast( argp, Template< Type > * );
    // "Director" derived classes need special care
    if ( Swig::Director *director = SWIG_DIRECTOR_CAST( result ) ) {
      PyObject_CallMethod( director->swig_get_self(), (char *) "__disown__", NULL );
    }
  }
  $1 = result;
}

%enddef


//---------------------------------------------------------------------------
%define BAREPTR_TYPEMAP_TEMPLATE_2( Template, Type1, Type2 )

%typecheck( SWIG_TYPECHECK_POINTER ) Template< Type1, Type2 >* 
{
    void *ptr;
    int check = 0;
    check = SWIG_ConvertPtr( $input, &ptr, $descriptor( Template< Type1, Type2 > * ), 0 );
    $1 = SWIG_IsOK( check ); 
}

%typemap( in ) Template< Type1, Type2 >* ( void  *argp = 0, int check = 0, Template< Type1, Type2 >* result ) 
{
  check = SWIG_ConvertPtr( $input, &argp, $descriptor( Template< Type1, Type2 >* ), SWIG_POINTER_DISOWN | %convertptr_flags );
  if ( SWIG_IsOK( check ) && argp ) {
    result = %reinterpret_cast( argp, Template< Type1, Type2 > * );
    // "Director" derived classes need special care
    if ( Swig::Director *director = SWIG_DIRECTOR_CAST( result ) ) {
      PyObject_CallMethod( director->swig_get_self(), (char *) "__disown__", NULL );
    }
  }
  $1 = result;
}

%enddef


//---------------------------------------------------------------------------
%define BAREPTR_TYPEMAP_TEMPLATE_3( Template, Type1, Type2, Type3 )

%typecheck( SWIG_TYPECHECK_POINTER ) Template< Type1, Type2, Type3 >* 
{
    void *ptr;
    int check = 0;
    check = SWIG_ConvertPtr( $input, &ptr, $descriptor( Template< Type1, Type2, Type3 > * ), 0 );
    $1 = SWIG_IsOK( check ); 
}

%typemap( in ) Template< Type1, Type2, Type3 >* ( void  *argp = 0, int check = 0, Template< Type1, Type2, Type3 >* result ) 
{
  check = SWIG_ConvertPtr( $input, &argp, $descriptor( Template< Type1, Type2, Type3 >* ), SWIG_POINTER_DISOWN | %convertptr_flags );
  if ( SWIG_IsOK( check ) && argp ) {
    result = %reinterpret_cast( argp, Template< Type1, Type2, Type3 > * );
    // "Director" derived classes need special care
    if ( Swig::Director *director = SWIG_DIRECTOR_CAST( result ) ) {
      PyObject_CallMethod( director->swig_get_self(), (char *) "__disown__", NULL );
    }
  }
  $1 = result;
}

%enddef


//---------------------------------------------------------------------------
#endif


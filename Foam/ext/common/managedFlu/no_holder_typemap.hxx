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
//  Author : Alexey PETROV, Andrey SIMURZIN


//---------------------------------------------------------------------------
#ifndef no_holder_typemap_hxx
#define no_holder_typemap_hxx


//---------------------------------------------------------------------------
%define NO_HOLDER_TYPEMAP( Type )

%typecheck( SWIG_TYPECHECK_POINTER ) Type&
{
  void *ptr;
  int res = SWIG_ConvertPtr( $input, (void **) &ptr, $descriptor( Type * ), 0 );
  int resHolder = SWIG_ConvertPtr( $input, (void **) &ptr, $descriptor( Type##Holder * ), 0 );
  $1 = SWIG_CheckState( res ) || SWIG_CheckState( resHolder );
}

%typemap( in ) Type& 
{
  void  *argp = 0;
  int res = 0;
  
  res = SWIG_ConvertPtr( $input, &argp, $descriptor(  Type * ), %convertptr_flags );
  if ( SWIG_IsOK( res )&& argp  ){
    Type * res = %reinterpret_cast( argp, Type * );
    $1 = res;
  } else {
    res = SWIG_ConvertPtr( $input, &argp, $descriptor( Type##Holder * ), %convertptr_flags );
    if ( SWIG_IsOK( res ) && argp ) {
      Type##Holder* tmp_res = %reinterpret_cast( argp, Type##Holder * );
      $1 = tmp_res->operator->();
    } else {
      %argument_fail( res, "$type", $symname, $argnum );
    }
  }
}

%enddef


//---------------------------------------------------------------------------
#endif


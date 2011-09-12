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
#ifndef Deps_cxx
#define Deps_cxx


//---------------------------------------------------------------------------
%module "Foam.ext.common.managedFlu.Deps"

%{
  #include "Foam/ext/common/managedFlu/Deps.hh"
%}

%import "Foam/ext/common/managedFlu/Args.cxx"


//---------------------------------------------------------------------------
%typecheck( SWIG_TYPECHECK_POINTER ) const Foam::Deps&
{
  void *ptr;
  int res_Deps = SWIG_ConvertPtr( $input, (void **) &ptr, $descriptor( Foam::Deps* ), 0 );
  int res_Simpl = SWIG_ConvertPtr( $input, (void **) &ptr, $descriptor( Foam::SimpleHolder * ), 0 );
  $1 = SWIG_CheckState( res_Deps ) || SWIG_CheckState( res_Simpl );
}


%typemap( in ) const Foam::Deps& ( void  *argp = 0, int check = 0, Foam::Deps result ) 
{
  // First check the simplest case, complete coinsidence of the types
  check = SWIG_ConvertPtr( $input, &argp, $descriptor( Foam::Deps * ), %convertptr_flags );
  if ( SWIG_IsOK( check ) && argp ) {
    result = *%reinterpret_cast( argp, Foam::Deps * );
  } else {
    check = SWIG_ConvertPtr( $input, &argp, $descriptor( Foam::SimpleHolder * ), %convertptr_flags );
    if ( SWIG_IsOK( check ) && argp ) {
      Foam::SimpleHolder* arg = %reinterpret_cast( argp, Foam::SimpleHolder * );
      result = Foam::Deps( arg );
    } else {
      %argument_fail( check, "$type", $symname, $argnum ); 
      }
  }
  $1 = &result;
}

//---------------------------------------------------------------------------
%include "Deps.hpp"


//--------------------------------------------------------------------------------------
#endif

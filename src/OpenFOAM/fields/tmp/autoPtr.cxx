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
#ifndef autoPtr_cxx
#define autoPtr_cxx


//---------------------------------------------------------------------------
%include "src/common.hxx"

%include "src/OpenFOAM/fields/tmp/smartPtr_extend.hxx"

%include "autoPtr.H"

%{
    #include "autoPtr.H"
%}


//---------------------------------------------------------------------------
%define AUTOPTR_TYPEMAP( Type )

%feature( "novaluewrapper" ) Foam::autoPtr< Type >;

%typemap( in ) const Foam::autoPtr< Type > & ( void  *argp = 0, int check = 0, Foam::autoPtr< Type > result ) 
{
  // First check the simplest case, complete coinsidence of the types
  check = SWIG_ConvertPtr( $input, &argp, $descriptor( Foam::autoPtr< Type > * ), %convertptr_flags );
  if ( SWIG_IsOK( check ) && argp ) {
    result = *%reinterpret_cast( argp, Foam::autoPtr< Type > * );
  } else {
    check = SWIG_ConvertPtr( $input, &argp, $descriptor( Type * ), SWIG_POINTER_DISOWN | %convertptr_flags );
    if ( SWIG_IsOK( check ) && argp ) {
      Type* arg = %reinterpret_cast( argp, Type * );
      // "Director" derived classes need special care
      if ( Swig::Director *director = SWIG_DIRECTOR_CAST( arg ) ) {
	PyObject_CallMethod( director->swig_get_self(), (char *) "__disown__", NULL );
      }
      result.reset( arg );
    } else {
      %argument_fail( check, "$type", $symname, $argnum ); 
    }
  }
  $1 = &result;
}

%enddef


//---------------------------------------------------------------------------
#endif

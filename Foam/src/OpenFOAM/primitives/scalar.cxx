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
#ifndef scalar_cxx
#define scalar_cxx


//---------------------------------------------------------------------------
%module "Foam.src.OpenFOAM.primitives.scalar";
%{
  #include "Foam/src/OpenFOAM/primitives/scalar.hh"
%}


//---------------------------------------------------------------------------
%import "Foam/src/common.hxx"

%include <doubleScalar.H>


//---------------------------------------------------------------------------
%typecheck( SWIG_TYPECHECK_POINTER ) Foam::scalar 
{
  $1 = PyFloat_Check( $input );
}


%typemap( in ) Foam::scalar
{
  Foam::scalar aValue = PyFloat_AsDouble( $input );
  $1 = $1_basetype( aValue );
}

%typecheck( SWIG_TYPECHECK_POINTER ) const Foam::scalar&
{
  void* ptr=0;
  int res = SWIG_ConvertPtr($input, &ptr, $descriptor(  Foam::dimensioned< Foam::scalar > * ), 0 |  0 );
  if ( SWIG_IsOK( res ) && ptr )
  {
    $1 = 0;
  }
  else
  {
    $1 = PyFloat_Check( $input );
  }
}


%typemap( in ) const Foam::scalar&
{
  void  *argp = 0;
  int res = 0;
  res = SWIG_ConvertPtr( $input, &argp, $descriptor(  Foam::dimensioned< Foam::scalar > * ), %convertptr_flags );
  if ( SWIG_IsOK( res ) && argp )
  {
    %argument_fail( res, "$type", $symname, $argnum );
  } 
  Foam::scalar aValue = PyFloat_AsDouble( $input );
  $1 = new $*1_ltype( aValue );
}


//----------------------------------------------
%typemap( out ) Foam::scalar
{
  void  *argp = 0;
  int res = 0;
  $result = PyFloat_FromDouble( $1 );
}

%typemap( out ) Foam::scalar*
{
  Foam::scalar aValue = *$1;
  $result = PyFloat_FromDouble( aValue );
}


%typemap( out ) const Foam::scalar &
{
  $result = PyFloat_FromDouble( *$1 );
}

%typemap( out ) Foam::scalar &
{
  $result = PyFloat_FromDouble( *$1 );
}


//---------------------------------------------------------------------------
namespace Foam
{ 
  struct scalar{};
}

%import "Foam/src/OpenFOAM/db/IOstreams/IOstreams/Istream.cxx"

%include <scalar.H>


//---------------------------------------------------------------------------
#endif

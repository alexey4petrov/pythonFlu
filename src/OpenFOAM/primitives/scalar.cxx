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
#ifndef scalar_cxx
#define scalar_cxx


//---------------------------------------------------------------------------
%include "src/common.hxx"


//---------------------------------------------------------------------------
%{
    #include "doubleScalar.H"
%}

%include "doubleScalar.H"


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

%typecheck( SWIG_TYPECHECK_POINTER ) Foam::scalar&
{
   $1 = PyFloat_Check( $input );
}


%typemap( in ) Foam::scalar&
{
    Foam::scalar aValue = PyFloat_AsDouble( $input );
    $1 = new $1_basetype( aValue );
}


//----------------------------------------------
%typemap( out ) Foam::scalar
{
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

%{
    #include "scalar.H"
%}

%include "scalar.H"


//---------------------------------------------------------------------------
#endif

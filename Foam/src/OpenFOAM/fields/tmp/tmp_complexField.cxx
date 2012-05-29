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
#ifndef tmp_complexField_cxx
#define tmp_complexField_cxx


//---------------------------------------------------------------------------
%module "Foam.src.OpenFOAM.fields.tmp.tmp_complexField"
%{
  #include "Foam/src/OpenFOAM/fields/tmp/tmp_complexField.hh"
%}


//---------------------------------------------------------------------------
%import "Foam/src/OpenFOAM/fields/tmp/tmp.cxx"

%import "Foam/src/OpenFOAM/fields/Fields/complexFields.cxx"


//----------------------------------------------------------------------------
TMP_TYPEMAP( Foam::complexField );

%template( tmp_complexField ) Foam::tmp< Foam::Field< Foam::complex > >;

%feature( "pythonappend" ) Foam::tmp< Foam::Field< Foam::complex > >::SMARTPTR_PYAPPEND_GETATTR( tmp_complexField );

%extend Foam::tmp< Foam::Field< Foam::complex > >
{
  SMARTPTR_EXTEND_ATTR( tmp_complexField );
  SEQUENCE_ADDONS( Foam::complex );
  LISTS_FUNCS( Foam::complex );
}

%extend Foam::tmp< Foam::Field< Foam::complex > > FIELD_VIRTUAL_EXTENDS( complex );


//---------------------------------------------------------------------------
#endif

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
#ifndef smart_tmp_surfaceScalarField_cpp
#define smart_tmp_surfaceScalarField_cpp


//---------------------------------------------------------------------------
%{
  #include "Foam/ext/common/finiteVolume/smart_tmp/smart_tmp_surfaceScalarField.hh"
%}


//---------------------------------------------------------------------------
%include "Foam/ext/common/smart_tmp.hxx"

%include "Foam/src/finiteVolume/fields/surfaceFields/surfaceScalarField.cpp"


//---------------------------------------------------------------------------
%template ( smart_tmp_surfaceScalarField ) Foam::smart_tmp< Foam::GeometricField< Foam::scalar, Foam::fvsPatchField, Foam::surfaceMesh > >;

SMART_TMP_VALID_EXTEND_TEMPLATE3( Foam::GeometricField, Foam::scalar, Foam::fvsPatchField, Foam::surfaceMesh );

%extend Foam::smart_tmp< Foam::GeometricField< Foam::scalar, Foam::fvsPatchField, Foam::surfaceMesh > >
{
  SMARTPTR_EXTEND_OPERATOR_EQ( Foam::scalar );
}

SMART_TMP_TYPEMAP_TEMPLATE3( Foam::GeometricField, Foam::scalar, Foam::fvsPatchField, Foam::surfaceMesh );


//---------------------------------------------------------------------------
#endif


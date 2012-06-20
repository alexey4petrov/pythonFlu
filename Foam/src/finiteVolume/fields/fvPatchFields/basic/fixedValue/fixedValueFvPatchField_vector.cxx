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
#ifndef fixedValueFvPatchField_vector_cxx
#define fixedValueFvPatchField_vector_cxx


//---------------------------------------------------------------------------
%module "Foam.src.finiteVolume.fields.fvPatchFields.basic.fixedValue.fixedValueFvPatchField_vector";
%{
  #include "Foam/src/finiteVolume/fields/fvPatchFields/basic/fixedValue/fixedValueFvPatchField_vector.hh"
%}

%import "Foam/src/director.hxx"

//---------------------------------------------------------------------------
%import "Foam/src/OpenFOAM/fields/Fields/primitiveFields.cxx"

%import "Foam/src/finiteVolume/fields/fvPatchFields/basic/fixedValue/fixedValueFvPatchField.hxx"

%ignore Foam::fixedValueFvPatchField< Foam::vector >::valueBoundaryCoeffs;

%feature( "director" ) fixedValueFvPatchVectorField;

DIRECTOR_PRE_EXTENDS( fixedValueFvPatchVectorField );

%template( fixedValueFvPatchVectorField ) Foam::fixedValueFvPatchField< Foam::vector >;


//---------------------------------------------------------------------------
%import "Foam/src/OpenFOAM/db/objectRegistry.cxx"

%extend Foam::fixedValueFvPatchField< Foam::vector >
{
  DIRECTOR_EXTENDS( fixedValueFvPatchVectorField );
  TYPEINFO_DIRECTOR_EXTENDS( fvPatchVectorField, fixedValueFvPatchVectorField );
}

%include "Foam/src/finiteVolume/fields/fvPatchFields/basic/fixedValue/fixedValueFvPatchField_vector.hh"


//---------------------------------------------------------------------------
#endif

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
//  See http://sourceforge.net/projects/pythonflu
//
//  Author : Alexey PETROV


//---------------------------------------------------------------------------
#ifndef fixedValueFvPatchField_scalar_cxx
#define fixedValueFvPatchField_scalar_cxx


//---------------------------------------------------------------------------
%module "Foam.src.finiteVolume.fields.fvPatchFields.basic.fixedValue.fixedValueFvPatchField_scalar";
%{
  #include "src/finiteVolume/fields/fvPatchFields/basic/fixedValue/fixedValueFvPatchField_scalar.hh"
%}

%import "src/director.hxx"

//---------------------------------------------------------------------------
%import "src/OpenFOAM/fields/Fields/primitiveFields.cxx"

%import "src/finiteVolume/fields/fvPatchFields/basic/fixedValue/fixedValueFvPatchField.hxx"

%feature( "director" ) fixedValueFvPatchScalarField;

DIRECTOR_PRE_EXTENDS( fixedValueFvPatchScalarField );

%template( fixedValueFvPatchScalarField ) Foam::fixedValueFvPatchField< Foam::scalar >;


//---------------------------------------------------------------------------
%import "src/OpenFOAM/db/objectRegistry.cxx"

%extend Foam::fixedValueFvPatchField< Foam::scalar >
{
  DIRECTOR_EXTENDS( fixedValueFvPatchScalarField );
  TYPEINFO_DIRECTOR_EXTENDS( fvPatchScalarField, fixedValueFvPatchScalarField );
}

%include "src/finiteVolume/fields/fvPatchFields/basic/fixedValue/fixedValueFvPatchField_scalar.hh"


//---------------------------------------------------------------------------
#endif

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
#ifndef DimensionedField_scalar_volMesh_cpp
#define DimensionedField_scalar_volMesh_cpp


//---------------------------------------------------------------------------
%module "Foam.src.OpenFOAM.fields.DimensionedFields.DimensionedField_scalar_volMesh";
%{
  #include "Foam/src/OpenFOAM/fields/DimensionedFields/DimensionedField_scalar_volMesh.hh"
%}


//----------------------------------------------------------------------------
%include "Foam/src/OpenFOAM/fields/DimensionedFields/DimensionedField.cpp"

%import "Foam/src/OpenFOAM/fields/Fields/primitiveFields.cxx"
%import "Foam/src/finiteVolume/volMesh.hpp"

DIMENSIONED_FIELD_VOLMESH_TYPEMAP( scalar );

%ignore Foam::DimensionedField< Foam::scalar, Foam::volMesh >::typeName;
%ignore Foam::DimensionedField< Foam::scalar, Foam::volMesh >::debug;
%ignore Foam::DimensionedField< Foam::scalar, Foam::volMesh >::T;

SCALAR_DIMENSIONED_FIELD_TEMPLATE_FUNC( volMesh );

%template( DimensionedField_scalar_volMesh ) Foam::DimensionedField< Foam::scalar, Foam::volMesh >;


//---------------------------------------------------------------------------

#endif

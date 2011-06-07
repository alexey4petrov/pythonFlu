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
#ifndef GeometricField_tensor_fvPatchField_volMesh_cpp
#define GeometricField_tensor_fvPatchField_volMesh_cpp


//---------------------------------------------------------------------------
%{
  #include "src/OpenFOAM/fields/GeometricFields/GeometricField_tensor_fvPatchField_volMesh.hh"
%}


//---------------------------------------------------------------------------
%include "src/OpenFOAM/fields/FieldFields/FieldField.cpp"

%import "src/OpenFOAM/fields/tmp/refCount.cxx"

%import "src/OpenFOAM/containers/Lists/PtrList/PtrList_tensorField.cxx"

%include "src/OpenFOAM/fields/FieldFields/FieldField_fvPatchField_tensor.cpp"


//---------------------------------------------------------------------------
%include "src/OpenFOAM/fields/GeometricFields/GeometricField.cpp"

%include "src/OpenFOAM/fields/DimensionedFields/DimensionedField_tensor_volMesh.cpp"

%ignore Foam::GeometricField< Foam::tensor, Foam::fvPatchField, Foam::volMesh >::debug;
%ignore Foam::GeometricField< Foam::tensor, Foam::fvPatchField, Foam::volMesh >::typeName;
%ignore Foam::GeometricField< Foam::tensor, Foam::fvPatchField, Foam::volMesh >::boundaryField;
%ignore Foam::GeometricField< Foam::tensor, Foam::fvPatchField, Foam::volMesh >::scale;
%ignore Foam::GeometricField< Foam::tensor, Foam::fvPatchField, Foam::volMesh >::min;
%ignore Foam::GeometricField< Foam::tensor, Foam::fvPatchField, Foam::volMesh >::max;

TENSOR_GEOMETRIC_FIELD_TEMPLATE_FUNC( Foam::fvPatchField, Foam::volMesh );

%template( GeometricField_tensor_fvPatchField_volMesh ) Foam::GeometricField< Foam::tensor, Foam::fvPatchField, Foam::volMesh >;


//---------------------------------------------------------------------------
#endif

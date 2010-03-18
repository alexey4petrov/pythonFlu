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
//  See https://csrcs.pbmr.co.za/svn/nea/prototypes/reaktor/pyfoam
//
//  Author : Alexey PETROV


//---------------------------------------------------------------------------
#ifndef finiteVolume_cxx
#define finiteVolume_cxx


//---------------------------------------------------------------------------
// Keep on corresponding "director" includes at the top of SWIG defintion file

%include "src/OpenFOAM/directors.hxx"

%include "src/finiteVolume/directors.hxx"


//---------------------------------------------------------------------------
%include "src/finiteVolume/fields/surfaceFields/surfaceScalarField.cxx"
%include "src/finiteVolume/fields/surfaceFields/surfaceVectorField.cxx"

%include "src/finiteVolume/fields/volFields/volScalarField.cxx"
%include "src/finiteVolume/fields/volFields/volVectorField.cxx"
%include "src/finiteVolume/fields/volFields/volTensorField.cxx"
%include "src/finiteVolume/fields/volFields/volSymmTensorField.cxx"
%include "src/finiteVolume/fields/volFields/volSphericalTensorField.cxx"

%include "src/OpenFOAM/fields/tmp/tmp_fvScalarMatrix.cxx"
%include "src/OpenFOAM/fields/tmp/tmp_fvVectorMatrix.cxx"

%include "src/OpenFOAM/containers/Lists/PtrList/PtrList_fvMesh.cxx" 
%include "src/OpenFOAM/containers/Lists/PtrList/PtrList_volScalarField.cxx"
%include "src/OpenFOAM/containers/Lists/PtrList/PtrList_surfaceScalarField.cxx"
%include "src/OpenFOAM/containers/Lists/PtrList/PtrList_volVectorField.cxx" 
%include "src/OpenFOAM/containers/Lists/PtrList/PtrList_fvPatch.cxx"
%include "src/OpenFOAM/containers/Lists/List/List_scalar.cxx"

%include "src/OpenFOAM/meshes/GeoMesh_fvMesh.cxx"

%include "src/finiteVolume/fvMesh/fvBoundaryMesh.cxx"
%include "src/finiteVolume/fvMesh/fvPatches/fvPatch.cxx"
%include "src/finiteVolume/fvMesh/fvPatches/derived/wallFvPatch.cxx"
%include "src/finiteVolume/surfaceMesh.cxx"
%include "src/finiteVolume/volMesh.cxx"

%include "src/finiteVolume/fields/fvPatchFields/fvPatchField_scalar.cxx"
%include "src/finiteVolume/fields/fvPatchFields/fvPatchField_vector.cxx"
%include "src/finiteVolume/fields/fvPatchFields/basic/mixed/mixedFvPatchField_scalar.cxx"
%include "src/finiteVolume/fields/fvPatchFields/basic/fixedGradient/fixedGradientFvPatchField_vector.cxx"
%include "src/finiteVolume/fields/fvPatchFields/basic/fixedGradient/fixedGradientFvPatchField_scalar.cxx"
%include "src/finiteVolume/fields/fvPatchFields/basic/fixedValue/fixedValueFvPatchField_scalar.cxx"
%include "src/finiteVolume/fields/fvPatchFields/fvPatchFieldMapper.cxx"

%include "src/finiteVolume/fields/fvPatchFields/zeroGradient/zeroGradientFvPatchField_scalar.cxx"
%include "src/finiteVolume/fields/fvPatchFields/zeroGradient/zeroGradientFvPatchField_vector.cxx"
%include "src/finiteVolume/fields/fvPatchFields/zeroGradient/zeroGradientFvPatchField_tensor.cxx"

%include "src/OpenFOAM/fields/tmp/tmp_fvPatchField_scalar.cxx"
%include "src/OpenFOAM/fields/tmp/tmp_fvPatchField_vector.cxx"

%include "src/finiteVolume/cfdTools/general/adjustPhi.cxx"
%include "src/finiteVolume/cfdTools/general/findRefCell.cxx"
%include "src/finiteVolume/cfdTools/general/bound.cxx"

%include "src/finiteVolume/interpolation/surfaceInterpolation/schemes/linear.cxx"

%include "src/finiteVolume/cfdTools/general/porousMedia/porousZones.cxx"


//---------------------------------------------------------------------------
#endif


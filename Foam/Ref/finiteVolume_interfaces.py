## pythonFlu - Python wrapping for OpenFOAM C++ API
## Copyright (C) 2010- Alexey Petrov
## Copyright (C) 2009-2010 Pebble Bed Modular Reactor (Pty) Limited (PBMR)
## 
## This program is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
## 
## You should have received a copy of the GNU General Public License
## along with this program.  If not, see <http://www.gnu.org/licenses/>.
## 
## See http://sourceforge.net/projects/pythonflu
##
## Author : Alexey PETROV, Andrey SIMURZIN
##


#--------------------------------------------------------------------------------------
attr2interface={ 'fvSchemes' : 'Foam.src.finiteVolume.finiteVolume.fvSchemes.fvSchemes',
                 'fvSolution' : 'Foam.src.finiteVolume.finiteVolume.fvSolution.fvSolution',
                 'volScalarField' : 'Foam.src.finiteVolume.fvMesh.fvMeshes.GeometricField_scalar_fvPatchField_volMesh',
                 'volVectorField' : 'Foam.src.finiteVolume.fvMesh.fvMeshes.GeometricField_vector_fvPatchField_volMesh',
                 'volTensorField' : 'Foam.src.finiteVolume.fvMesh.fvMeshes.GeometricField_tensor_fvPatchField_volMesh',
                 'volSymmTensorField' : 'Foam.src.finiteVolume.fvMesh.fvMeshes.GeometricField_symmTensor_fvPatchField_volMesh',
                 'surfaceScalarField' : 'Foam.src.finiteVolume.fvMesh.fvMeshes.GeometricField_scalar_fvsPatchField_surfaceMesh',
                 'surfaceVectorField' : 'Foam.src.finiteVolume.fvMesh.fvMeshes.GeometricField_vector_fvsPatchField_surfaceMesh',
                 'tmp_volScalarField' : 'Foam.src.finiteVolume.fvMesh.fvMeshes.tmp_volScalarField',
                 'tmp_volVectorField' : 'Foam.src.finiteVolume.fvMesh.fvMeshes.tmp_volVectorField',
                 'tmp_volTensorField' : 'Foam.src.finiteVolume.fvMesh.fvMeshes.tmp_volTensorField',
                 'tmp_volSymmTensorField' : 'Foam.src.finiteVolume.fvMesh.fvMeshes.tmp_volSymmTensorField',
                 'tmp_surfaceScalarField' : 'Foam.src.finiteVolume.fvMesh.fvMeshes.tmp_surfaceScalarField',
                 'tmp_surfaceVectorField' : 'Foam.src.finiteVolume.fvMesh.fvMeshes.tmp_surfaceVectorField',
                 'autoPtr_volScalarField' : 'Foam.src.finiteVolume.fvMesh.fvMeshes.autoPtr_volScalarField',
                 'autoPtr_volVectorField' : 'Foam.src.finiteVolume.fvMesh.fvMeshes.autoPtr_volVectorField',
                 'autoPtr_volTensorField' : 'Foam.src.finiteVolume.fvMesh.fvMeshes.autoPtr_volTensorField',
                 'autoPtr_volSymmTensorField' : 'Foam.src.finiteVolume.fvMesh.fvMeshes.autoPtr_volSymmTensorField',
                 'autoPtr_surfaceScalarField' : 'Foam.src.finiteVolume.fvMesh.fvMeshes.autoPtr_surfaceScalarField',
                 'autoPtr_surfaceVectorField' : 'Foam.src.finiteVolume.fvMesh.fvMeshes.autoPtr_surfaceVectorField',
                 'PtrList_volScalarField' : 'Foam.src.OpenFOAM.containers.Lists.PtrList.PtrList_volScalarField.PtrList_volScalarField',
                 'PtrList_volVectorField' : 'Foam.src.OpenFOAM.containers.Lists.PtrList.PtrList_volVectorField.PtrList_volVectorField',
                 'PtrList_surfaceScalarField' : 'Foam.src.OpenFOAM.containers.Lists.PtrList.PtrList_surfaceScalarField.PtrList_surfaceScalarField',
                 'fvMesh' : 'Foam.src.finiteVolume.fvMesh.fvMeshes.fvMesh',
                 'PtrList_fvMesh' : 'Foam.src.OpenFOAM.containers.Lists.PtrList.PtrList_fvMesh.PtrList_fvMesh',
                 'fvPatchScalarField' : 'Foam.src.finiteVolume.fvMesh.fvMeshes.fvPatchField_scalar',
                 'fvPatchVectorField' : 'Foam.src.finiteVolume.fvMesh.fvMeshes.fvPatchField_vector',
                 'fvPatchTensorField' : 'Foam.src.finiteVolume.fvMesh.fvMeshes.fvPatchField_tensor',
                 'tmp_fvPatchField_scalar' : 'Foam.src.finiteVolume.fvMesh.fvMeshes.tmp_fvPatchField_scalar',
                 'tmp_fvPatchField_vector' : 'Foam.src.finiteVolume.fvMesh.fvMeshes.tmp_fvPatchField_vector',
                 'autoPtr_fvPatchField_scalar' : 'Foam.src.finiteVolume.fvMesh.fvMeshes.autoPtr_fvPatchField_scalar',
                 'autoPtr_fvPatchField_vector' : 'Foam.src.finiteVolume.fvMesh.fvMeshes.autoPtr_fvPatchField_vector',
                 'PtrList_fvPatchField_scalar' : 'Foam.src.finiteVolume.fvMesh.fvMeshes.PtrList_fvPatchField_scalar',
                 'PtrList_fvPatchField_vector' : 'Foam.src.finiteVolume.fvMesh.fvMeshes.PtrList_fvPatchField_vector',
                 'fvsPatchField_scalar' : 'Foam.src.finiteVolume.fvMesh.fvMeshes.fvsPatchField_scalar',
                 'fvsPatchField_vector' : 'Foam.src.finiteVolume.fvMesh.fvMeshes.fvsPatchField_vector',
                 'FieldField_fvPatchField_scalar' : 'Foam.src.finiteVolume.fvMesh.fvMeshes.FieldField_fvPatchField_scalar',
                 'FieldField_fvPatchField_vector' : 'Foam.src.finiteVolume.fvMesh.fvMeshes.FieldField_fvPatchField_vector',
                 'FieldField_fvPatchField_tensor' : 'Foam.src.finiteVolume.fvMesh.fvMeshes.FieldField_fvPatchField_tensor',
                 'DimensionedField_scalar_volMesh' : 'Foam.src.finiteVolume.fvMesh.fvMeshes.DimensionedField_scalar_volMesh',
                 'tmp_DimensionedField_scalar_volMesh' : 'Foam.src.finiteVolume.fvMesh.fvMeshes.tmp_DimensionedField_scalar_volMesh',
                 'DimensionedField_vector_volMesh' : 'Foam.src.finiteVolume.fvMesh.fvMeshes.DimensionedField_vector_volMesh',
                 'tmp_DimensionedField_vector_volMesh' : 'Foam.src.finiteVolume.fvMesh.fvMeshes.tmp_DimensionedField_vector_volMesh',
                 'DimensionedField_tensor_volMesh' : 'Foam.src.finiteVolume.fvMesh.fvMeshes.DimensionedField_tensor_volMesh',
                 'DimensionedField_symmTensor_volMesh' : 'Foam.src.finiteVolume.fvMesh.fvMeshes.DimensionedField_symmTensor_volMesh',
                 'DimensionedField_sphericalTensor_volMesh' : 'Foam.src.finiteVolume.fvMesh.fvMeshes.DimensionedField_sphericalTensor_volMesh',
                 'fvPatch' : 'Foam.src.finiteVolume.fvMesh.fvMeshes.fvPatch',
                 'PtrList_fvPatch' : 'Foam.src.finiteVolume.fvMesh.fvMeshes.PtrList_fvPatch',
                 'fvBoundaryMesh' : 'Foam.src.finiteVolume.fvMesh.fvMeshes.fvBoundaryMesh',
                 'surfaceInterpolation' : 'Foam.src.finiteVolume.fvMesh.fvMeshes.surfaceInterpolation',
                 'TConstructorToTableCounter_fvPatchField_scalar' : 'Foam.src.finiteVolume.fvMesh.fvMeshes.TConstructorToTableCounter_fvPatchField_scalar',
                 'TConstructorToTableCounter_fvPatchField_vector' : 'Foam.src.finiteVolume.fvMesh.fvMeshes.TConstructorToTableCounter_fvPatchField_vector',
                 'fvScalarMatrix' : 'Foam.src.finiteVolume.fvMatrices.fvMatrices.fvScalarMatrix',
                 'fvVectorMatrix' : 'Foam.src.finiteVolume.fvMatrices.fvMatrices.fvVectorMatrix',
                 'tmp_fvScalarMatrix' : 'Foam.src.finiteVolume.fvMatrices.fvMatrices.tmp_fvScalarMatrix',
                 'tmp_fvVectorMatrix' : 'Foam.src.finiteVolume.fvMatrices.fvMatrices.tmp_fvVectorMatrix',
                 'solve' : 'Foam.src.finiteVolume.fvMatrices.fvMatrices.solve',
                 'checkMethod' : 'Foam.src.finiteVolume.fvMatrices.fvMatrices.checkMethod',
                 'correction' : 'Foam.src.finiteVolume.fvMatrices.fvMatrices.correction',
                 'linearInterpolate' : 'Foam.src.finiteVolume.interpolation.surfaceInterpolation.schemes.linear.linearInterpolate',
                 'weighted_vector' : 'Foam.src.finiteVolume.interpolation.surfaceInterpolation.schemes.weighted.weighted_vector.weighted_vector',
                 'setRefCell' : 'Foam.finiteVolume.setRefCell', #!!!!
                 'getRefCellValue' : 'Foam.src.finiteVolume.cfdTools.general.findRefCell.getRefCellValue',
                 'adjustPhi' : 'Foam.src.finiteVolume.cfdTools.general.adjustPhi.adjustPhi',
                 'bound' : 'Foam.src.finiteVolume.cfdTools.general.bound.bound',
                 'mixedFvPatchScalarField' : 'Foam.src.finiteVolume.fields.fvPatchFields.basic.mixed.mixedFvPatchField_scalar.mixedFvPatchScalarField',
                 'fixedValueFvPatchScalarField' : 'Foam.src.finiteVolume.fields.fvPatchFields.basic.fixedValue.fixedValueFvPatchField_scalar.fixedValueFvPatchScalarField',
                 'calculatedFvPatchField_scalar' : 'Foam.src.finiteVolume.fields.fvPatchFields.basic.calculated.calculatedFvPatchField_scalar.calculatedFvPatchField_scalar',
                 'fixedGradientFvPatchVectorField' : 'Foam.src.finiteVolume.fields.fvPatchFields.basic.fixedGradient.fixedGradientFvPatchField_vector.fixedGradientFvPatchVectorField',
                 'fixedGradientFvPatchScalarField' : 'Foam.src.finiteVolume.fields.fvPatchFields.basic.fixedGradient.fixedGradientFvPatchField_scalar.fixedGradientFvPatchScalarField',
                 'calculatedFvsPatchField_scalar' : 'Foam.src.finiteVolume.fields.fvsPatchFields.basic.calculated.calculatedFvsPatchField_scalar.calculatedFvsPatchField_scalar',
                 'porousZone' : 'Foam.src.finiteVolume.cfdTools.general.porousMedia.porousZone.porousZone',
                 'wallFvPatch' : 'Foam.src.finiteVolume.fvMesh.fvPatches.derived.wallFvPatch.wallFvPatch',
                 'subCycle_volScalarField' : 'Foam.src.OpenFOAM.algorithms.subCycle.subCycle_volScalarField.subCycle_volScalarField',
                 'surfaceInterpolationScheme_vector' : 'Foam.src.finiteVolume.interpolation.surfaceInterpolation.surfaceInterpolationScheme.surfaceInterpolationScheme_vector.surfaceInterpolationScheme_vector',
                 'surfaceInterpolationScheme_scalar' : 'Foam.src.finiteVolume.interpolation.surfaceInterpolation.surfaceInterpolationScheme.surfaceInterpolationScheme_scalar.surfaceInterpolationScheme_scalar',
                 'limitedSurfaceInterpolationScheme_vector' : 'Foam.src.finiteVolume.interpolation.surfaceInterpolation.limitedSchemes.limitedSurfaceInterpolationScheme.limitedSurfaceInterpolationScheme_vector.limitedSurfaceInterpolationScheme_vector',
                 'NVDTVD' : 'Foam.src.finiteVolume.interpolation.surfaceInterpolation.limitedSchemes.LimitedScheme.NVDTVD.NVDTVD',
                 'MUSCL_NVDTVD' : 'Foam.src.finiteVolume.interpolation.surfaceInterpolation.limitedSchemes.MUSCL.MUSCL_NVDTVD.MUSCL_NVDTVD',
                 'LimitedScheme_vector_MUSCLLimiter_NVDTVD_limitFuncs_magSqr' : 'Foam.src.finiteVolume.interpolation.surfaceInterpolation.limitedSchemes.LimitedScheme.LimitedScheme_vector_MUSCLLimiter_NVDTVD_limitFuncs_magSqr.LimitedScheme_vector_MUSCLLimiter_NVDTVD_limitFuncs_magSqr',
                 'multivariateSurfaceInterpolationScheme_scalar' : 'Foam.src.finiteVolume.interpolation.surfaceInterpolation.multivariateSchemes.multivariateSurfaceInterpolationScheme.multivariateSurfaceInterpolationScheme_scalar.multivariateSurfaceInterpolationScheme_scalar',
                 'MRFZone' : 'Foam.src.finiteVolume.cfdTools.general.MRF.MRFZone',
                 'MRFZones' : 'Foam.src.finiteVolume.cfdTools.general.MRF.MRFZones.MRFZones',
                 'IOPtrList_MRFZone' : 'Foam.src.OpenFOAM.containers.Lists.PtrList.IOPtrList.IOPtrList_MRFZone.IOPtrList_MRFZone',
                 'PtrList_MRFZone' : 'Foam.src.OpenFOAM.containers.Lists.PtrList.PtrList_MRFZone.PtrList_MRFZone',
                 'initContinuityErrs' : 'Foam.finiteVolume.cfdTools.general.include.initContinuityErrs',
                 'ContinuityErrs' : 'Foam.finiteVolume.cfdTools.general.include.ContinuityErrs',
                 'readPISOControls' : 'Foam.finiteVolume.cfdTools.general.include.readPISOControls',
                 'readTimeControls' : 'Foam.finiteVolume.cfdTools.general.include.readTimeControls',
                 'setInitialDeltaT' : 'Foam.finiteVolume.cfdTools.general.include.setInitialDeltaT',
                 'setDeltaT' : 'Foam.finiteVolume.cfdTools.general.include.setDeltaT',
                 'readSIMPLEControls' : 'Foam.finiteVolume.cfdTools.general.include.readSIMPLEControls',
                 'readPIMPLEControls' : 'Foam.finiteVolume.cfdTools.general.include.readPIMPLEControls',
                 'CourantNo' : 'Foam.finiteVolume.cfdTools.general.include.CourantNo',
                 'readEnvironmentalProperties' : 'Foam.finiteVolume.cfdTools.general.include.readEnvironmentalProperties',
                 'readGravitationalAcceleration' : 'Foam.finiteVolume.cfdTools.general.include.readGravitationalAcceleration',
                 'createPhi' : 'Foam.finiteVolume.cfdTools.incompressible.createPhi',
                 'compressibleCreatePhi' : 'Foam.finiteVolume.cfdTools.compressible.compressibleCreatePhi',
                 'compressibleCourantNo' : 'Foam.finiteVolume.cfdTools.compressible.compressibleCourantNo',
                 'compressibleContinuityErrs' : 'Foam.finiteVolume.cfdTools.compressible.compressibleContinuityErrs',
                 'rhoEqn' : 'Foam.finiteVolume.cfdTools.compressible.rhoEqn' }
                 


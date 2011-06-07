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
## Author : Alexey PETROV
##


#---------------------------------------------------------------------------
from Foam.src.finiteVolume.finiteVolume.fvSchemes import *
from Foam.src.finiteVolume.finiteVolume.fvSolution import *

from Foam.src.finiteVolume.fvMesh.fvMeshes import *

from Foam.src.OpenFOAM.containers.Lists.PtrList.PtrList_fvMesh import *
from Foam.src.OpenFOAM.containers.Lists.PtrList.PtrList_volScalarField import *
from Foam.src.OpenFOAM.containers.Lists.PtrList.PtrList_volVectorField import *
from Foam.src.OpenFOAM.containers.Lists.PtrList.PtrList_surfaceScalarField import *

from Foam.src.finiteVolume.fvMatrices.fvMatrices import *

from Foam.src.finiteVolume.interpolation.surfaceInterpolation.schemes.linear import *
from Foam.src.finiteVolume.interpolation.surfaceInterpolation.schemes.weighted.weighted_vector import *

from Foam.src.finiteVolume.cfdTools.general.findRefCell import *
from Foam.src.finiteVolume.cfdTools.general.adjustPhi import *
from Foam.src.finiteVolume.cfdTools.general.bound import *

from Foam.src.finiteVolume.fields.fvPatchFields.basic.mixed.mixedFvPatchField_scalar import *
from Foam.src.finiteVolume.fields.fvPatchFields.basic.fixedValue.fixedValueFvPatchField_scalar import *
from Foam.src.finiteVolume.fields.fvPatchFields.basic.calculated.calculatedFvPatchField_scalar import *
from Foam.src.finiteVolume.fields.fvPatchFields.basic.fixedGradient.fixedGradientFvPatchField_vector import *
from Foam.src.finiteVolume.fields.fvPatchFields.basic.fixedGradient.fixedGradientFvPatchField_scalar import *

from Foam.src.finiteVolume.fields.fvsPatchFields.basic.calculated.calculatedFvsPatchField_scalar import *

from Foam.src.finiteVolume.cfdTools.general.porousMedia.porousZones import *
from Foam.src.finiteVolume.fvMesh.fvPatches.derived.wallFvPatch import *
from Foam.src.OpenFOAM.algorithms.subCycle.subCycle_volScalarField import *

from Foam.src.finiteVolume.interpolation.surfaceInterpolation.surfaceInterpolationScheme.surfaceInterpolationScheme_vector import *
from Foam.src.finiteVolume.interpolation.surfaceInterpolation.surfaceInterpolationScheme.surfaceInterpolationScheme_scalar import *
from Foam.src.finiteVolume.interpolation.surfaceInterpolation.limitedSchemes.limitedSurfaceInterpolationScheme.limitedSurfaceInterpolationScheme_vector import *
from Foam.src.finiteVolume.interpolation.surfaceInterpolation.limitedSchemes.LimitedScheme.NVDTVD import *
from Foam.src.finiteVolume.interpolation.surfaceInterpolation.limitedSchemes.LimitedScheme.LimitFuncs import *
from Foam.src.finiteVolume.interpolation.surfaceInterpolation.limitedSchemes.MUSCL.MUSCL_NVDTVD import *
from Foam.src.finiteVolume.interpolation.surfaceInterpolation.limitedSchemes.LimitedScheme.LimitedScheme_vector_MUSCLLimiter_NVDTVD_limitFuncs_magSqr import *

from Foam.src.finiteVolume.finiteVolume.snGradSchemes.snGradScheme import *

from Foam.src.finiteVolume.interpolation.surfaceInterpolation.multivariateSchemes.multivariateSurfaceInterpolationScheme.multivariateSurfaceInterpolationScheme_scalar import *

from Foam.src.finiteVolume.cfdTools.general.MRF.MRFZone import *
from Foam.src.finiteVolume.cfdTools.general.MRF.MRFZones import *
from Foam.src.OpenFOAM.containers.Lists.PtrList.IOPtrList.IOPtrList_MRFZone import *
from Foam.src.OpenFOAM.containers.Lists.PtrList.PtrList_MRFZone import *


#---------------------------------------------------------------------------
volScalarField = GeometricField_scalar_fvPatchField_volMesh
volScalarField.DimensionedInternalField = DimensionedField_scalar_volMesh

volVectorField = GeometricField_vector_fvPatchField_volMesh

volTensorField = GeometricField_tensor_fvPatchField_volMesh

volSymmTensorField = GeometricField_symmTensor_fvPatchField_volMesh

surfaceScalarField = GeometricField_scalar_fvsPatchField_surfaceMesh

surfaceVectorField = GeometricField_vector_fvsPatchField_surfaceMesh


#---------------------------------------------------------------------------
fvPatchScalarField = fvPatchField_scalar

fvPatchVectorField = fvPatchField_vector

fvPatchTensorField = fvPatchField_tensor


#----------------------------------------------------------------------------
calculatedFvsPatchScalarField = calculatedFvsPatchField_scalar


#---------------------------------------------------------------------------
calculatedFvPatchScalarField = calculatedFvPatchField_scalar


#---------------------------------------------------------------------------
from Foam.src.finiteVolume.fields.fvPatchFields.zeroGradient.zeroGradientFvPatchField_scalar import *
zeroGradientFvPatchScalarField = zeroGradientFvPatchField_scalar

from Foam.src.finiteVolume.fields.fvPatchFields.zeroGradient.zeroGradientFvPatchField_vector import *
zeroGradientFvPatchVectorField = zeroGradientFvPatchField_vector

from Foam.src.finiteVolume.fields.fvPatchFields.zeroGradient.zeroGradientFvPatchField_scalar import *
zeroGradientFvPatchTensorField = zeroGradientFvPatchField_vector


#----------------------------------------------------------------------------
def continuityErrs( mesh, phi, runTime, cumulativeContErr ):
    from Foam import fvm, fvc

    contErr = fvc.div( phi )
    
    sumLocalContErr = runTime.deltaT().value() * contErr.mag().weightedAverage( mesh.V() ).value()

    globalContErr = runTime.deltaT().value() * contErr.weightedAverage( mesh.V() ).value()

    cumulativeContErr += globalContErr
    
    from Foam.OpenFOAM import ext_Info, nl
    ext_Info << "time step continuity errors : sum local =" << sumLocalContErr \
             << ", global =" << globalContErr \
             << ", cumulative =" << cumulativeContErr
    
    return cumulativeContErr


#---------------------------------------------------------------------------
def setRefCell( *args ):
    from Foam.finiteVolume import ext_setRefCell
    tmp = ext_setRefCell( *args )
    return tmp.m_refCelli, tmp.m_refValue


#---------------------------------------------------------------------------

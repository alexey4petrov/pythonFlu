## VulaSHAKA (Simultaneous Neutronic, Fuel Performance, Heat And Kinetics Analysis)
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
## See https://vulashaka.svn.sourceforge.net/svnroot/vulashaka
##
## Author : Alexey PETROV
##


#---------------------------------------------------------------------------
from Foam.src.finiteVolume.fvMesh.fvMesh import *

from Foam.src.finiteVolume.interpolation.surfaceInterpolation.schemes.linear import *

from Foam.src.finiteVolume.cfdTools.general.findRefCell import *
from Foam.src.finiteVolume.cfdTools.general.adjustPhi import *

from Foam.src.finiteVolume.fvMatrices.fvMatrices import *


#---------------------------------------------------------------------------
from Foam.src.OpenFOAM.fields.GeometricFields.GeometricField_scalar_fvPatchField_volMesh import *
volScalarField = GeometricField_scalar_fvPatchField_volMesh

from Foam.src.OpenFOAM.fields.GeometricFields.GeometricField_vector_fvPatchField_volMesh import *
volVectorField = GeometricField_vector_fvPatchField_volMesh

from Foam.src.OpenFOAM.fields.GeometricFields.GeometricField_tensor_fvPatchField_volMesh import *
volTensorField = GeometricField_tensor_fvPatchField_volMesh

from Foam.src.OpenFOAM.fields.GeometricFields.GeometricField_SymmTensor_fvPatchField_volMesh import *
volSymmTensorField = GeometricField_symmTensor_fvPatchField_volMesh

from Foam.src.OpenFOAM.fields.GeometricFields.GeometricField_scalar_fvsPatchField_surfaceMesh import *
surfaceScalarField = GeometricField_scalar_fvsPatchField_surfaceMesh

from Foam.src.OpenFOAM.fields.GeometricFields.GeometricField_vector_fvsPatchField_surfaceMesh import *
surfaceVectorField = GeometricField_vector_fvsPatchField_surfaceMesh


#---------------------------------------------------------------------------
from Foam.src.finiteVolume.fields.fvPatchFields.fvPatchField_scalar import *
fvPatchScalarField = fvPatchField_scalar

from Foam.src.finiteVolume.fields.fvPatchFields.fvPatchField_vector import *
fvPatchVectorField = fvPatchField_vector

from Foam.src.finiteVolume.fields.fvPatchFields.fvPatchField_tensor import *
fvPatchTensorField = fvPatchField_tensor


# #----------------------------------------------------------------------------
# calculatedFvsPatchScalarField = calculatedFvsPatchField_scalar
# 
# 
# #---------------------------------------------------------------------------
# calculatedFvPatchScalarField = calculatedFvPatchField_scalar
# 
# 
#---------------------------------------------------------------------------
from Foam.src.finiteVolume.fields.fvPatchFields.zeroGradient.zeroGradientFvPatchField_scalar import *
zeroGradientFvPatchScalarField = zeroGradientFvPatchField_scalar

from Foam.src.finiteVolume.fields.fvPatchFields.zeroGradient.zeroGradientFvPatchField_vector import *
zeroGradientFvPatchVectorField = zeroGradientFvPatchField_vector

from Foam.src.finiteVolume.fields.fvPatchFields.zeroGradient.zeroGradientFvPatchField_tensor import *
zeroGradientFvPatchTensorField = zeroGradientFvPatchField_tensor


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

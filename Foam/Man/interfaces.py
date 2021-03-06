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
from Foam.helper import TManLoadHelper
from Foam.Man import incompressible_interfaces
from Foam.Man import compressible_interfaces
from Foam.Man import radiation_interfaces
from Foam.Man import fvm_interfaces
from Foam.Man import fvc_interfaces
from Foam.Man import SRF_interfaces


#--------------------------------------------------------------------------------------
attr2interface={ 'Deps' : 'Foam.ext.common.managedFlu.Deps.Deps',
                 'Time': 'Foam.src.OpenFOAM.db.Time.Time.TimeHolder',
                 'IOobject' : 'Foam.src.OpenFOAM.db.IOobject.IOobjectHolder',
                 'fvMesh' : 'Foam.src.finiteVolume.fvMesh.fvMeshes.fvMeshHolder',
                 'dictionary' : 'Foam.src.OpenFOAM.db.dictionary.dictionary.dictionaryHolder',
                 'IOdictionary' : 'Foam.src.OpenFOAM.db.IOdictionary.IOdictionaryHolder',
                 'uniformDimensionedVectorField' : 'Foam.src.OpenFOAM.fields.UniformDimensionedFields.UniformDimensionedVectorField.uniformDimensionedVectorFieldHolder',
                 'GeometricField' : 'Foam.template.GeometricFieldHolder',
                 'volScalarField' : 'Foam.src.finiteVolume.fvMesh.fvMeshes.GeometricFieldHolder_scalar_fvPatchField_volMesh',
                 'volTensorField' : 'Foam.src.finiteVolume.fvMesh.fvMeshes.GeometricFieldHolder_tensor_fvPatchField_volMesh',
                 'volVectorField' : 'Foam.src.finiteVolume.fvMesh.fvMeshes.GeometricFieldHolder_vector_fvPatchField_volMesh',
                 'surfaceScalarField' : 'Foam.src.finiteVolume.fvMesh.fvMeshes.GeometricFieldHolder_scalar_fvsPatchField_surfaceMesh',
                 'surfaceVectorField' : 'Foam.src.finiteVolume.fvMesh.fvMeshes.GeometricFieldHolder_vector_fvsPatchField_surfaceMesh',
                 'fvScalarMatrix' : 'Foam.src.finiteVolume.fvMatrices.fvMatrices.fvScalarMatrixHolder',
                 'fvVectorMatrix' : 'Foam.src.finiteVolume.fvMatrices.fvMatrices.fvVectorMatrixHolder',
                 'basicPsiThermo' : 'Foam.src.OpenFOAM.fields.tmp.autoPtr_basicPsiThermo.basicPsiThermoHolder',
                 'basicRhoThermo' : 'Foam.src.OpenFOAM.fields.tmp.autoPtr_basicRhoThermo.basicRhoThermoHolder',
                 'basicSolidThermo' : 'Foam.src.OpenFOAM.fields.tmp.autoPtr_basicSolidThermo.basicSolidThermoHolder',
                 'thermalPorousZones' : 'Foam.src.thermophysicalModels.thermalPorousZone.thermalPorousZones.thermalPorousZonesHolder',
                 'singlePhaseTransportModel' : 'Foam.src.transportModels.incompressible.singlePhaseTransportModel.singlePhaseTransportModelHolder',
                 'simpleControl' : 'Foam.src.finiteVolume.cfdTools.general.solutionControl.simpleControl.simpleControlHolder',
                 'pimpleControl' : 'Foam.src.finiteVolume.cfdTools.general.solutionControl.pimpleControl.pimpleControlHolder',
                 'Kmesh' : 'Foam.src.randomProcesses.Kmesh.Kmesh.KmeshHolder',
                 'UOprocess' : 'Foam.src.randomProcesses.processes.UOprocess.UOprocessHolder',
                 'MRFZones' : 'Foam.src.finiteVolume.cfdTools.general.MRF.MRFZones.MRFZonesHolder',
                 'porousZones' : 'Foam.src.finiteVolume.cfdTools.general.porousMedia.porousZones.porousZonesHolder',
                 'basicSourceList' : 'Foam.src.finiteVolume.cfdTools.general.fieldSources.basicSource.basicSource.basicSourceList.basicSourceListHolder',
                 'IObasicSourceList' : 'Foam.src.finiteVolume.cfdTools.general.fieldSources.basicSource.basicSource.IObasicSourceList.IObasicSourceListHolder',
                 'twoPhaseMixture' : 'Foam.src.transportModels.incompressible.twoPhaseMixture.twoPhaseMixtureHolder',
                 'interfaceProperties' : 'Foam.src.transportModels.interfaceProperties.interfaceProperties.interfacePropertiesHolder',
                 'createTime' : 'Foam.OpenFOAM.include.createTimeHolder',
                 'createMesh' : 'Foam.OpenFOAM.include.createMeshHolder',
                 'createMeshNoClear' : 'Foam.OpenFOAM.include.createMeshNoClearHolder',
                 'createDynamicFvMesh' : 'Foam.dynamicFvMesh.createDynamicFvMeshHolder',
                 'createPhi' : 'Foam.finiteVolume.cfdTools.incompressible.createPhiHolder',
                 'compressibleCreatePhi' : 'Foam.finiteVolume.cfdTools.compressible.compressibleCreatePhiHolder',
                 'readGravitationalAcceleration' : 'Foam.finiteVolume.cfdTools.general.include.readGravitationalAccelerationHolder',
                 'linearInterpolate' : 'Foam.ext.common.finiteVolume.managedFlu.linear.linearInterpolate',
                 'incompressible': TManLoadHelper( incompressible_interfaces.attr2interface ),
                 'compressible': TManLoadHelper( compressible_interfaces.attr2interface ),
                 'radiation': TManLoadHelper( radiation_interfaces.attr2interface ),
                 'fvm' : TManLoadHelper( fvm_interfaces.attr2interface ),
                 'fvc' : TManLoadHelper( fvc_interfaces.attr2interface ),
                 'SRF' : TManLoadHelper( SRF_interfaces.attr2interface ),}
                 


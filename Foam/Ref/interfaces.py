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
from Foam.helper import TLoadHelper
from Foam.Ref import token_interfaces


#--------------------------------------------------------------------------------------
attr2interface={ 'argList' : 'Foam.src.OpenFOAM.global_.argList.argList',
                 'messageStream' : 'Foam.src.OpenFOAM.db.error.messageStream.messageStream',
                 'ext_SeriousError' : 'Foam.src.OpenFOAM.db.error.messageStream.ext_SeriousError',
                 'ext_Warning' : 'Foam.src.OpenFOAM.db.error.messageStream.ext_Warning',
                 'ext_Info' : 'Foam.src.OpenFOAM.db.error.messageStream.ext_Info',
                 'Ostream' : 'Foam.src.OpenFOAM.db.IOstreams.IOstreams.Ostream.Ostream',
                 'nl' : 'Foam.src.OpenFOAM.db.IOstreams.IOstreams.Ostream.nl',
                 'tab' : 'Foam.src.OpenFOAM.db.IOstreams.IOstreams.Ostream.tab',
                 'endl' : 'Foam.src.OpenFOAM.db.IOstreams.IOstreams.Ostream.endl',
                 'Time': 'Foam.src.OpenFOAM.db.Time.Time.TimeHolder',
                 'IOobject' : 'Foam.src.OpenFOAM.db.IOobject.IOobjectHolder',
                 'IOobjectList' : 'Foam.src.OpenFOAM.db.IOobjectList.IOobjectList',
                 'fileName' : 'Foam.src.OpenFOAM.primitives.strings.fileName.fileName',
                 'IOdictionary' : 'Foam.src.OpenFOAM.db.IOdictionary.IOdictionary',
                 'autoPtr_IOdictionary' : 'Foam.src.OpenFOAM.fields.tmp.autoPtr_IOdictionary.autoPtr_IOdictionary',
                 'dictionary' : 'Foam.src.OpenFOAM.db.dictionary.dictionary.dictionary',
                 'word' : 'Foam.src.OpenFOAM.primitives.strings.word.word',
                 'keyType' : 'Foam.src.OpenFOAM.primitives.strings.keyType.keyType',
                 'Switch' : 'Foam.src.OpenFOAM.db.Switch.Switch',
                 'dimensionedScalar' : 'Foam.src.OpenFOAM.dimensionedTypes.dimensionedScalar.dimensionedScalar',
                 'dimensionedVector' : 'Foam.src.OpenFOAM.dimensionedTypes.dimensionedVector.dimensionedVector',
                 'dimensionedSymmTensor' : 'Foam.src.OpenFOAM.dimensionedTypes.dimensionedSymmTensor.dimensionedSymmTensor',
                 'dimensionedTensor' : 'Foam.src.OpenFOAM.dimensionedTypes.dimensionedTensor.dimensionedTensor',
                 'dimensionSet' : 'Foam.src.OpenFOAM.dimensionSet.dimensionSet',
                 'dimensionSets' : ' Foam.src.OpenFOAM.dimensionSets.dimensionSets',
                 'scalar' : 'float',
                 'string' : 'str',
                 'GREAT' : 'Foam.src.OpenFOAM.primitives.scalar.GREAT',
                 'SMALL' : 'Foam.src.OpenFOAM.primitives.scalar.SMALL',
                 'readScalar' : 'Foam.src.OpenFOAM.primitives.scalar.readScalar',
                 'readLabel' : 'Foam.src.OpenFOAM.primitives.label.readLabel',
                 'readInt' : 'Foam.src.OpenFOAM.primitives.int_',
                 'vector' : 'Foam.src.OpenFOAM.primitives.vector.vector',
                 'symmTensor' : 'Foam.src.OpenFOAM.primitives.symmTensor.symmTensor',
                 'tensor' : 'Foam.src.OpenFOAM.primitives.tensor.tensor',
                 'readBool' : 'Foam.src.OpenFOAM.primitives.bool.readBool',
                 'one' : 'Foam.src.OpenFOAM.primitives.one.one',
                 'complex' : 'Foam.src.OpenFOAM.primitives.complex.complex',
                 'complexVector' : 'Foam.src.OpenFOAM.primitives.complexVector.complexVector',
                 'Random' : 'Foam.src.OpenFOAM.primitives.Random.Random',
                 'IFstream' : 'Foam.src.OpenFOAM.db.IOstreams.Fstreams.IFstream.IFstream',
                 'OFstream' : 'Foam.src.OpenFOAM.db.IOstreams.Fstreams.OFstream.OFstream',
                 'Pstream' : 'Foam.src.OpenFOAM.db.IOstreams.Pstreams.Pstream.Pstream',
                 'solution' : 'Foam.src.OpenFOAM.matrices.solution.solution',
                 'solution_upgradeSolverDict' : 'Foam.src.OpenFOAM.matrices.solution.solution_upgradeSolverDict',
                 'ext_solution' : 'Foam.src.OpenFOAM.matrices.ext_solution.ext_solution',
                 'PtrList_entry' : 'Foam.src.OpenFOAM.containers.Lists.PtrList.PtrList_entry.PtrList_entry',
                 'PtrList_GenericType' : 'Foam.src.OpenFOAM.containers.Lists.PtrList.PtrList_GenericType.PtrList_GenericType',
                 'PtrList_GenericINew' : 'Foam.src.OpenFOAM.containers.Lists.PtrList.PtrList_GenericINew.PtrList_GenericINew',
                 'PtrList_Generic' : 'Foam.src.OpenFOAM.containers.Lists.PtrList.PtrList_Generic.PtrList_Generic',
                 'UniformDimensionedVectorField' : 'Foam.src.OpenFOAM.fields.UniformDimensionedFields.UniformDimensionedVectorField.UniformDimensionedVectorField',
                 'PtrList_UniformDimensionedVectorField' : 'Foam.src.OpenFOAM.containers.Lists.PtrList.PtrList_UniformDimensionedVectorField.PtrList_UniformDimensionedVectorField',
                 'HashPtrTable_IOobject_word_string_hash' : 'Foam.src.OpenFOAM.containers.HashTables.HashPtrTable.HashPtrTable_IOobject_word_string_hash.HashPtrTable_IOobject_word_string_hash',
                 'HashTable_int_word_string_hash' : 'Foam.src.OpenFOAM.containers.HashTables.HashTable.HashTable_int_word_string_hash.HashTable_int_word_string_hash',
                 'NamedEnum' : 'Foam.src.OpenFOAM.containers.NamedEnum.NamedEnum.NamedEnum',
                 'autoPtr_polyPatch' : 'Foam.src.OpenFOAM.fields.tmp.autoPtr_polyPatch.autoPtr_polyPatch',
                 'polyPatchID' : 'Foam.src.OpenFOAM.meshes.polyMesh.zones.ZoneID.polyPatchID.polyPatchID',
                 'scalarField' : 'Foam.src.OpenFOAM.fields.Fields.primitiveFields.scalarField',
                 'vectorField' : 'Foam.src.OpenFOAM.fields.Fields.primitiveFields.vectorField',
                 'sphericalTensorField' : 'Foam.src.OpenFOAM.fields.Fields.primitiveFields.sphericalTensorField',
                 'symmTensorField' : 'Foam.src.OpenFOAM.fields.Fields.primitiveFields.symmTensorField',
                 'tensorField' : 'Foam.src.OpenFOAM.fields.Fields.primitiveFields.tensorField',
                 'tmp_scalarField' : 'Foam.src.OpenFOAM.fields.Fields.primitiveFields.tmp_scalarField',
                 'tmp_vectorField' : 'Foam.src.OpenFOAM.fields.Fields.primitiveFields.tmp_vectorField',
                 'tmp_sphericalTensorField' : 'Foam.src.OpenFOAM.fields.Fields.primitiveFields.tmp_sphericalTensorField',
                 'tmp_symmTensorField' : 'Foam.src.OpenFOAM.fields.Fields.primitiveFields.tmp_symmTensorField',
                 'tmp_tensorField' : 'Foam.src.OpenFOAM.fields.Fields.primitiveFields.tmp_tensorField',
                 'IStringStream' : 'Foam.src.OpenFOAM.db.IOstreams.StringStreams.IStringStream.IStringStream',
                 'mapDistribute' : 'Foam.src.OpenFOAM.meshes.polyMesh.mapPolyMesh.mapDistribute.mapDistribute.mapDistribute',
                 'boolList' : 'Foam.src.OpenFOAM.containers.Lists.List.List_bool.List_bool',
                 'labelList' : 'Foam.src.OpenFOAM.containers.Lists.List.List_label.List_label',
                 'scalarList' : 'Foam.src.OpenFOAM.containers.Lists.List.List_scalar.List_scalar',
                 'tensorList' : 'Foam.src.OpenFOAM.containers.Lists.List.List_tensor.List_tensor',
                 'tokenList' : 'Foam.src.OpenFOAM.containers.Lists.List.List_token.List_token',
                 'vectorList' : 'Foam.src.OpenFOAM.containers.Lists.List.List_vector.List_vector',
                 'wordList' : 'Foam.src.OpenFOAM.containers.Lists.List.List_word.List_word',
                 'complexList' : 'Foam.src.OpenFOAM.containers.Lists.List.List_complex.List_complex',
                 'cellList' : 'Foam.src.OpenFOAM.containers.Lists.List.List_cell.List_cell',
                 'faceList' : 'Foam.src.OpenFOAM.containers.Lists.List.List_face.List_face',
                 'polyPatchListPtr' : 'Foam.src.OpenFOAM.containers.Lists.List.List_polyPatchPtr.List_polyPatchPtr',
                 'wordHashTable' : 'Foam.src.OpenFOAM.containers.HashTables.HashTable.HashTable_word_word_string_hash.HashTable_word_word_string_hash',
                 'I' : 'Foam.src.OpenFOAM.primitives.sphericalTensor.I',
                 'mag' : 'abs',
                 'oneField' : 'Foam.src.OpenFOAM.fields.Fields.oneField.oneField',
                 'oneFieldField' : 'Foam.src.OpenFOAM.fields.FieldFields.oneFieldField.oneFieldField',
                 'geometricOneField' : 'Foam.src.OpenFOAM.fields.GeometricFields.geometricOneField.geometricOneField',
                 'complexField' : 'Foam.src.OpenFOAM.fields.Fields.complexFields.complexField',
                 'complexVectorField' : 'Foam.src.OpenFOAM.fields.Fields.complexFields.complexVectorField',
                 'tmp_complexField' : 'Foam.src.OpenFOAM.fields.tmp.tmp_complexField.tmp_complexField',
                 'tmp_complexVectorField ' : 'Foam.src.OpenFOAM.fields.tmp.tmp_complexField.tmp_complexVectorField',
                 'setRootCase' : 'Foam.OpenFOAM.include.setRootCase', 
                 'createTime' : 'Foam.OpenFOAM.include.createTime',
                 'createMesh' : 'Foam.OpenFOAM.include.createMesh',
                 'createMeshNoClear' : 'Foam.OpenFOAM.include.createMeshNoClear',
                 'token' : token_interfaces.TTokenLoadHelper( token_interfaces.attr2interface ) }
                 


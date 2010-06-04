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
//  See https://vulashaka.svn.sourceforge.net/svnroot/vulashaka
//
//  Author : Alexey PETROV


//---------------------------------------------------------------------------
#ifndef OpenFOAM_cxx
#define OpenFOAM_cxx


//---------------------------------------------------------------------------
// Keep on corresponding "director" includes at the top of SWIG defintion file

%include "src/OpenFOAM/directors.hxx"


//----------------------------------------------------------------------------
%include "src/OpenFOAM/primitives/bool.cxx"
%include "src/OpenFOAM/primitives/label.cxx"
%include "src/OpenFOAM/primitives/scalar.cxx"
%include "src/OpenFOAM/primitives/vector.cxx"
%include "src/OpenFOAM/primitives/tensor.cxx"
%include "src/OpenFOAM/primitives/s_ymmTensor.cxx"
%include "src/OpenFOAM/primitives/strings/string.cxx"
%include "src/OpenFOAM/primitives/strings/word.cxx"
%include "src/OpenFOAM/primitives/strings/fileName.cxx"
%include "src/OpenFOAM/primitives/direction.cxx"

%include "src/OpenFOAM/primitives/ops/ops_label.cxx"

%include "src/OpenFOAM/primitives/Lists/boolList.cxx"
%include "src/OpenFOAM/primitives/Lists/labelList.cxx"
%include "src/OpenFOAM/primitives/Lists/scalarList.cxx"
%include "src/OpenFOAM/primitives/Lists/vectorList.cxx"
%include "src/OpenFOAM/primitives/Lists/tensorList.cxx"
%include "src/OpenFOAM/primitives/Lists/wordList.cxx"
%include "src/OpenFOAM/primitives/Lists/tokenList.cxx"

%include "src/OpenFOAM/containers/HashTables/HashTable/HashTable_word_word_string_hash.cxx"

%include "src/OpenFOAM/containers/Lists/List/List_pPolyPatch.cxx"
%include "src/OpenFOAM/meshes/meshShapes/face/faceList.cxx"
%include "src/OpenFOAM/meshes/meshShapes/cell/cellList.cxx"

%include "src/OpenFOAM/db/Switch.cxx"
%include "src/OpenFOAM/db/IOobject.cxx"
%include "src/OpenFOAM/db/IOobjectList.cxx"
%include "src/OpenFOAM/db/IOdictionary.cxx"
%include "src/OpenFOAM/db/IOstreams/token.cxx"
%include "src/OpenFOAM/db/IOstreams/IOstreams/IOstream.cxx"
%include "src/OpenFOAM/db/IOstreams/IOstreams/Ostream.cxx"
%include "src/OpenFOAM/db/IOstreams/IOstreams/Istream.cxx"
%include "src/OpenFOAM/db/IOstreams/Sstreams/OSstream.cxx"
%include "src/OpenFOAM/db/IOstreams/Sstreams/ISstream.cxx"
%include "src/OpenFOAM/db/IOstreams/Fstreams/OFstream.cxx"
%include "src/OpenFOAM/db/IOstreams/Fstreams/IFstream.cxx"
%include "src/OpenFOAM/db/IOstreams/StringStreams/IStringStream.cxx"
%include "src/OpenFOAM/db/IOstreams/StringStreams/OStringStream.cxx"
%include "src/OpenFOAM/db/IOstreams/Pstreams/Pstream.cxx"
%include "src/OpenFOAM/db/error/messageStream.cxx"
%include "src/OpenFOAM/db/objectRegistry.cxx"
%include "src/OpenFOAM/db/regIOobject.cxx"
%include "src/OpenFOAM/db/Time/Time.cxx"

%include "src/OpenFOAM/dimensionSet.cxx"
%include "src/OpenFOAM/dimensionSets.cxx"
%include "src/OpenFOAM/dimensionedTypes/dimensionedType.cxx"
%include "src/OpenFOAM/dimensionedTypes/dimensionedScalar.cxx"
%include "src/OpenFOAM/dimensionedTypes/dimensionedVector.cxx"
%include "src/OpenFOAM/dimensionedTypes/dimensionedTensor.cxx"
%include "src/OpenFOAM/dimensionedTypes/dimensionedSymmTensor.cxx"

%include "src/OpenFOAM/meshes/patchIdentifier.cxx"
%include "src/OpenFOAM/meshes/meshShapes/cell/cell.cxx"
%include "src/OpenFOAM/meshes/meshShapes/cell/cellList.cxx"

%include "src/OpenFOAM/meshes/meshShapes/face/face.cxx"
%include "src/OpenFOAM/meshes/meshShapes/face/faceList.cxx"
%include "src/OpenFOAM/meshes/meshShapes/face/faceListFwd.cxx"
%include "src/OpenFOAM/meshes/meshShapes/face/oppositeFace.cxx"

%include "src/OpenFOAM/meshes/primitiveShapes/point/point.cxx"
%include "src/OpenFOAM/meshes/primitiveShapes/point/pointField.cxx"
%include "src/OpenFOAM/meshes/primitiveShapes/point/pointFieldFwd.cxx"

%include "src/OpenFOAM/meshes/primitiveMesh/primitiveMesh.cxx"

%include "src/OpenFOAM/meshes/polyMesh/polyMesh.cxx"
%include "src/OpenFOAM/meshes/polyMesh/polyBoundaryMesh.cxx"
%include "src/OpenFOAM/meshes/polyMesh/polyPatches/polyPatch.cxx"
%include "src/OpenFOAM/meshes/polyMesh/zones/ZoneID/polyPatchID.cxx"
%include "src/OpenFOAM/fields/tmp/autoPtr_polyPatch.cxx" 

%include "src/OpenFOAM/global/argList.cxx"

%include "src/OpenFOAM/matrices/ext_solution.cxx"

%include "src/OpenFOAM/fields/tmp/autoPtr_UniformDimensionedVectorField.cxx" 
%include "src/OpenFOAM/containers/Lists/PtrList/PtrList_UniformDimensionedVectorField.cxx"
%include "src/OpenFOAM/containers/Lists/PtrList/PtrList_entry.cxx"

%include "/src/OpenFOAM/meshes/polyMesh/mapPolyMesh/mapDistribute/mapDistribute.cxx"


//---------------------------------------------------------------------------
#endif

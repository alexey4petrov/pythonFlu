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


#--------------------------------------------------------------------------
from Foam.src.OpenFOAM.global_.argList import *

from Foam.src.OpenFOAM.db.error.messageStream import *
from Foam.src.OpenFOAM.db.IOstreams.IOstreams.Ostream import *

from Foam.src.OpenFOAM.db.Time.Time import *
from Foam.src.OpenFOAM.db.IOobject import *
from Foam.src.OpenFOAM.db.IOobjectList import *
from Foam.src.OpenFOAM.primitives.strings.fileName import *

from Foam.src.OpenFOAM.db.IOdictionary import *
from Foam.src.OpenFOAM.fields.tmp.autoPtr_IOdictionary import *
from Foam.src.OpenFOAM.db.dictionary.dictionary import *
from Foam.src.OpenFOAM.primitives.strings.word import *
from Foam.src.OpenFOAM.primitives.strings.keyType import *

from Foam.src.OpenFOAM.db.Switch import *

from Foam.src.OpenFOAM.dimensionedTypes.dimensionedScalar import *
from Foam.src.OpenFOAM.dimensionedTypes.dimensionedVector import *
from Foam.src.OpenFOAM.dimensionedTypes.dimensionedSymmTensor import *
from Foam.src.OpenFOAM.dimensionedTypes.dimensionedTensor import *

from Foam.src.OpenFOAM.dimensionSet import *
from Foam.src.OpenFOAM.dimensionSets import *

from Foam.src.OpenFOAM.primitives.scalar import *
from Foam.src.OpenFOAM.primitives.label import *
from Foam.src.OpenFOAM.primitives.int_ import *
from Foam.src.OpenFOAM.primitives.vector import *
from Foam.src.OpenFOAM.primitives.symmTensor import *
from Foam.src.OpenFOAM.primitives.tensor import *
from Foam.src.OpenFOAM.primitives.bool import *
from Foam.src.OpenFOAM.primitives.one import *
from Foam.src.OpenFOAM.primitives.complex import *
from Foam.src.OpenFOAM.primitives.complexVector import *
from Foam.src.OpenFOAM.primitives.Random import *

from Foam.src.OpenFOAM.primitives.ops.ops_label import *

from Foam.src.OpenFOAM.db.IOstreams.Fstreams.IFstream import *
from Foam.src.OpenFOAM.db.IOstreams.Fstreams.OFstream import *
from Foam.src.OpenFOAM.db.IOstreams.Pstreams.Pstream import *

from Foam.src.OpenFOAM.matrices.solution import *
from Foam.src.OpenFOAM.matrices.ext_solution import *


#---------------------------------------------------------------------------
from Foam.src.OpenFOAM.db.IOstreams.token import *

token.NULL_TOKEN = ext_make_punctuationToken( token.NULL_TOKEN )
token.SPACE = ext_make_punctuationToken( token.SPACE )
token.TAB = ext_make_punctuationToken( token.TAB )
token.NL = ext_make_punctuationToken( token.NL )

token.END_STATEMENT = ext_make_punctuationToken( token.END_STATEMENT )
token.BEGIN_LIST = ext_make_punctuationToken( token.BEGIN_LIST )
token.END_LIST = ext_make_punctuationToken( token.END_LIST )
token.BEGIN_SQR = ext_make_punctuationToken( token.BEGIN_SQR )
token.END_SQR = ext_make_punctuationToken( token.END_SQR )
token.BEGIN_BLOCK = ext_make_punctuationToken( token.BEGIN_BLOCK )
token.END_BLOCK = ext_make_punctuationToken( token.END_BLOCK )

token.COLON = ext_make_punctuationToken( token.COLON )
token.COMMA = ext_make_punctuationToken( token.COMMA )

token.BEGIN_STRING = ext_make_punctuationToken( token.BEGIN_STRING )
token.END_STRING = ext_make_punctuationToken( token.END_STRING )

token.ASSIGN = ext_make_punctuationToken( token.ASSIGN )
token.ADD = ext_make_punctuationToken( token.ADD )
token.SUBTRACT = ext_make_punctuationToken( token.SUBTRACT )
token.MULTIPLY = ext_make_punctuationToken( token.MULTIPLY )
token.DIVIDE = ext_make_punctuationToken( token.DIVIDE )


#---------------------------------------------------------------------------
from Foam.src.OpenFOAM.containers.Lists.PtrList.PtrList_entry import *
from Foam.src.OpenFOAM.containers.Lists.PtrList.PtrList_GenericType import *
from Foam.src.OpenFOAM.containers.Lists.PtrList.PtrList_GenericINew import *
from Foam.src.OpenFOAM.containers.Lists.PtrList.PtrList_Generic import *

from Foam.src.OpenFOAM.fields.UniformDimensionedFields.UniformDimensionedVectorField import *
from Foam.src.OpenFOAM.containers.Lists.PtrList.PtrList_UniformDimensionedVectorField import *

from Foam.src.OpenFOAM.containers.HashTables.HashPtrTable.HashPtrTable_IOobject_word_string_hash import *

from Foam.src.OpenFOAM.containers.HashTables.HashTable.HashTable_int_word_string_hash import *
from Foam.src.OpenFOAM.containers.NamedEnum.NamedEnum import *


from Foam.src.OpenFOAM.fields.tmp.autoPtr_polyPatch import *
from Foam.src.OpenFOAM.meshes.polyMesh.zones.ZoneID.polyPatchID import *

from Foam.src.OpenFOAM.fields.Fields.primitiveFields import *

from Foam.src.OpenFOAM.db.IOstreams.StringStreams.IStringStream import *

from Foam.src.OpenFOAM.meshes.polyMesh.mapPolyMesh.mapDistribute.mapDistribute import *


#---------------------------------------------------------------------------
scalar = float

string = str


#---------------------------------------------------------------------------
from Foam.src.OpenFOAM.containers.Lists.List.List_bool import *
boolList = List_bool

from Foam.src.OpenFOAM.containers.Lists.List.List_label import *
labelList = List_label

from Foam.src.OpenFOAM.containers.Lists.List.List_scalar import *
scalarList = List_scalar

from Foam.src.OpenFOAM.containers.Lists.List.List_tensor import *
tensorList = List_tensor

from Foam.src.OpenFOAM.containers.Lists.List.List_token import *
tokenList = List_token

from Foam.src.OpenFOAM.containers.Lists.List.List_vector import *
vectorList = List_vector

from Foam.src.OpenFOAM.containers.Lists.List.List_word import *
wordList = List_word

from Foam.src.OpenFOAM.containers.Lists.List.List_complex import *
complexList = List_complex


#---------------------------------------------------------------------------
from Foam.src.OpenFOAM.containers.Lists.List.List_cell import *
cellList = List_cell

from Foam.src.OpenFOAM.containers.Lists.List.List_face import *
faceList = List_face

from Foam.src.OpenFOAM.containers.Lists.List.List_polyPatchPtr import *
polyPatchListPtr = List_polyPatchPtr

from Foam.src.OpenFOAM.containers.HashTables.HashTable.HashTable_word_word_string_hash import *
wordHashTable = HashTable_word_word_string_hash


#---------------------------------------------------------------------------
from Foam.src.OpenFOAM.primitives.sphericalTensor import *
I = sphericalTensor.I


#---------------------------------------------------------------------------
mag = abs


#---------------------------------------------------------------------------
from Foam.src.OpenFOAM.fields.Fields.oneField import *
from Foam.src.OpenFOAM.fields.FieldFields.oneFieldField import *
from Foam.src.OpenFOAM.fields.GeometricFields.geometricOneField import *


#---------------------------------------------------------------------------
from Foam.src.OpenFOAM.fields.Fields.complexFields import *
from Foam.src.OpenFOAM.fields.tmp.tmp_complexField import *
from Foam.src.OpenFOAM.fields.tmp.tmp_complexVectorField import *

	
#---------------------------------------------------------------------------

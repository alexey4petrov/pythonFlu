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


#--------------------------------------------------------------------------
from Foam.src.OpenFOAM.global_.argList import *

from Foam.src.OpenFOAM.db.error.messageStream import *
from Foam.src.OpenFOAM.db.IOstreams.IOstreams.Ostream import *

from Foam.src.OpenFOAM.db.Time.Time import *
from Foam.src.OpenFOAM.db.IOobject import *
from Foam.src.OpenFOAM.primitives.strings.fileName import *

from Foam.src.OpenFOAM.db.IOdictionary import *
from Foam.src.OpenFOAM.db.dictionary.dictionary import *
from Foam.src.OpenFOAM.primitives.strings.word import *

from Foam.src.OpenFOAM.db.Switch import *

from Foam.src.OpenFOAM.dimensionedTypes.dimensionedScalar import *
from Foam.src.OpenFOAM.dimensionedTypes.dimensionedVector import *
from Foam.src.OpenFOAM.dimensionedTypes.dimensionedSymmTensor import *
from Foam.src.OpenFOAM.dimensionedTypes.dimensionedTensor import *

from Foam.src.OpenFOAM.dimensionSet import *
from Foam.src.OpenFOAM.dimensionSets import *

from Foam.src.OpenFOAM.primitives.scalar import *
from Foam.src.OpenFOAM.primitives.int_ import *
from Foam.src.OpenFOAM.primitives.vector import *
from Foam.src.OpenFOAM.primitives.s_phericalTensor import *
from Foam.src.OpenFOAM.primitives.tensor import *

from Foam.src.OpenFOAM.db.IOstreams.Fstreams.IFstream import *

from Foam.src.OpenFOAM.containers.Lists.PtrList.PtrList_entry import *
from Foam.src.OpenFOAM.containers.Lists.PtrList.PtrList_GenericType import *
from Foam.src.OpenFOAM.containers.Lists.PtrList.PtrList_GenericINew import *
from Foam.src.OpenFOAM.containers.Lists.PtrList.PtrList_Generic import *

from Foam.src.OpenFOAM.fields.UniformDimensionedFields.UniformDimensionedVectorField import *
from Foam.src.OpenFOAM.containers.Lists.PtrList.PtrList_UniformDimensionedVectorField import *

from Foam.src.OpenFOAM.fields.Fields.vectorField import *


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
from Foam.src.OpenFOAM.primitives.s_phericalTensor import *
I = sphericalTensor.I


#---------------------------------------------------------------------------
mag = abs


#---------------------------------------------------------------------------

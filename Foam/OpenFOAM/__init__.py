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
from Foam import get_module_initializtion_command
exec get_module_initializtion_command( "OpenFOAM_" ) 


#---------------------------------------------------------------------------
scalar = float

string = str


#---------------------------------------------------------------------------
boolList = List_bool

labelList = List_label

scalarList = List_scalar

scalarList = List_string

scalarList = List_scalar

tensorList = List_tensor

tokenList = List_token

vectorList = List_vector

wordList = List_word


#---------------------------------------------------------------------------
wordList = List_word

cellList = List_cell

faceList = List_face

pPolyPatchList = List_pPolyPatch

wordHashTable = HashTable_word_word_string_hash


#---------------------------------------------------------------------------
I = sphericalTensor.I

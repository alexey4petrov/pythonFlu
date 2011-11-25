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
##  Author : Alexey PETROV, Andrey SIMURZIN


#---------------------------------------------------------------------------
from Foam import ref
from nose.tools import ok_, raises, eq_


#---------------------------------------------------------------------------
def testCreateField():
    vector1= ref.vector( 1.0,1.0,1.0 )
    vector2= ref.vector( 2.0,2.0,2.0 )

    vector_Field = ref.vectorField( 2 )
    vector_Field[0] = vector1
    vector_Field[1] = vector2
    
def testFieldIterator():
    vector1= ref.vector( 1.0,1.0,1.0 )

    vector_Field = ref.vectorField( 2 )
    vector_Field[ 0 ] = vector1
    vector_Field[ 1 ] = vector1
    for item in vector_Field:
       eq_(item.x(),vector1.x())
       eq_(item.y(),vector1.y())
       eq_(item.z(),vector1.z())
       pass


#---------------------------------------------------------------------------


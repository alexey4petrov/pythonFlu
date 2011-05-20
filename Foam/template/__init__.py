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


#--------------------------------------------------------------------------------------
def fvPatchField( Type ):
    className = None

    import Foam.OpenFOAM
    if Type == Foam.OpenFOAM.scalar :
        className = "scalar"
    elif Type == Foam.OpenFOAM.vector :
        className = "vector"
    else:
        raise NotImplementedError( "fvPatchField< %s > " % repr( Type ) )

    a_class = None
    an_expression = "from Foam.finiteVolume import fvPatchField_%s as engine; a_class = engine" % ( className )
    exec( an_expression )

    return a_class


#--------------------------------------------------------------------------------------
def fvsPatchField( Type ) :
    className = None

    import Foam.OpenFOAM
    if Type == Foam.OpenFOAM.scalar :
        className = "scalar"
    elif Type == Foam.OpenFOAM.vector :
        className = "vector"
    else:
        raise NotImplementedError( "fvsPatchField< %s > " % repr( Type ) )

    a_class = None
    an_expression = "from Foam.finiteVolume import fvsPatchField_%s as engine; a_class = engine" % ( className )
    exec( an_expression )

    return a_class
        

#--------------------------------------------------------------------------------------
def GeometricFieldTypeName( Type, MeshType ) :
    import Foam

    typeClassName = None
    if Type == Foam.OpenFOAM.scalar :
        typeClassName = "Scalar"
    elif Type == Foam.OpenFOAM.vector :
        typeClassName = "Vector"
    else:
        raise NotImplementedError( "GeometricField< %s, XX, YY > " % ( repr( Type ) ) )


    meshClassName = None
    import Foam.finiteVolume
    if MeshType == Foam.finiteVolume.volMesh :
        meshClassName = "vol"
    elif MeshType == Foam.finiteVolume.surfaceMesh :
        meshClassName = "surface"
    else:
        raise NotImplementedError( "GeometricField< %s, %s, %s > " % ( repr( Type ), repr( patchFieldType ), repr( MeshType ) ) )

    
    className = "%s%sField" % ( meshClassName, typeClassName )
                                  
    return className
    

#--------------------------------------------------------------------------------------
def GeometricField( Type, patchFieldType, MeshType ) :

    typeClassName = None
    import Foam.OpenFOAM
    if Type == Foam.OpenFOAM.scalar :
        typeClassName = "scalar"
    elif Type == Foam.OpenFOAM.vector :
        typeClassName = "vector"
    else:
        raise NotImplementedError( "GeometricField< %s, XX, YY > " % ( repr( Type ) ) )


    patchFieldClassName = None
    if patchFieldType == fvPatchField :
        patchFieldClassName = "fvPatchField"
    elif patchFieldType == fvsPatchField :
        patchFieldClassName = "fvsPatchField"
    else:
        raise NotImplementedError( "GeometricField< %s, %s, YY > " % ( repr( Type ), repr( patchFieldType ) ) )

    
    meshClassName = None
    import Foam.finiteVolume
    if MeshType == Foam.finiteVolume.volMesh :
        meshClassName = "volMesh"
    elif MeshType == Foam.finiteVolume.surfaceMesh :
        meshClassName = "surfaceMesh"
    else:
        raise NotImplementedError( "GeometricField< %s, %s, %s > " % ( repr( Type ), repr( patchFieldType ), repr( MeshType ) ) )

    
    a_class = None
    className = "GeometricField_%s_%s_%s" % ( typeClassName, patchFieldClassName, meshClassName )
    an_expression = "from Foam.finiteVolume import %s as engine; a_class = engine" % ( className )
    exec( an_expression )

    return a_class
    

#----------------------------------------------------------------------------------------       
def getfvPatchFieldConstructorToTableBase_scalar() :
    aClass = None

    from Foam.finiteVolume import TConstructorToTableCounter_fvPatchField_scalar
    aCounter = TConstructorToTableCounter_fvPatchField_scalar.counter()
    
    aClassName = "fvPatchFieldConstructorToTableBase_scalar_%d" % aCounter
    anExpression = "from Foam.finiteVolume import %s; aClass = %s" % \
                   ( aClassName, aClassName )
    exec( anExpression )

    return aClass


#-------------------------------------------------------------------------------------------
def getfvPatchFieldConstructorToTableBase_vector() :
    aClass = None

    from Foam.finiteVolume import TConstructorToTableCounter_fvPatchField_vector
    aCounter = TConstructorToTableCounter_fvPatchField_vector.counter()
    
    aClassName = "fvPatchFieldConstructorToTableBase_vector_%d" % aCounter
    anExpression = "from Foam.finiteVolume import %s; aClass = %s" % \
                   ( aClassName, aClassName )
    exec( anExpression )

    return aClass


#-------------------------------------------------------------------------------------------
from Foam.template.PtrList import *

from Foam.OpenFOAM import PtrList_INewHolder, PtrList_INewBase, PtrList_TypeHolder, PtrList_TypeBase, autoPtr_PtrList_TypeHolder

from Foam.OpenFOAM import PtrList_Generic as PtrList

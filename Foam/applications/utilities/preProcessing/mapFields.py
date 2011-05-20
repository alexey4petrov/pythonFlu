#!/usr/bin/env python

#--------------------------------------------------------------------------------------
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
from Foam.OpenFOAM import ext_Info, ext_Warning, ext_SeriousError, tab, nl

#---------------------------------------------------------------------------
def createTime( rootPath, caseName ) :
    print "Create time for '%s'\n" % caseName
    
    from Foam.OpenFOAM import Time
    from Foam.OpenFOAM import fileName
    
    runTime = Time( Time.controlDictName.fget(),
                    fileName( rootPath ),
                    fileName( caseName ) )
    
    #runTime.setTime( runTime.endTime(), 0 )

    return runTime


#--------------------------------------------------------------------------------------
def __getClass__( theObject, theClassTypeDef ):
    aClass = None

    anExpression = "from Foam.finiteVolume import %s; aClass = %s" % \
                   ( theClassTypeDef, theClassTypeDef )
    exec( anExpression )

    return aClass


#--------------------------------------------------------------------------------------
def getIOobjectClass( theIOobject ):
    return __getClass__( theIOobject, theIOobject.headerClassName() )


#--------------------------------------------------------------------------------------
def getFieldClass( theField ):
    return __getClass__( theField, theField.type() )


#---------------------------------------------------------------------------
def extractVolFields( theMesh ) :
    aName2VolField = dict()
    
    from Foam.OpenFOAM import IOobjectList, fileName
    anIOobjects = IOobjectList( theMesh, fileName( theMesh.time().timeName() ) )

    for anIOobject in anIOobjects :
        aClassName = anIOobject.headerClassName()

        aClass = getIOobjectClass( anIOobject )
        aField = aClass( anIOobject, theMesh )
        aName2VolField[ str( anIOobject.name() ) ] = aField
        pass

    return aName2VolField


#---------------------------------------------------------------------------
def modifyScalarField( theField ) :
    import random
    for cellI in range( theField.size() ) :
        theField[ cellI ] = 1.0e7 * random.random()
        pass
    
    return theField


#---------------------------------------------------------------------------
def modifyVectorField( theField ) :
    import random
    from Foam.OpenFOAM import vector
    for cellI in range( theField.size() ) :
        array = [ 1.0e7 * random.random() for i in range( 3 ) ]
        theField[ cellI ] = vector( array[ 0 ], array[ 1 ], array[ 2 ] )
        pass
    
    return theField


#--------------------------------------------------------------------------------------
def __mapVolField__( theSourceField, meshToMeshInterp, patchMap, cuttingPatches ) :
    aTargetField = None
    
    meshTarget = meshToMeshInterp.toMesh()
    aFieldName = theSourceField.name()

    aFieldClass = getFieldClass( theSourceField )
    if aFieldClass.ext_foundObject( meshTarget, aFieldName ) :
        aTargetField = aFieldClass.ext_lookupObject( meshTarget, aFieldName )
    else:
        from Foam.OpenFOAM import IOobject, fileName    
        aTargetIOobject = IOobject( aFieldName,
                                    fileName( meshTarget.time().timeName() ),
                                    meshTarget,
                                    IOobject.READ_IF_PRESENT,
                                    IOobject.AUTO_WRITE )
        if aTargetIOobject.headerOk() :
            aTargetField = aFieldClass( aTargetIOobject, meshTarget )
            pass
        pass
    
    from Foam import fvc
    meshSource = meshToMeshInterp.fromMesh()
    ext_Info() << tab <<"interpolating \"" << aFieldName << "\"" << nl
    ext_Info() << tab << tab << "source : \"" << meshSource.time().path() << "\"" << nl
    ext_Info() << tab << tab << tab << fvc.domainIntegrate( theSourceField ) << nl
    ext_Info() << tab << tab << tab << theSourceField.ext_min() << nl
    ext_Info() << tab << tab << tab << theSourceField.ext_max() << nl

    from Foam.sampling import meshToMesh
    meshToMeshInterp.interpolate( aTargetField, theSourceField, meshToMesh.INTERPOLATE )

    ext_Info() << tab << tab << "target : \"" << meshTarget.time().path() << "\"" << nl
    ext_Info() << tab << tab << tab << fvc.domainIntegrate( aTargetField ) << nl
    ext_Info() << tab << tab << tab << aTargetField.ext_min() << nl
    ext_Info() << tab << tab << tab << aTargetField.ext_max() << nl
   
    return aTargetField


#--------------------------------------------------------------------------------------
import Foam.OpenFOAM


#--------------------------------------------------------------------------------------
def mapVolField( theSourceField, meshSource, meshTarget,
                 # List of pairs of source/target patches for mapping
                 patchMap = Foam.OpenFOAM.wordHashTable(),
                 # List of target patches cutting the source domain (these need to be
                 # handled specially e.g. interpolated from inernal values)
                 cuttingPatches = Foam.OpenFOAM.wordList()
                 ) :
    from Foam.sampling import meshToMesh
    meshToMeshInterp = meshToMesh( meshSource, meshTarget, patchMap, cuttingPatches )

    return __mapVolField__( theSourceField, meshToMeshInterp, patchMap, cuttingPatches )


#--------------------------------------------------------------------------------------
def mapVolFields( name2VolField, meshSource, meshTarget,
                  patchMap = Foam.OpenFOAM.wordHashTable(),
                  # List of target patches cutting the source domain (these need to be
                  # handled specially e.g. interpolated from inernal values)
                  cuttingPatches = Foam.OpenFOAM.wordList()
                  ) :
    aName2VolField = dict()

    from Foam.sampling import meshToMesh
    meshToMeshInterp = meshToMesh( meshSource, meshTarget, patchMap, cuttingPatches )

    print "\nMapping fields for time", meshSource.time().timeName(), "\n"
    for aSourceField in name2VolField.values() :
        aTargetField = __mapVolField__( aSourceField, meshToMeshInterp, patchMap, cuttingPatches )
        aName2VolField[ str( aTargetField.name() ) ] = aTargetField
        pass
    
    return aName2VolField


#--------------------------------------------------------------------------------------
def main_standalone( argc, argv ):

    from Foam.OpenFOAM.include import setRootCase
    args = setRootCase( argc, argv )

    import os
    root_dir = os.path.join( str( args.rootPath() ), str( args.caseName() ) )

    from Foam.OpenFOAM.include import createMesh
    timeSource = createTime( root_dir, "coarse_mesh" )
    meshSource = createMesh( timeSource )
    
    from Foam.OpenFOAM.include import createMesh
    timeTarget = createTime( root_dir, "fine_mesh" )
    meshTarget = createMesh( timeTarget )

    from Foam.OpenFOAM import wordHashTable, word
    # List of pairs of source/target patches for mapping
    patchMap = wordHashTable()
    #patchMap.insert( word( "lid" ), word( "movingWall" ) )
    
    from Foam.OpenFOAM import wordList, word
    # List of target patches cutting the source domain (these need to be
    # handled specially e.g. interpolated from internal values)
    cuttingPatches = wordList()
    #cuttingPatches = wordList( 1, word( "fixedWalls" ) )

    aName2VolField = extractVolFields( meshSource )

    modifyScalarField( aName2VolField[ 'p' ])
    modifyVectorField( aName2VolField[ 'U' ] )

    aName2VolField = mapVolFields( aName2VolField, meshSource, meshTarget, patchMap, cuttingPatches )

    ext_Info() << "\nEnd\n"

    import os
    return os.EX_OK


#--------------------------------------------------------------------------------------
if __name__ == "__main__" :
    import sys, os
    os._exit( main_standalone( len( sys.argv ), sys.argv ) )
    pass

    
#--------------------------------------------------------------------------------------

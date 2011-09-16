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
def setRootCase( argc, argv ) :
    from Foam.OpenFOAM import argList
    
    args = argList( argc, argv )
    if not args.checkRootCase() :
        import os
        os._exit( os.EX_USAGE )
        pass

    return args


#---------------------------------------------------------------------------
def createTime( args ) :
    from Foam import get_proper_function
    fun = get_proper_function( "Foam.OpenFOAM.include.createTime_impl",
                               "createTime" )
    return fun( args )
     
                    

#---------------------------------------------------------------------------
class getTime( object ):
    """
    C++ orientied mapping for the corresponding functional objects
    """
    def __init__( self, args ):
        self.args = args
        pass
    
    def __call__( self ):
        return createTime( self.args )

    pass


#---------------------------------------------------------------------------
def createMesh( runTime ):
    from Foam.OpenFOAM import ext_Info, nl
    ext_Info() << "Create mesh for time = " << runTime.timeName() << nl << nl

    from Foam.OpenFOAM import Time
    from Foam.OpenFOAM import IOobject, IOobjectHolder
    from Foam.OpenFOAM import fileName
    from Foam.finiteVolume import fvMeshHolder, fvMesh
    
    mesh = fvMeshHolder( IOobjectHolder( fvMesh.defaultRegion.fget(),
                             fileName( runTime.timeName() ),
                             runTime,
                             IOobject.MUST_READ ) )
    
    print repr( mesh )   
    return mesh


#---------------------------------------------------------------------------
def createMeshNoClear( runTime ):
    from Foam.OpenFOAM import ext_Info, nl
    ext_Info() << "Create mesh, no clear-out for time = " << runTime.timeName() << nl << nl

    from Foam.OpenFOAM import Time
    from Foam.OpenFOAM import IOobject, IOobjectHolder
    from Foam.OpenFOAM import fileName
    from Foam.finiteVolume import fvMesh, fvMeshHolder
    
    mesh = fvMeshHolder( IOobjectHolder( fvMesh.defaultRegion.fget(),
                             fileName( runTime.timeName() ),
                             runTime,
                             IOobject.MUST_READ ) )

    return mesh

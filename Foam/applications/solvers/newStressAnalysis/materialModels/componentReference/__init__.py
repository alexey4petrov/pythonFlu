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


#--------------------------------------------------------------------------------
#to use wrapped unit to uncomment next two line and rename class componentReference to componentReference_

#from componentReferenceList_ import *
#componentReferenceList = PtrList_componentReference



#--------------------------------------------------------------------------------
from Foam.template import PtrList_TypeBase
class componentReference( PtrList_TypeBase ):
    def __init__( self, *args ):
        #- Construct from components
        try:
            self._init__with_6_param( *args )
            return
        except AssertionError:
            pass
        #- - Construct from dictionary
        try:
            self._init__with_2_param( *args )
            return
        except AssertionError:
            pass
        
        #- - Construct from self
        try:
            self._init__self( *args )
            return
        except AssertionError:
            pass
        
        raise AssertionError()
        
        
    #-----------------------------------------------------------------------------  
    def _init__with_6_param(self, *args):
        if len(args) != 6:
           raise AssertionError( "len( args ) != 6" )
        
        argc = 0
        from Foam.finiteVolume import fvMesh
        try:
            fvMesh.ext_isinstance( args[ argc ] )
        except TypeError:
            raise AssertionError( "args[ argc ].__class__ != fvMesh" )
        mesh = args[ argc ]; argc +=1
        
        from Foam.OpenFOAM import word
        try:
            patchName = word( str( args[ argc ] ) )
        except ValueError:
           raise AttributeError("The second arg is not string")
        argc +=1
        
        try:
           faceIndex = int( args[ argc ] )
        except ValueError:
           raise AttributeError("The third arg is not label")
        argc +=1
        
        try:
           dir_ = int( args[ argc ] )
        except ValueError:
           raise AttributeError("The fourth arg is not direction")
        if dir_ < 0 or dir_>255:
           raise AttributeError("The fourth arg is not direction") 
        argc +=1
        
        try:
           value = float( args[ argc ] )
        except ValueError:
           raise AttributeError ("The fifth arg is not scalar")
        
        from Foam.OpenFOAM import polyPatchID
        self.patchID_ = polyPatchID( patchName, mesh.boundaryMesh() )
        self.faceIndex_ = faceIndex
        self.dir_ = dir_
        self.value_ = value
        self.checkPatchFace(mesh)
        
        
    #-----------------------------------------------------------------------------
    def _init__with_2_param( self, *args ):
        if len(args) != 2:
           raise AssertionError( "len( args ) != 2" )
        argc = 0
        
        from Foam.finiteVolume import fvMesh
        try:
            fvMesh.ext_isinstance( args[ argc ] )
        except TypeError:
            raise AssertionError( "args[ argc ].__class__ != fvMesh" )
        mesh = args[ argc ]; argc +=1
        
        from Foam.OpenFOAM import dictionary
        try:
            dictionary.ext_isinstance( args[ argc ] )
        except TypeError:
            raise AssertionError( "args[ argc ].__class__ != dictionary" )
        dict_ = args[ argc ]
        PtrList_TypeBase.__init__( self )
        from Foam.OpenFOAM import polyPatchID, word, readLabel, readScalar
        self.patchID_ = polyPatchID( dict_.lookup( word( "patch" ) ), mesh.boundaryMesh() )
        self.faceIndex_ = readLabel( dict_.lookup( word( "face" ) ) )
        self.dir_ = self.getDir( dict_ )
        self.value_ = readScalar( dict_.lookup( word( "value" ) ) )
        self.checkPatchFace(mesh)
    
    
    #----------------------------------------------------------------------------
    def _init__self(self, *args):
        if len(args) != 1:
           raise AssertionError( "len( args ) != 1" )
        
        argc = 0
        if args[ argc ].__class__ != self.__class__:
           raise AssertionError( "args[ argc ].__class__ != self.__class__" )
        clone = args[ argc ]
        
        self.patchID_ = clone.patchID_
        self.faceIndex_ = clone.faceIndex_
        self.dir_ = clone.dir_
        self.value_ = clone.value_
        
        
        
    #------------------------------------------------------------------------------    
    from Foam.template import PtrList_INewBase
    class iNew( PtrList_INewBase ):
        def __init__( self, mesh_ ):
            from Foam.finiteVolume import fvMesh
            try:
               fvMesh.ext_isinstance( mesh_ )
            except TypeError:
               raise AssertionError( "args[ argc ].__class__ != fvMesh" )
            from Foam.template import PtrList_INewBase
            PtrList_INewBase.__init__( self )
            self.mesh_ = mesh_
            pass


    #---------------------------------------------------------------------------------
        def __call__(self, is_):
           try:
              from Foam.OpenFOAM import dictionary
              crDict = dictionary(is_)
              from Foam.template import autoPtr_PtrList_TypeHolder
              return autoPtr_PtrList_TypeHolder( componentReference( self.mesh_, crDict ) )
           except Exception:
              import sys, traceback
              traceback.print_exc( file = sys.stdout )
              pass
    #---------------------------------------------------------------------------------
    
    #- Create direction given a name
    def getDir( self, dict_ ):
        from Foam.OpenFOAM import dictionary
        try:
            dictionary.ext_isinstance( dict_ )
        except TypeError:
            raise AssertionError( "args[ argc ].__class__ != dictionary" )
        
        from Foam.OpenFOAM import word
        dirName = str( word( dict_.lookup( word( "direction" ) ) ) )
        
        if dirName == "x" or dirName == "X":
           from Foam.OpenFOAM import vector
           return vector.X
        elif dirName == "y" or dirName == "Y":
           from Foam.OpenFOAM import vector
           return vector.Y
        elif dirName == "z" or dirName == "Z":
           from Foam.OpenFOAM import vector
           return vector.Z
        else:
           raise IOError("Direction %s not recognize. Use x,y or z " %dirName )
     
     
    #-----------------------------------------------------------------------------
    #- Check if patch face is in range
    def checkPatchFace( self, mesh ):

        from Foam.finiteVolume import fvMesh
        try:
            fvMesh.ext_isinstance( mesh )
        except TypeError:
            raise AssertionError( "args[ argc ].__class__ != fvMesh" )
        
        if not self.patchID_.active() or  self.faceIndex_ >= mesh.boundaryMesh()[self.patchID_.index()].ext_size():
           raise AssertionError ("Non-existing patch or index out of range ")
        
        pass
     
     
    #-----------------------------------------------------------------------------
    # - clone
    def clone( self ):
         return componentReference( self )
    
    #-----------------------------------------------------------------------------
    #- Return patch index
    def patchIndex( self ):
        return self.patchID_.index()
    
    
    #------------------------------------------------------------------------------
    #- Return face index
    def faceIndex( self ):
        return self.faceIndex_
        
    
    #-------------------------------------------------------------------------------
    #- Return direction
    def dir( self ):
        return self.dir_
    
    
    #--------------------------------------------------------------------------------
    #- Return value
    def value( self ):
        return self.value_


#------------------------------------------------------------------------------------

       



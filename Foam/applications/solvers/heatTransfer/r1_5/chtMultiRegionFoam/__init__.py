#!/usr/bin/env python

#--------------------------------------------------------------------------------------
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


#------------------------------------------------------------------------------------
from Foam.OpenFOAM import IOdictionary
class regionProperties( IOdictionary ):
    def __init__( self, runTime ):
        from Foam.OpenFOAM import IOobject, word, fileName
        IOdictionary.__init__( self, IOobject( word( "regionProperties" ), 
                                               fileName( runTime.time().constant() ), 
                                               runTime.db(), 
                                               IOobject.MUST_READ, 
                                               IOobject.NO_WRITE  ) )
        from Foam.OpenFOAM import List_word
        self.fluidRegionNames = List_word( self.lookup( word( "fluidRegionNames" ) ) )
        self.solidRegionNames = List_word( self.lookup( word( "solidRegionNames" ) ) )
	pass
	
    pass


#-------------------------------------------------------------------------------
class coupleManager( object ):
    def __init__( self, *args ):
        try:
            self._init__fvPatch( *args )
            return
        except AssertionError:
            pass
        except Exception:
            import sys, traceback
            traceback.print_exc( file = sys.stdout )
            pass
        
        try:
            self._init__fvPatch__dictionary( *args )
            return
        except AssertionError:
            pass
        except Exception:
            import sys, traceback
            traceback.print_exc( file = sys.stdout )
            pass

        try:
            self._init__self( *args )
            return
        except AssertionError:
            pass
        except Exception:
            import sys, traceback
            traceback.print_exc( file = sys.stdout )
            pass
        
        raise AssertionError()
        pass


#------------------------------
    def  _init__fvPatch( self, *args ):
        if len ( args) != 1 :
           raise AssertionError( "len( args ) != 1" )
        argc = 0

        from Foam.finiteVolume import fvPatch
        try:
            fvPatch.ext_isinstance( args[ argc ] )
        except TypeError:
            raise AssertionError( "args[ argc ].__class__ != fvPatch" )
        patch = args[ argc ]
        
        self.patch_ = patch
        from Foam.OpenFOAM import word
        self.neighbourRegionName_ = word( "undefined-neighbourRegionName" )
        self.neighbourPatchName_ = word( "undefined-neighbourPatchName" )
        self.neighbourFieldName_ = word( "undefined-neighbourFieldName" )
        self.localRegion_ = self.patch_.boundaryMesh().mesh()
        
        return self
        
        
#-------------------------------        
    def _init__fvPatch__dictionary( self, *args ):
        if len ( args ) != 2 :
           raise AssertionError( "len( args ) != 1" )
        argc = 0
        
        from Foam.finiteVolume import fvPatch
        try:
            fvPatch.ext_isinstance( args[ argc ] )
        except TypeError:
            raise AssertionError( "args[ argc ].__class__ != fvPatch" )
        patch = args [ argc ]; argc = argc + 1
        
        from Foam.OpenFOAM import dictionary
        try:
            dictionary.ext_isinstance( args[ argc ] )
        except TypeError:
            raise AssertionError( "args[ argc ].__class__ != dictionary" )
        dict_ = args[ argc ]
        
        self.patch_ = patch
        from Foam.OpenFOAM import word
        self.neighbourRegionName_ = word( dict_.lookup( word( "neighbourRegionName" ) ) )
        self.neighbourPatchName_ = word( dict_.lookup( word( "neighbourPatchName" ) ) )
        self.neighbourFieldName_ = word( dict_.lookup( word( "neighbourFieldName" ) ) )
        self.localRegion_ = self.patch_.boundaryMesh().mesh()
        
        return self


#------------------------------
    def _init__self( self, *args ):
        if len( args ) != 1 :
            raise AssertionError( "len( args ) != 1" )
        argc = 0

        if args[ argc ].__class__ != self.__class__ :
            raise AssertionError( "args[ argc ].__class__ != self.__class__" )
        cm = args[ argc ]
        
        self.patch_ = cm.patch()
        self.neighbourRegionName_ = cm.neighbourRegionName()
        self.neighbourPatchName_ = cm.neighbourPatchName()
        self.neighbourFieldName_ = cm.neighbourFieldName()
        self.localRegion_ = self.patch_.boundaryMesh().mesh()
        
        return self


#------------------------------
    def checkCouple( self ):
        from Foam.OpenFOAM import ext_Info, nl
        ext_Info() << "neighbourRegionName_ = " << self.neighbourRegionName_ << nl
        ext_Info() << "neighbourPatchName_ = " << neighbourPatchName_ << nl
        ext_Info() << "neighbourFieldName_ = " << neighbourFieldName_ << nl
        
        nPatch = self.neighbourPatch()
        
        if self.patch_.size() != nPatch.size():
           ext_Info() << "FATAL ERROR in" << "Foam::coupleManager::checkCouple()" << "Unequal patch sizes:" << nl \
                      << "    patch name (size) = " << self.patch_.name() << "(" << self.patch_.size() << ")" << nl \
                      << "    neighbour patch name (size) = " << nPatch.name() << "(" << self.patch_.size() << ")" << nl
           import os 
           os.abort()
        pass


#------------------------------
    def coupleToObj( self ):
        nPatch = self.neighbourPatch()
        from Foam.OpenFOAM import OFstream
        obj = OFstream( self.patch_.name() + "_to_" + nPatch.name() + word( "_couple.obj" ) )
        
        c1 = self.patch_.Cf()
        c2 = self.neighbourPatch().Cf()
        
        from Foam.OpenFOAM import ext_Info, nl
        if c1.size() != c2.size():
           ext_Info() << "FATAL ERROR in" << "coupleManager::coupleToObj() const"<< "Coupled patches are of unequal size:" << nl \
                      << "    patch0 = " << self.patch_.name() << "(" << patch_.size() <<  ")" << nl \
                      << "    patch1 = " << nPatch.name() << "(" << nPatch.size() <<  ")" << nl
           import os
           os.abort()
        
        for i in range( c1.size):
            obj << "v " << c1[i].x() << " " << c1[i].y() << " " << c1[i].z() << nl \
                << "v " << c2[i].x() << " " << c2[i].y() << " " << c2[i].z() << nl \
                << "l " << (2*i + 1) << " " << (2*i + 2) << nl
            pass
        
        pass
        

#------------------------------
    def writeEntries( self, os ):
        from Foam.OpenFOAM import word, token, nl
        
        os.writeKeyword( word( "neighbourRegionName" ) )
        os << self.neighbourRegionName_ << token( token.END_STATEMENT ) << nl
        os.writeKeyword( word( "neighbourPatchName" ) )
        os << self.neighbourPatchName_ << token( token.END_STATEMENT ) << nl
        os.writeKeyword( word( "neighbourFieldName" ) )
        os << self.neighbourFieldName_ << token( token.END_STATEMENT ) << nl
         
        pass


#-------------------------------
    def patch( self ):
        return self.patch_


#--------------------------------
    def neighbourRegionName( self ):
        return self.neighbourRegionName_


#--------------------------------
    def neighbourPatchName( self ):
        return self.neighbourPatchName_


#---------------------------------
    def neighbourFieldName( self ):
        return self.neighbourFieldName_


#----------------------------------
    def neighbourRegion( self ):
        from Foam.finiteVolume import fvMesh
        return fvMesh.ext_lookupObject( self.localRegion_.parent(), self.neighbourRegionName_ ) 
        
        
#---------------------------------
    def neighbourPatchID( self ):
        return self.neighbourRegion().boundaryMesh().findPatchID( self.neighbourPatchName_ )


#----------------------------------
    def neighbourPatch( self ):
        return self.neighbourRegion().boundary()[ self.neighbourPatchID() ]

#----------------------------------
    def neighbourPatchField( self, Type ):
        from Foam.template import GeometricFieldTypeName
        from Foam.finiteVolume import volMesh
        an_expr = "from Foam.finiteVolume import %s" %GeometricFieldTypeName( Type, volMesh )
        exec( an_expr )
        an_expr = "res = %s.ext_lookupPatchField( self.neighbourPatch(), self.neighbourFieldName_ )" %GeometricFieldTypeName( Type, volMesh )
        exec( an_expr )
        return res


#--------------------------------------------------------------------------------------

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
## See https://vulashaka.svn.sourceforge.net/svnroot/vulashaka/pyfoam
##
## Author : Alexey PETROV
##


#---------------------------------------------------------------------------
from Foam.OpenFOAM import ext_Info, ext_Warning, ext_SeriousError, tab, nl


#------------------------------------------------------------------------------------
from Foam.finiteVolume import fixedGradientFvPatchVectorField

#------------------------------------------------------------------------------------
class tractionDisplacementFvPatchVectorField( fixedGradientFvPatchVectorField ):
    def __init__( self, *args ):
        try:
            self._init__fvPatch__DimensionedField_vector_volMesh( *args )
            return
        except AssertionError:
            pass
        except Exception:
            import sys, traceback
            traceback.print_exc( file = sys.stdout )
            pass
        
        try:
            self._init__fvPatch__DimensionedField_vector_volMesh__dictionary( *args )
            return
        except AssertionError:
            pass
        except Exception:
            import sys, traceback
            traceback.print_exc( file = sys.stdout )
            pass

        try:
            self._init__self__fvPatch__DimensionedField_vector_volMesh__mapper( *args )
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
        
        try:
            self._init__self__DimensionedField_vector_volMesh( *args )
            return
        except AssertionError:
            pass
        except Exception:
            import sys, traceback
            traceback.print_exc( file = sys.stdout )
            pass
        
        raise AssertionError()

    #------------------------------------------------------------------------------------
    def type( self ) :
        from Foam.OpenFOAM import word
        return word( "tractionDisplacement" )
    
    #------------------------------------------------------------------------------------
    def _init__fvPatch__DimensionedField_vector_volMesh( self, *args ) :
        if len( args ) != 2 :
            raise AssertionError( "len( args ) != 2" )
        argc = 0

        from Foam.OpenFOAM import fvPatch
        if args[ argc ].__class__ != fvPatch :
            raise AssertionError( "args[ argc ].__class__ != fvPatch" )
        p = args[ argc ]; argc += 1
        
        from Foam.OpenFOAM import DimensionedField_vector_volMesh
        if args[ argc ].__class__ != DimensionedField_vector_volMesh :
            raise AssertionError( "args[ argc ].__class__ != DimensionedField_vector_volMesh" )
        iF = args[ argc ]; argc += 1
        
        fixedGradientFvPatchVectorField.__init__( self, p, iF )
        
        from Foam.OpenFOAM import word
        from Foam.OpenFOAM import vectorField, vector, scalarField
        self.UName_ = word( "undefined" )
        self.rheologyName_ = word( "undefined" )
        self.traction_ = vectorField( p.size(), vector.zero)
        self.pressure_ = scalarField(p.size(), 0.0)
                
        return self


    #------------------------------------------------------------------------------------
    def _init__fvPatch__DimensionedField_vector_volMesh__dictionary( self, *args ) :
        if len( args ) != 3 :
            raise AssertionError( "len( args ) != 3" )
        argc = 0
        
        from Foam.OpenFOAM import fvPatch
        if args[ argc ].__class__ != fvPatch :
            raise AssertionError( "args[ argc ].__class__ != fvPatch" )
        p = args[ argc ]; argc += 1

        from Foam.OpenFOAM import DimensionedField_vector_volMesh
        if args[ argc ].__class__ != DimensionedField_vector_volMesh :
            raise AssertionError( "args[ argc ].__class__ != DimensionedField_vector_volMesh" )
        iF = args[ argc ]; argc += 1
        
        from Foam.OpenFOAM import dictionary
        if args[ argc ].__class__ != dictionary :
            raise AssertionError( "args[ argc ].__class__ != dictionary" )
        dict_ = args[ argc ]; argc += 1

        fixedGradientFvPatchVectorField.__init__( self,p, iF )
       
        from Foam.OpenFOAM import word
        from Foam.OpenFOAM import vectorField, vector, scalarField
        self.UName_ = word( dict_.lookup( word( "U" ) ) )
        self.rheologyName_ = word( dict_.lookup( word( "rheology" ) ) )
        self.traction_ = vectorField( word( "traction" ) , dict_, p.size() )
        self.pressure_ = scalarField( word( "pressure" ), dict_, p.size() )
        ext_Info() << "rf: " << self.rheologyName_ << nl
                
        return self

        
    #------------------------------------------------------------------------------------
    def _init__self__fvPatch__DimensionedField_vector_volMesh__mapper( self, *args ) :
        if len( args ) != 4 :
            raise AssertionError( "len( args ) != 4" )
        argc = 0
        
        if args[ argc ].__class__ != self.__class__ :
            raise AssertionError( "args[ argc ].__class__ != self.__class__" )
        tdpvf = args[ argc ]; argc += 1
        
        from Foam.OpenFOAM import fvPatch
        if args[ argc ].__class__ != fvPatch :
            raise AssertionError( "args[ argc ].__class__ != fvPatch" )
        p = args[ argc ]; argc += 1

        from Foam.OpenFOAM import DimensionedField_vector_volMesh
        if args[ argc ].__class__ != DimensionedField_vector_volMesh :
            raise AssertionError( "args[ argc ].__class__ != DimensionedField_vector_volMesh" )
        iF = args[ argc ]; argc += 1
        
        from Foam.finiteVolume import fvPatchFieldMapper
        if args[ argc ].__class__ != dictionary :
            raise AssertionError( "args[ argc ].__class__ != dictionary" )
        mapper = args[ argc ]; argc += 1
        
        fixedGradientFvPatchVectorField.__init__( self, tdpvf, p, iF, mapper )
        
        from Foam.OpenFOAM import word
        from Foam.OpenFOAM import vectorField, scalarField
        self.UName_ = tdpvf.UName_
        self.rheologyName_ = tdpvf.rheologyName_
        self.traction_ = vectorField( tdpvf.traction_ , mapper )
        self.pressure_ = scalarField( tdpvf.pressure_ , mapper )
        
        return self


    #------------------------------------------------------------------------------------
    def _init__self( self, *args ) :
        if len( args ) != 1 :
            raise AssertionError( "len( args ) != 1" )
        argc = 0
        
        if args[ argc ].__class__ != self.__class__ :
            raise AssertionError( "args[ argc ].__class__ != self.__class__" )
        tdpvf = args[ argc ]; argc += 1
        
        fixedGradientFvPatchVectorField.__init__( self, tdpvf )

        from Foam.OpenFOAM import vectorField, scalarField
        self.UName_ = tdpvf.UName_
        self.rheologyName_ = tdpvf.rheologyName_
        self.traction_ = tdpvf.traction_ 
        self.pressure_ = tdpvf.pressure_ 
        
        return self
        
        
    #------------------------------------------------------------------------------------
    def _init__self__DimensionedField_vector_volMesh( self, *args ) :
        if len( args ) != 2 :
            raise AssertionError( "len( args ) != 2" )
        argc = 0
  
        if args[ argc ].__class__ != self.__class__ :
            raise AssertionError( "args[ argc ].__class__ != self.__class__" )
        tdpvf = args[ argc ]; argc += 1
        
        from Foam.OpenFOAM import DimensionedField_vector_volMesh
        if args[ argc ].__class__ != DimensionedField_vector_volMesh :
            raise AssertionError( "args[ argc ].__class__ != DimensionedField_vector_volMesh" )
        iF = args[ argc ]; argc += 1
        
        fixedGradientFvPatchVectorField.__init__( self, tdpvf, iF )
        
        from Foam.OpenFOAM import vectorField, scalarField
        self.UName_ = tdpvf.UName_
        self.rheologyName_ = tdpvf.rheologyName_
        self.traction_ = tdpvf.traction_
        self.pressure_ = tdpvf.pressure_ 
        
        return self
        
        
    #------------------------------------------------------------------------------------
    def clone( self, *args ) :
        try:
            return self._clone( *args )
        except AssertionError:
            pass
        except Exception:
            import sys, traceback
            traceback.print_exc( file = sys.stdout )
            pass
        
        try:
            return self._clone__DimensionedField_vector_volMesh( *args )
        except AssertionError :
            pass
        except Exception:
            import sys, traceback
            traceback.print_exc( file = sys.stdout )
            pass
        
        raise AssertionError()
           
    #------------------------------------------------------------------------------------
    def _clone( self, *args ) :
        if len( args ) != 0 :
            raise AssertionError( "len( args ) != 0" )

        from Foam.finiteVolume import tmp_fvPatchField_vector
        obj = tractionDisplacementFvPatchVectorField( self )

        return tmp_fvPatchField_vector( obj )
        
    #------------------------------------------------------------------------------------
    def _clone__DimensionedField_vector_volMesh( self, *args ) :
        if len( args ) != 1 :
            raise AssertionError( "len( args ) != 1" )
        argc = 0

        from Foam.OpenFOAM import DimensionedField_vector_volMesh
        if args[ argc ].__class__ != DimensionedField_vector_volMesh :
            return AssertionError( "args[ argc ].__class__ != DimensionedField_vector_volMesh" )
        iF = args[ argc ]; argc += 1

        from Foam.finiteVolume import tmp_fvPatchField_vector
        obj = tractionDisplacementFvPatchVectorField( self, iF )
        print repr( obj )
        return tmp_fvPatchField_vector( obj )
    
    
    #------------------------------------------------------------------------------------
    def traction(self):
        return self.traction_
    
    
    #-------------------------------------------------------------------------------------
    def pressure(self):
        return self.pressure_
    
    
    #-------------------------------------------------------------------------------------
    def autoMap(self, *args):
        print "in autoMap"
        if len( args ) != 1 :
            raise AssertionError( "len( args ) != 1" )
        argc = 0
        m = args[ argc ]

        from Foam.finiteVolume import fixedGradientFvPatchVectorField
        fixedGradientFvPatchVectorField.autoMap( self, m )
        self.traction_.autoMap(m)
        self.pressure_.autoMap(m)
        pass 
    
    
    #---------------------------------------------------------------------------------------
    # Reverse-map the given fvPatchField onto this fvPatchField
    def rmap( self, *args ):
        print "in rmap"
        if len( args ) != 1 :
            raise AssertionError( "len( args ) != 1" )
        argc = 0
        ptf = args[ argc ]; argc += 1
        addr = args[ argc ]
        
        from Foam.finiteVolume import fixedGradientFvPatchVectorField
        fixedGradientFvPatchVectorField.rmap( self, ptf, addr )

        dmptf = fixedGradientFvPatchVectorField.ext_refCast( ptf )
        
        self.traction_.rmap(dmptf.traction_, addr);
        self.pressure_.rmap(dmptf.pressure_, addr);
        pass
        
        
    #---------------------------------------------------------------------------------------
    def updateCoeffs(self):
        print "in updateCoeffs"
        


    #----------------------------------------------------------------------------------------
from Foam.template import getfvPatchFieldConstructorToTableBase_vector

class fvPatchFieldConstructorToTable_tractionDispl( getfvPatchFieldConstructorToTableBase_vector() ):

    def __init__( self ):
        aBaseClass = getfvPatchFieldConstructorToTableBase_vector()
        aBaseClass.__init__( self )
        
        from Foam.OpenFOAM import word 
        aBaseClass.init( self, self, word( "tractionDisplacement" ) )
        pass
    
    def new_patch( self, p, iF ):
        from Foam.finiteVolume import tmp_fvPatchField_vector
        obj = tractionDisplacementFvPatchVectorField( p,iF )

        return tmp_fvPatchField_vector( obj )

    def new_patchMapper( self, ptf , p, iF, m ):
        from Foam.finiteVolume import tmp_fvPatchField_vector
        obj = tractionDisplacementFvPatchVectorField( ptf , p, iF, m )

        return tmp_fvPatchField_vector( obj )
    
    def new_dictionary( self, p, iF, dict_ ):
        from Foam.finiteVolume import tmp_fvPatchField_vector
        obj = tractionDisplacementFvPatchVectorField( p, iF, dict_ )
        
        return tmp_fvPatchField_vector( obj )
            
    pass

      
#----------------------------------------------------------------------------------------------------------
tractionDisp_fvPatchFieldConstructorToTable = fvPatchFieldConstructorToTable_tractionDispl()


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


#---------------------------------------------------------------------------
from Foam.finiteVolume import fixedValueFvPatchScalarField
from Foam.OpenFOAM import word


#----------------------------------------------------------------------------
class fixedRhoFvPatchScalarField( fixedValueFvPatchScalarField ):
    typeName = word( "fixedRho" )
    def __init__( self, *args ):
        try:
            self._init__fvPatch__DimensionedField_scalar_volMesh( *args )
            return
        except AssertionError:
            pass
        except Exception:
            import sys, traceback
            traceback.print_exc( file = sys.stdout )
            pass
       
        try:
            self._init__fvPatch__DimensionedField_scalar_volMesh__dictionary( *args )
            return
        except AssertionError:
            pass
        except Exception:
            import sys, traceback
            traceback.print_exc( file = sys.stdout )
            pass
       
        try:
            self._init__self__fvPatch__DimensionedField_scalar_volMesh__fvPatchFieldMapper( *args )
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
            self._init__self__DimensionedField_scalar_volMesh( *args )
            return
        except AssertionError:
            pass
        except Exception:
            import sys, traceback
            traceback.print_exc( file = sys.stdout )
            pass
            
        raise AssertionError()
        pass
    #--------------------------------
    def _init__fvPatch__DimensionedField_scalar_volMesh( self, *args ):
        if len( args ) != 2 :
            raise AssertionError( "len( args ) != 2" )
        argc = 0
        
        from Foam.finiteVolume import fvPatch
        try:
            fvPatch.ext_isinstance( args[ argc ] )
        except TypeError:
            raise AssertionError( "args[ argc ].__class__ != fvPatch" )
        p = args[ argc ]; argc += 1    
        
        from Foam.finiteVolume import DimensionedField_scalar_volMesh
        try:
            DimensionedField_scalar_volMesh.ext_isinstance( args[ argc ] )
        except TypeError:
            raise AssertionError( "args[ argc ].__class__ != DimensionedField_scalar_volMesh" )
        iF = args[ argc ]
        fixedValueFvPatchScalarField.__init__( self, p, iF )
        
        return self
    
    
    #-------------------------------------
    def _init__fvPatch__DimensionedField_scalar_volMesh__dictionary( self, *args ):
        if len( args ) != 3 :
           raise AssertionError( "len( args ) != 3" )
        argc = 0
        
        from Foam.finiteVolume import fvPatch        
        try:
            fvPatch.ext_isinstance( args[ argc ] )
        except TypeError:
            raise AssertionError( "args[ argc ].__class__ != fvPatch" )
        p = args[ argc ]; argc += 1
        
        from Foam.finiteVolume import DimensionedField_scalar_volMesh
        try:
            DimensionedField_scalar_volMesh.ext_isinstance( args[ argc ] )
        except TypeError:
            raise AssertionError( "args[ argc ].__class__ != DimensionedField_scalar_volMesh" )
        iF = args[ argc ]; argc += 1
        
        from Foam.OpenFOAM import dictionary
        try:
            dictionary.ext_isinstance( args[ argc ] )
        except TypeError:
            raise AssertionError( "args[ argc ].__class__ != dictionary" )
        dict_ = args[ argc ]
        
        fixedValueFvPatchScalarField.__init__( self, p, iF, dict_ )
        
        return self
        
        
    #--------------------------
    def _init__self__fvPatch__DimensionedField_scalar_volMesh__fvPatchFieldMapper( self, *args ):
        if len( args ) != 4 :
           raise AssertionError( "len( args ) != 4" )
        argc = 0
       
        if args[ argc ].__class__ != self.__class__ :
           raise AssertionError( "args[ argc ].__class__ != self.__class__" )
        ptf = args[ argc ]; argc += 1
       
        from Foam.finiteVolume import fvPatch        
        try:
            fvPatch.ext_isinstance( args[ argc ] )
        except TypeError:
            raise AssertionError( "args[ argc ].__class__ != fvPatch" )
        p = args[ argc ]; argc += 1
       
        from Foam.finiteVolume import DimensionedField_scalar_volMesh
        try:
            DimensionedField_scalar_volMesh.ext_isinstance( args[ argc ] )
        except TypeError:
           raise AssertionError( "args[ argc ].__class__ != DimensionedField_scalar_volMesh" )
        iF = args[ argc ]; argc += 1
       
        from Foam.finiteVolume import fvPatchFieldMapper
        try:
            fvPatchFieldMapper.ext_isinstance( args[ argc ] )
        except TypeError:
            raise AssertionError( "args[ argc ].__class__ != fvPatchFieldMapper" )
        mapper = args[ argc ]
        
        fixedValueFvPatchScalarField.__init__( self, ptf, p, iF, mapper )
        
        return self
        
    #------------------------
    def _init__self( self, *args ):
        if len( args ) != 1 :
           raise AssertionError( "len( args ) != 1" )
        argc = 0
        
        if args[ argc ].__class__ != self.__class__ :
           raise AssertionError( "args[ argc ].__class__ != self.__class__" )
        tppsf = args[ argc ]; argc += 1
        
        fixedValueFvPatchScalarField.__init__( self, tppsf )
        
        return self
    
    
    #---------------------------
    def _init__self__DimensionedField_scalar_volMesh( self, *args ):
        if len( args ) != 2 :
           raise AssertionError( "len( args ) != 2" )
        argc = 0
        
        if args[ argc ].__class__ != self.__class__ :
           raise AssertionError( "args[ argc ].__class__ != self.__class__" )
        tppsf = args[ argc ]; argc += 1
        
        from Foam.finiteVolume import DimensionedField_scalar_volMesh        
        try:
            DimensionedField_scalar_volMesh.ext_isinstance( args[ argc ] )
        except TypeError:
            raise AssertionError( "args[ argc ].__class__ != DimensionedField_scalar_volMesh" )
        iF = args[ argc ]; argc += 1
        
        fixedValueFvPatchScalarField.__init__( self, tppsf, iF )
        
        return self
    
    
    #--------------------------------
    def type( self ):
        return word("fixedRho")
    
    
    #--------------------------------
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
            return self._clone__DimensionedField_scalar_volMesh( *args )
        except AssertionError :
            pass
        except Exception:
            import sys, traceback
            traceback.print_exc( file = sys.stdout )
            pass
    
    
    #----------------------------------
    def _clone( self, *args ):
        if len( args ) != 0 :
            raise AssertionError( "len( args ) != 0" )

        from Foam.finiteVolume import tmp_fvPatchField_scalar
        obj = fixedRhoFvPatchScalarField( self )

        return tmp_fvPatchField_scalar( obj )
        
    
    #-----------------------------------
    def _clone__DimensionedField_scalar_volMesh( self, *args ):
        if len( args ) != 1 :
           raise AssertionError( "len( args ) != 1" )
        argc = 0
        
        from Foam.finiteVolume import DimensionedField_scalar_volMesh        
        try:
            DimensionedField_scalar_volMesh.ext_isinstance( args[ argc ] )
        except TypeError:
            raise AssertionError( "args[ argc ].__class__ != DimensionedField_scalar_volMesh" )
        iF = args[ argc ]; argc += 1
        
        from Foam.finiteVolume import tmp_fvPatchField_scalar
        obj = fixedRhoFvPatchScalarField( self, iF )

        return tmp_fvPatchField_scalar( obj )
    
    
    #-----------------------------------
    def updateCoeffs( self ):
        try:
           if self.updated():
              return
           from Foam.finiteVolume import volScalarField
           psip = volScalarField.ext_lookupPatchField(self.patch(), word( "psi" ) )
           pp = volScalarField.ext_lookupPatchField( self.patch(), word( "p" ) )
           self == ( psip * pp )

           fixedValueFvPatchScalarField.updateCoeffs( self )
        except Exception, exc:
            import sys, traceback
            traceback.print_exc( file = sys.stdout )
            raise exc
        
        pass
              
        
#--------------------------------------------------------------------------------------
from Foam.template import getfvPatchFieldConstructorToTableBase_scalar
class fvPatchFieldConstructorToTable_fixedRho( getfvPatchFieldConstructorToTableBase_scalar() ):
    def __init__( self ):
        aBaseClass = getfvPatchFieldConstructorToTableBase_scalar()
        aBaseClass.__init__( self )
        
        from Foam.OpenFOAM import word 
        aBaseClass.init( self, self, word( "fixedRho" ) )
        pass
    
        
    #-----------------
    def new_patch( self, p, iF ):
        from Foam.finiteVolume import tmp_fvPatchField_scalar
        obj = fixedRhoFvPatchScalarField( p,iF )

        return tmp_fvPatchField_scalar( obj )
    
    
    #-----------------
    def new_patchMapper( self, ptf , p, iF, m ):
        from Foam.finiteVolume import tmp_fvPatchField_scalar
        obj = fixedRhoFvPatchScalarField( ptf , p, iF, m )

        return tmp_fvPatchField_scalar( obj )
    
    
    #---------------------
    def new_dictionary( self, p, iF, dict_ ):
        from Foam.finiteVolume import tmp_fvPatchField_scalar
        obj = fixedRhoFvPatchScalarField( p, iF, dict_ )

        return tmp_fvPatchField_scalar( obj )
            
    pass

      
#----------------------------------------------------------------------------------------------------------
fixedRho_fvPatchFieldConstructorToTable = fvPatchFieldConstructorToTable_fixedRho()

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


#-------------------------------------------------------------------------------
from Foam.finiteVolume import fixedValueFvPatchScalarField

#-------------------------------------------------------------------------------
class solidWallTemperatureCoupledFvPatchScalarField( fixedValueFvPatchScalarField ):
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
            self._init__self__DimensionedField_scalar_volMesh( *args )
            return
        except AssertionError:
            pass
        except Exception:
            import sys, traceback
            traceback.print_exc( file = sys.stdout )
            pass
            
        raise AssertionError()


    #------------------------------------------------------------------------------
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
        
        fixedValueFvPatchScalarField.__init__( p, iF )
        from Foam.applications.solvers.heatTransfer.r1_5.chtMultiRegionFoam import coupleManager
        self.coupleManager_ = coupleManager( p )
        self.KName_ = word( "undefined-K" )
        
        return self


    #------------------------------------------------------------------------------
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
        
        fixedValueFvPatchScalarField.__init__( self, p, iF )
        from Foam.applications.solvers.heatTransfer.r1_5.chtMultiRegionFoam import coupleManager
        self.coupleManager_ = coupleManager( p, dict_ )
        from Foam.OpenFOAM import word
        self.KName_ = word( dict_.lookup( word( "K" ) ) )
        
        if dict_.found( word( "value" ) ):
           from Foam.finiteVolume import fvPatchScalarField
           from Foam.OpenFOAM import scalarField
           fvPatchScalarField.ext_assign( self, scalarField( word( "value" ), dict_, p.size() ) )
           pass
        else:
           self.evaluate()
           pass
        
        return self


    #-----------------------------------------------------------------------------
    def _init__self__fvPatch__DimensionedField_scalar_volMesh__fvPatchFieldMapper( self, *args ):
        if len( args ) != 3 :
            raise AssertionError( "len( args ) != 3" )
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
        print "in the constructor's"
        from Foam.finiteVolume import fvPatchFieldMapper
        try:
            fvPatchFieldMapper.ext_isinstance( args[ argc ] )
        except TypeError:
            raise AssertionError( "args[ argc ].__class__ != fvPatchFieldMapper" )
        mapper = args[ argc ]
        
        fixedValueFvPatchScalarField.__init__( self, ptf, p, iF, mapper )
        self.coupleManager_ = ptf.coupleManager_
        self.KName_ = ptf.KName_
        
        return self


    #-----------------------------------------------------------------------------
    def _init__self__DimensionedField_scalar_volMesh( self, *args ):
        if len( args ) != 2 :
            raise AssertionError( "len( args ) != 2" )
        argc = 0

        if args[ argc ].__class__ != self.__class__ :
            raise AssertionError( "args[ argc ].__class__ != self.__class__" )
        wtcsf = args[ argc ]; argc += 1
        
        from Foam.finiteVolume import DimensionedField_scalar_volMesh        
        try:
            DimensionedField_scalar_volMesh.ext_isinstance( args[ argc ] )
        except TypeError:
            raise AssertionError( "args[ argc ].__class__ != DimensionedField_scalar_volMesh" )
        iF = args[ argc ]; argc += 1
        
        fixedValueFvPatchScalarField.__init__( self, wtcsf, iF )
        self.coupleManager_ = wtcsf.coupleManager_
        self.KName_ = wtcsf.KName_
        
        return self


    #-----------------------------------------------------------------------------
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
            
            
    #------------------------------------------------------------------------------
    def type( self ):
        from Foam.OpenFOAM import word
        return word("solidWallTemperatureCoupled")
        
        
    #------------------------------------------------------------------------------
    def _clone( self, *args ) :
        if len( args ) != 0 :
            raise AssertionError( "len( args ) != 0" )

        from Foam.finiteVolume import tmp_fvPatchField_scalar
        obj = solidWallTemperatureCoupledFvPatchScalarField( self )

        return tmp_fvPatchField_scalar( obj )
    
    
    #------------------------------------------------------------------------------
    def _clone__DimensionedField_scalar_volMesh( self, *args ) :
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
        obj = solidWallTemperatureCoupledFvPatchScalarField( self, iF )
        
        return tmp_fvPatchField_scalar( obj )
        
        
    #------------------------------------------------------------------------------
    def updateCoeffs( self ):
        try:  
           if self.updated():
              return

           from Foam.OpenFOAM import scalar
           neighbourField = self.coupleManager_.neighbourPatchField( scalar )
        
           self == neighbourField
        
           fixedValueFvPatchScalarField.updateCoeffs( self )
        except Exception, exc:
            import sys, traceback
            traceback.print_exc( file = sys.stdout )
            raise exc
        
        pass
    
    
    #------------------------------------------------------------------------------
    def write( self, os ):
        try:
           from Foam.finiteVolume import fvPatchScalarField
           fvPatchScalarField.write( self, os)
           self.coupleManager_.writeEntries( os )
           from Foam.OpenFOAM import word, token, nl
           os.writeKeyword( word( "K" ) ) << self.KName_ << token( token.END_STATEMENT ) << nl
           self.writeEntry( word( "value" ), os )
           pass
        except Exception, exc:
            import sys, traceback
            traceback.print_exc( file = sys.stdout )
            raise exc
    
    #------------------------------------------------------------------------------
    def flux( self ):
        try: 
           from Foam.finiteVolume import volScalarField
           Kw = volScalarField.ext_lookupPatchField( self.patch(), self.KName_ )
           Tw = self
        
           return Tw.ext_snGrad()*self.patch().magSf()*Kw
        except Exception, exc:
            import sys, traceback
            traceback.print_exc( file = sys.stdout )
            raise exc

    pass    
        
#----------------------------------------------------------------------------------
from Foam.template import getfvPatchFieldConstructorToTableBase_scalar
class fvPatchFieldConstructorToTable_solidWallTemperatureCoupled( getfvPatchFieldConstructorToTableBase_scalar() ):
    def __init__( self ):
        aBaseClass = getfvPatchFieldConstructorToTableBase_scalar()
        aBaseClass.__init__( self )
        
        from Foam.OpenFOAM import word 
        aBaseClass.init( self, self, word( "solidWallTemperatureCoupled" ) )
        pass
    
        
    #-----------------
    def new_patch( self, p, iF ):
        from Foam.finiteVolume import tmp_fvPatchField_scalar
        obj = solidWallTemperatureCoupledFvPatchScalarField( p,iF )

        return tmp_fvPatchField_scalar( obj )
    
    
    #-----------------
    def new_patchMapper( self, ptf , p, iF, m ):
        from Foam.finiteVolume import tmp_fvPatchField_scalar
        obj = solidWallTemperatureCoupledFvPatchScalarField( ptf , p, iF, m )

        return tmp_fvPatchField_scalar( obj )
    
    
    #---------------------
    def new_dictionary( self, p, iF, dict_ ):
        from Foam.finiteVolume import tmp_fvPatchField_scalar
        obj = solidWallTemperatureCoupledFvPatchScalarField( p, iF, dict_ )

        return tmp_fvPatchField_scalar( obj )
            
    pass

      
#----------------------------------------------------------------------------------------------------------
solidWallTemperatureCoupled_fvPatchFieldConstructorToTable = fvPatchFieldConstructorToTable_solidWallTemperatureCoupled()

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
from Foam.OpenFOAM import ext_Info, ext_Warning, ext_SeriousError, tab, nl

#------------------------------------------------------------------------------------
from Foam.finiteVolume import mixedFvPatchScalarField

class solidWallMixedTemperatureCoupledFvPatchScalarField( mixedFvPatchScalarField ):
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
            self._init__self__DimensionedField_scalar_volMesh( *args )
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
        return word( "solidWallMixedTemperatureCoupled" )
    
    #------------------------------------------------------------------------------------
    def _init__fvPatch__DimensionedField_scalar_volMesh( self, *args ) :
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
        iF = args[ argc ]; argc += 1
        
        mixedFvPatchScalarField.__init__( self, p, iF )
        
        from Foam.OpenFOAM import word
        self.neighbourFieldName_ = word( "undefined-neighbourFieldName" ) 
        self.KName_ = word( "undefined-K" )
        
        self.refValue().ext_assign( 0.0 )
        self.refGrad().ext_assign( 0.0 )
        self.valueFraction().ext_assign( 1.0 )
        
        return self
        
    #------------------------------------------------------------------------------------
    def _init__fvPatch__DimensionedField_scalar_volMesh__dictionary( self, *args ) :
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
        dict_ = args[ argc ]; argc += 1
        
        mixedFvPatchScalarField.__init__( self, p, iF )
        from Foam.OpenFOAM import word
        self.neighbourFieldName_ = word( dict_.lookup( word( "neighbourFieldName" ) ) )
        self.KName_ = word( dict_.lookup( word( "K" ) ) )
       
        from Foam.finiteVolume import fvPatchScalarField
        from Foam.OpenFOAM import word, scalarField, readBool
        fvPatchScalarField.ext_assign( self, scalarField( word( "value" ), dict_, p.size() ) )
        
        if dict_.found( word( "refValue" ) ) :
            #Full restart
            self.refValue().ext_assign( scalarField( word( "refValue" ), dict_, p.size() ) )
            self.refGrad().ext_assign( scalarField( word( "refGradient" ), dict_, p.size() ) )
            self.valueFraction().ext_assign( scalarField( word( "valueFraction" ), dict_, p.size() ) )
        else:
            # Start from user entered data. Assume fixedValue.
            self.refValue().ext_assign( self )
            self.refGrad().ext_assign( 0.0 )
            self.valueFraction().ext_assign( 1.0 )
            pass

        return self

        
    #------------------------------------------------------------------------------------
    def _init__self__DimensionedField_scalar_volMesh( self, *args ) :
        if len( args ) != 2 :
            raise AssertionError( "len( args ) != 3" )
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

        mixedFvPatchScalarField.__init__( self, wtcsf, iF )

        self.neighbourFieldName_ = wtcsf.neighbourFieldName_ 
        self.KName_ = wtcsf.KName_
        
        return self
        
    #------------------------------------------------------------------------------------
    def write( self, os ) :
        mixedFvPatchScalarField.write( self, os )

        from Foam.OpenFOAM import keyType, word, token
        os.writeKeyword( keyType( word( "neighbourFieldName" ) ) ) << self.neighbourFieldName_ << token( token.END_STATEMENT ) << nl
        os.writeKeyword( keyType( word( "K" ) ) ) << self.KName_ << token( token.END_STATEMENT ) << nl
        pass


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
            return self._clone__DimensionedField_scalar_volMesh( *args )
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

        from Foam.finiteVolume import tmp_fvPatchField_scalar
        obj = solidWallMixedTemperatureCoupledFvPatchScalarField( self )

        return tmp_fvPatchField_scalar( obj )
        
    #------------------------------------------------------------------------------------
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
        obj = solidWallMixedTemperatureCoupledFvPatchScalarField( self, iF )
        
        return tmp_fvPatchField_scalar( obj )
        
    #------------------------------------------------------------------------------------
    def K( self ) :
      from Foam.finiteVolume import volScalarField
      return volScalarField.ext_lookupPatchField( self.patch(), self.KName_ )

    
    #-------------------------------------------------------------------------------------
    def updateCoeffs( self ) :
        try:
            if self.updated() :
                return
            
            from Foam.meshTools import directMappedPatchBase
            mpp = directMappedPatchBase.ext_refCast( self.patch().patch() )
            
            nbrMesh = mpp.sampleMesh()

            from Foam.finiteVolume import fvMesh
            nbrPatch = fvMesh.ext_refCast( nbrMesh ).boundary()[ mpp.samplePolyPatch().index() ]
            
            # Force recalculation of mapping and schedule
            distMap = mpp.map()
            
            intFld = self.patchInternalField()
            
            from Foam.finiteVolume import volScalarField
            nbrField = solidWallMixedTemperatureCoupledFvPatchScalarField.ext_refCast( volScalarField.ext_lookupPatchField( nbrPatch, self.neighbourFieldName_ ) )
            
            #Swap to obtain full local values of neighbour internal field
            nbrIntFld = nbrField.patchInternalField()
            
            from Foam.OpenFOAM import mapDistribute, Pstream
            mapDistribute.distribute( Pstream.defaultCommsType.fget(), 
                                      distMap.schedule(), 
                                      distMap.constructSize(), 
                                      distMap.subMap(),       #what to send
                                      distMap.constructMap(), #what to receive
                                      nbrIntFld() )
            
            # Swap to obtain full local values of neighbour K*delta
            nbrKDelta = nbrField.K()*nbrPatch.deltaCoeffs()
            mapDistribute.distribute( Pstream.defaultCommsType.fget(), 
                                      distMap.schedule(), 
                                      distMap.constructSize(), 
                                      distMap.subMap(),       #what to send
                                      distMap.constructMap(), #what to receive
                                      nbrKDelta() ) 
            
            myKDelta = self.K()*self.patch().deltaCoeffs()
            
            # Both sides agree on
            # - temperature : (myKDelta*fld + nbrKDelta*nbrFld)/(myKDelta+nbrKDelta)
            # - gradient    : (temperature-fld)*delta
            # We've got a degree of freedom in how to implement this in a mixed bc.
            # (what gradient, what fixedValue and mixing coefficient)
            # Two reasonable choices:
            # 1. specify above temperature on one side (preferentially the high side)
            #    and above gradient on the other. So this will switch between pure
            #    fixedvalue and pure fixedgradient
            # 2. specify gradient and temperature such that the equations are the
            #    same on both sides. This leads to the choice of
            #    - refGradient = zero gradient
            #    - refValue = neighbour value
            #    - mixFraction = nbrKDelta / (nbrKDelta + myKDelta())
            
            self.refValue().ext_assign( nbrIntFld )
            self.refGrad().ext_assign( 0.0 )
            self.valueFraction().ext_assign( nbrKDelta / ( nbrKDelta + myKDelta() ) )
            
            mixedFvPatchScalarField.updateCoeffs( self )


            if self.debug: 
              Q = ( self.K() * self.patch().magSf() * self.snGrad() ).gSum()


              ext_Info ()<< patch().boundaryMesh().mesh().name()  << ":" \
                         << patch().name() << ':' << self.dimensionedInternalField().name() << " <- " \
                         << nbrMesh.name() << ':' << nbrPatch.name() << ':' << self.dimensionedInternalField().name() << " :" \
                         << " heat[W]:"  << Q << " walltemperature "\
                         << " min:" << self.gMin() << " max:" << self.gMax() << " avg:" << self.gAverage() << nl
              pass           
            pass
        except Exception, exc:
            import sys, traceback
            traceback.print_exc( file = sys.stdout )
            raise exc
        pass
    
    #-------------------------------------------------------------------------------------
    pass


#------------------------------------------------------------------------------------
from Foam.template import getfvPatchFieldConstructorToTableBase_scalar

class fvPatchFieldConstructorToTable_WallMixed( getfvPatchFieldConstructorToTableBase_scalar() ):

    def __init__( self ):
        aBaseClass = getfvPatchFieldConstructorToTableBase_scalar()
        aBaseClass.__init__( self )
        
        from Foam.OpenFOAM import word 
        aBaseClass.init( self, self, word( "solidWallMixedTemperatureCoupled" ) )
        pass
    
    def new_patch( self, p, iF ):
        from Foam.finiteVolume import tmp_fvPatchField_scalar
        obj = solidWallMixedTemperatureCoupledFvPatchScalarField( p,iF )

        return tmp_fvPatchField_scalar( obj )

    def new_patchMapper( self, ptf , p, iF, m ):
        from Foam.finiteVolume import tmp_fvPatchField_scalar
        obj = solidWallMixedTemperatureCoupledFvPatchScalarField( ptf , p, iF, m )

        return tmp_fvPatchField_scalar( obj )
    
    def new_dictionary( self, p, iF, dict_ ):
        from Foam.finiteVolume import tmp_fvPatchField_scalar
        obj = solidWallMixedTemperatureCoupledFvPatchScalarField( p, iF, dict_ )
        return tmp_fvPatchField_scalar( obj )
            
    pass

      
#----------------------------------------------------------------------------------------------------------
WallMixed_fvPatchFieldConstructorToTable = fvPatchFieldConstructorToTable_WallMixed()


#----------------------------------------------------------------------------------------------------------

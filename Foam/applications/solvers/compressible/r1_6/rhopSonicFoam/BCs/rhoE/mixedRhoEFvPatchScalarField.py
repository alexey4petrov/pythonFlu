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
from Foam.OpenFOAM import ext_Info, ext_Warning, ext_SeriousError, tab, nl, word

#------------------------------------------------------------------------------------
from Foam.finiteVolume import mixedFvPatchScalarField

class mixedRhoEFvPatchScalarField( mixedFvPatchScalarField ):
    typeName = word( "mixedRhoE" )
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

    #------------------------------------------------------------------------------------
    def type( self ) :
        from Foam.OpenFOAM import word
        return word( "mixedRhoE" )
    
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
        self.refValue().ext_assign( 0.0 )
        self.refGrad().ext_assign( 0.0 )
        self.valueFraction().ext_assign( 0.0 )
       
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
        
        if dict_.found( word( "value" ) ):
           self.ext_assign( scalarField( word( "value" ), dict_, p.size() ) )
           pass
        else:
           self.ext_assign( self.patchInternalField() )
           pass
        
        self.refValue().ext_assign( self )
        self.refGrad().ext_assign( 0.0 )
        self.valueFraction().ext_assign( 0.0 )

        return self

        
    #------------------------------------------------------------------------------------
    def _init__self__DimensionedField_scalar_volMesh( self, *args ) :
        if len( args ) != 2 :
            raise AssertionError( "len( args ) != 3" )
        argc = 0

        if args[ argc ].__class__ != self.__class__ :
            raise AssertionError( "args[ argc ].__class__ != self.__class__" )
        ptpsf = args[ argc ]; argc += 1
        
        from Foam.finiteVolume import DimensionedField_scalar_volMesh        
        try:
            DimensionedField_scalar_volMesh.ext_isinstance( args[ argc ] )
        except TypeError:
            raise AssertionError( "args[ argc ].__class__ != DimensionedField_scalar_volMesh" )
        iF = args[ argc ]; argc += 1

        mixedFvPatchScalarField.__init__( self, ptpsf, iF )

        return self
        
        
    #-------------------------------------------------------------------------------------
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
        
        mixedFvPatchScalarField.__init__( self, ptf, p, iF, mapper )
        
        return self
    #------------------------
    def _init__self( self, *args ):
        if len( args ) != 1 :
           raise AssertionError( "len( args ) != 1" )
        argc = 0
        
        if args[ argc ].__class__ != self.__class__ :
           raise AssertionError( "args[ argc ].__class__ != self.__class__" )
        ptpsf = args[ argc ]; argc += 1
        
        mixedFvPatchScalarField.__init__( self, ptpsf )
        
        return self
    
        
    #------------------------------------------------------------------------------------
    def write( self, os ) :
        from Foam.finiteVolume import fvPatchScalarField
        fvPatchScalarField.write( self, os )
        
        from Foam.OpenFOAM import keyType, word, token
        
        os.writeKeyword( keyType( word( "valueFraction" ) ) ) << self.valueFraction() << token( token.END_STATEMENT ) << nl
        os.writeKeyword( keyType( word( "refValue" ) ) ) << self.refValue() << token( token.END_STATEMENT ) << nl
        os.writeKeyword( keyType( word( "refGrad" ) ) ) << self.refGrad() << token( token.END_STATEMENT ) << nl
        
        self.writeEntry( word( "value" ), os );
        
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
        obj = mixedRhoEFvPatchScalarField( self )

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
        obj = mixedRhoEFvPatchScalarField( self, iF )
        
        return tmp_fvPatchField_scalar( obj )
    
    
    #-------------------------------------------------------------------------------------
    def autoMap(self, *args):
        if len( args ) != 1 :
            raise AssertionError( "len( args ) != 1" )
        argc = 0
        m = args[ argc ]

        from Foam.finiteVolume import mixedFvPatchScalarField
        mixedFvPatchScalarField.autoMap( self, m )
        pass 
        
   
    #-------------------------------------------------------------------------------------
    def rmap(self, *args):
        if len( args ) != 2 :
            raise AssertionError( "len( args ) != 2" )
        argc = 0
        ptf = args[ argc ]; args = args + 1
        addr = args[ argc ]

        from Foam.finiteVolume import mixedFvPatchScalarField
        mixedFvPatchScalarField.rmap( self, ptf, addr )
        pass 
    
    
    #------------------------------------------------------------------------------------
    def updateCoeffs( self ) :
        try:
            
            if self.updated() :
               return
            from Foam.finiteVolume import volScalarField
            from Foam.OpenFOAM import word
            rhop = volScalarField.ext_lookupPatchField( self.patch(), word( "rho" ) )
            from Foam.finiteVolume import volVectorField            
            rhoUp =volVectorField.ext_lookupPatchField( self.patch(), word( "rhoU" ) )
            
            T = volScalarField.ext_lookupObject( self.db(), word( "T" ) )
            patchi = self.patch().index()
            Tp = T.ext_boundaryField()[patchi] 
            
            Tp.evaluate()

            from Foam.OpenFOAM import IOdictionary
            thermodynamicProperties = IOdictionary.ext_lookupObject( self.db(), word( "thermodynamicProperties" ) )
            
            from Foam.OpenFOAM import dimensionedScalar
            Cv = dimensionedScalar( thermodynamicProperties.lookup( word( "Cv" ) ) )
                   
            self.valueFraction().ext_assign( rhop.ext_snGrad() / ( rhop.ext_snGrad() -  rhop * self.patch().deltaCoeffs()  ) )
            self.refValue().ext_assign( 0.5 * rhop * ( rhoUp / rhop ).magSqr() )

            self.refGrad().ext_assign( rhop * Cv.value() * Tp.ext_snGrad() +\
                                       ( self.refValue() - ( 0.5 * rhop.patchInternalField()\
                                                          * ( rhoUp.patchInternalField() /rhop.patchInternalField() ).magSqr() ) ) * self.patch().deltaCoeffs() )
            mixedFvPatchScalarField.updateCoeffs( self )
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

class fvPatchFieldConstructorToTable_mixedRhoE( getfvPatchFieldConstructorToTableBase_scalar() ):

    def __init__( self ):
        aBaseClass = getfvPatchFieldConstructorToTableBase_scalar()
        aBaseClass.__init__( self )
        
        from Foam.OpenFOAM import word 
        aBaseClass.init( self, self, word( "mixedRhoE" ) )
        pass
    
    def new_patch( self, p, iF ):
        from Foam.finiteVolume import tmp_fvPatchField_scalar
        obj = mixedRhoEFvPatchScalarField( p,iF )

        return tmp_fvPatchField_scalar( obj )

    def new_patchMapper( self, ptf , p, iF, m ):
        from Foam.finiteVolume import tmp_fvPatchField_scalar
        obj = mixedRhoEFvPatchScalarField( ptf , p, iF, m )

        return tmp_fvPatchField_scalar( obj )
    
    def new_dictionary( self, p, iF, dict_ ):
        from Foam.finiteVolume import tmp_fvPatchField_scalar
        obj = mixedRhoEFvPatchScalarField( p, iF, dict_ )
        return tmp_fvPatchField_scalar( obj )
            
    pass

      
#----------------------------------------------------------------------------------------------------------
mixedRhoE_fvPatchFieldConstructorToTable = fvPatchFieldConstructorToTable_mixedRhoE()


#----------------------------------------------------------------------------------------------------------

#!/usr/bin/env python

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

#----------------------------------------------------------------------------
from Foam.applications.solvers.newStressAnalysis.materialModels.rheologyModel.rheologyLaws import rheologyLaw


#----------------------------------------------------------------------------
class multiMaterial( rheologyLaw, list ):
    def __init__( self, name, sigma, dict_ ):
        from Foam.OpenFOAM import word, dictionary
        from Foam.finiteVolume import volSymmTensorField
        if name.__class__ != word :
           raise AttributeError("name.__class__ !== word")
           
        if  sigma.__class__ != volSymmTensorField :
            raise AttributeError("sigma.__class__ != volSymmTensorField")
            
        if dict_.__class__ != dictionary :
           raise AttributeError("dict_.__class__ != dictionary")

        rheologyLaw.__init__(self, name, sigma, dict_ )
      
        from Foam.OpenFOAM import IOobject, fileName
        from Foam.finiteVolume import volScalarField
        self.materials_ = volScalarField( IOobject( word( "materials" ),
                                                    fileName( self.mesh().time().timeName() ),
                                                    self.mesh(),
                                                    IOobject.MUST_READ,
                                                    IOobject.AUTO_WRITE ),
                                          self.mesh() )
           
        from Foam.OpenFOAM import PtrList_entry
        lawEntries = PtrList_entry( dict_.lookup( word("laws") ) )
                
        for lawI in range( lawEntries.size() ):
            self.append( rheologyLaw.New( lawEntries[lawI].keyword(), sigma, lawEntries[lawI].dict() ) )
            
        from Foam.OpenFOAM import SMALL
        if self.materials_.ext_min().value() < 0 or self.materials_.ext_max().value() > (len(self) + SMALL):
           raise IOError(" Invalid definition of material indicator field.")
        
        pass
 
           
    #-----------------------------------------------------------------------------------------        
    def type(self):
        from Foam.OpenFOAM import word
        return word( "multiMaterial" )
    
    
    #-----------------------------------------------------------------------------------------    
    #- Calculate indicator field given index
    def indicator( self, i ):
        try:
            arg = int( i )
        except ValueError:
            raise AttributeError ("The i is not int")
        
        mat = self.materials_.internalField()
        
        from Foam.OpenFOAM import scalarField, SMALL
        result = scalarField( mat.size(), 0.0 )
        for matI in range(mat.size()):
            if mat[ matI ] > (i- SMALL) and mat[matI] < (i + 1 - SMALL):
               result[ matI ] = 1.0
        
        return result
     
               
    #-------------------------------------------------------------------------------------------
    #- Return density
    def rho( self, *args):
        if len(args) > 1:
            raise AttributeError("len(args) > 1")
        if len(args) == 1:
            try:
                arg = float(args[0])
            except ValueError:
                raise AttributeError ("The arg is not float")
        
        from Foam.finiteVolume import volScalarField, zeroGradientFvPatchScalarField
        from Foam.OpenFOAM import word, fileName, IOobject, dimensionedScalar, dimDensity
        
        result = volScalarField( IOobject( word( "rho" ),
                                           fileName(self.mesh().time().timeName()),
                                           self.mesh(),
                                           IOobject.NO_READ,
                                           IOobject.NO_WRITE ),
                                 self.mesh(),
                                 dimensionedScalar( word( "zeroRho" ), dimDensity, 0 ),
                                 zeroGradientFvPatchScalarField.typeName )
        
        #Accumulate data for all fields
        from Foam.OpenFOAM import ext_Info 
        
        for lawI in self:
            result.internalField().ext_assign( result.internalField() + self.indicator( self.index( lawI ) ) * lawI.rho().internalField() )
        
        result.correctBoundaryConditions()
        
        return result
    
    
    #-------------------------------------------------------------------------------------------
    #- Return modulus of elasticity
    def E( self, *args):
        if len(args) > 1:
            raise AttributeError("len(args) > 1")
        if len(args) == 1:
            try:
                arg = float(args[0])
            except ValueError:
                raise AttributeError ("The arg is not float")
                
        from Foam.finiteVolume import volScalarField, zeroGradientFvPatchScalarField
        from Foam.OpenFOAM import word, fileName, IOobject, dimensionedScalar, dimForce, dimArea
        
        result = volScalarField( IOobject( word( "E" ),
                                           fileName( self.mesh().time().timeName() ),
                                           self.mesh(),
                                           IOobject.NO_READ,
                                           IOobject.NO_WRITE ),
                                 self.mesh(),
                                 dimensionedScalar( word( "zeroE" ), dimForce/dimArea, 0),
                                 zeroGradientFvPatchScalarField.typeName )
        
        #Accumulate data for all fields
        for lawI in self:
            result.internalField().ext_assign( result.internalField() + \
                                               self.indicator( self.index( lawI ) ) * lawI.E().internalField()  )
            
        result.correctBoundaryConditions()
        
        return result
    
    
    #-------------------------------------------------------------------------------------------
    #- Return Poisson's ratio
    def nu( self, *args):
        if len(args) > 1:
            raise AttributeError("len(args) > 1")
        if len(args) == 1:
            try:
                arg = float(args[0])
            except ValueError:
                raise AttributeError ("The arg is not float")
        
        from Foam.finiteVolume import volScalarField, zeroGradientFvPatchScalarField
        from Foam.OpenFOAM import word, fileName, IOobject, dimensionedScalar, dimless
        
        result = volScalarField( IOobject( word( "nu" ),
                                           fileName( self.mesh().time().timeName() ),
                                           self.mesh(),
                                           IOobject.NO_READ,
                                           IOobject.NO_WRITE ),
                                 self.mesh(),
                                 dimensionedScalar( word( "zeroE" ), dimless, 0),
                                 zeroGradientFvPatchScalarField.typeName )
        
        #Accumulate data for all fields
        for lawI in self:
            result.internalField().ext_assign( result.internalField() + \
                                               self.indicator( self.index( lawI ) ) * lawI.nu().internalField()  )
            
        result.correctBoundaryConditions()
        
        return result


    #-------------------------------------------------------------------------------------------
    #- Return modulus of plasticity
    def Ep( self ):
        from Foam.finiteVolume import volScalarField, zeroGradientFvPatchScalarField
        from Foam.OpenFOAM import word, fileName, IOobject, dimensionedScalar, dimForce, dimArea, GREAT
        
        result = volScalarField( IOobject( word( "Ep" ),
                                           fileName( self.mesh().time().timeName() ),
                                           self.mesh(),
                                           IOobject.NO_READ,
                                           IOobject.NO_WRITE ),
                                 self.mesh(),
                                 dimensionedScalar( wrod( "zeroEp" ), dimForce/dimArea, GREAT),
                                 zeroGradientFvPatchScalarField.typeName )
        
        #Accumulate data for all fields
        for lawI in self.rheologyLawList:
            result.internalField().ext_assign( result.internalField() + \
                                               self.indicator( lawI ) * self.rheologyLawList[ lawI ].Ep().internalField()  )
            
        result.correctBoundaryConditions()
        
        return result


    #-------------------------------------------------------------------------------------------
    #- Return yield stress
    def sigmaY( self ):
        from Foam.finiteVolume import volScalarField, zeroGradientFvPatchScalarField
        from Foam.OpenFOAM import word, fileName, IOobject, dimensionedScalar, dimForce, dimArea, GREAT
        
        result =  volScalarField( IOobject( word( "sigmaY" ),
                                            fileName( self.mesh().time().timeName() ),
                                            self.mesh(),
                                            IOobject.NO_READ,
                                            IOobject.NO_WRITE ),
                                  self.mesh(),
                                  dimensionedScalar( word( "zeroSigmaY" ), dimForce/dimArea, GREAT),
                                  zeroGradientFvPatchScalarField.typeName )
        
        #Accumulate data for all fields
        for lawI in self.rheologyLawList:
            result.internalField().ext_assign( result.internalField() + \
                                               self.indicator( lawI ) * self.rheologyLawList[ lawI ].sigmaY().internalField()  )
            
        result.correctBoundaryConditions()
        
        return result


    #-------------------------------------------------------------------------------------------
    #- Return creep compliance
    def J(self, t):
        try:
            arg = float( t )
        except ValueError:
            raise AttributeError ("The t is not scalar")
            
            
        raise NotImplementedError("J(scalar t)")
    
    
    #-------------------------------------------------------------------------------------------
    #- Correct the rheological model
    def correct( self ):
        for lawI in self:
            lawI.correct()
    
    
    #--------------------------------------------------------------------------------------------

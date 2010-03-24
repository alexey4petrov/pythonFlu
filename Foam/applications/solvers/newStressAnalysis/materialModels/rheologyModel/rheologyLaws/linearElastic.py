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
class linearElastic( rheologyLaw ):
    def __init__( self, name, sigma, dict_ ):
        
        from Foam.OpenFOAM import word, dictionary
        from Foam.finiteVolume import volSymmTensorField
        if name.__class__ != word :
           raise AttributeError("name.__class__ !== word")
           
        if  sigma.__class__ != volSymmTensorField :
            raise AttributeError("sigma.__class__ != volSymmTensorField")
            
        if dict_.__class__ != dictionary :
           raise AttributeError("dict_.__class__ != dictionary")
                    
        rheologyLaw.__init__( self, name, sigma, dict_ )
        
        from Foam.OpenFOAM import dimensionedScalar
        self.rho_ = dimensionedScalar( dict_.lookup(word( "rho" ) ) )
        self.E_ = dimensionedScalar( dict_.lookup( word( "E" ) ) )
        self.nu_ = dimensionedScalar( dict_.lookup( word( "nu" ) ) )
        pass
        
           
    #-----------------------------------------------------------------------------------------        
    def type(self):
        from Foam.OpenFOAM import word
        return word( "linearElastic" )
    
    
    #-----------------------------------------------------------------------------------------        
    #- Return density
    def rho( self, *args ):
        if len(args) > 1:
            raise AttributeError("len(args) > 1")
        if len(args) == 1:
            try:
                arg = float(args[0])
            except ValueError:
                raise AttributeError ("The args is not float")
        
        from Foam.finiteVolume import volScalarField, zeroGradientFvPatchScalarField, tmp_volScalarField
        from Foam.OpenFOAM import word, fileName, IOobject
        
        result = volScalarField( IOobject( word( "rho" ),
                                            fileName( self.mesh().time().timeName() ),
                                            self.mesh(),
                                            IOobject.NO_READ,
                                            IOobject.NO_WRITE ),
                                  self.mesh(),
                                  self.rho_,
                                  zeroGradientFvPatchScalarField.typeName )
        
        result.correctBoundaryConditions()
        
        return result
        
        
    #-----------------------------------------------------------------------------------------        
    #- Return modulus of elasticity
    def E( self, *args ):
        if len(args) > 1:
            raise AttributeError("len(args) > 1")
        if len(args) == 1:
            try:
                arg = float(args[0])
            except ValueError:
                raise AttributeError ("The args is not float")
                
        from Foam.finiteVolume import volScalarField, zeroGradientFvPatchScalarField,tmp_volScalarField
        from Foam.OpenFOAM import word, fileName, IOobject
        result = volScalarField( IOobject( word( "E" ),
                                            fileName( self.mesh().time().timeName() ),
                                            self.mesh(),
                                            IOobject.NO_READ,
                                            IOobject.NO_WRITE ),
                                            self.mesh(),
                                            self.E_,
                                            zeroGradientFvPatchScalarField.typeName )  
        
        result.correctBoundaryConditions()
        
        return result
        

    #-----------------------------------------------------------------------------------------        
     #- Return Poisson's ratio
    def nu( self, *args ):
        if len(args) > 1:
            raise AttributeError("len(args) > 1")
        if len(args) == 1:
            try:
                arg = float(args[0])
            except ValueError:
                raise AttributeError ("The args is not float")
        
        from Foam.finiteVolume import volScalarField, zeroGradientFvPatchScalarField
        from Foam.OpenFOAM import word, fileName, IOobject
        tresult = volScalarField( IOobject( word( "nu" ),
                                            fileName( self.mesh().time().timeName() ),
                                            self.mesh(),
                                            IOobject.NO_READ,
                                            IOobject.NO_WRITE ),
                                            self.mesh(),
                                            self.nu_,
                                            zeroGradientFvPatchScalarField.typeName ) 
        tresult.correctBoundaryConditions()
        
        return tresult


    #-----------------------------------------------------------------------------------------        
    #- Return modulus of plasticity
    def Ep( self ):
        from Foam.finiteVolume import volScalarField, zeroGradientFvPatchScalarField
        from Foam.OpenFOAM import word, fileName, IOobject, dimensionedScalar, dimForce, dimArea
        tresult = volScalarField( IOobject( word( "Ep" ),
                                            fileName( self.mesh().time().timeName() ),
                                            self.mesh(),
                                            IOobject.NO_READ,
                                            IOobject.NO_WRITE ),
                                            self.mesh(),
                                            dimensionedScalar( word( "zeroEp" ), dimForce/dimArea, 0.0),
                                            zeroGradientFvPatchScalarField.typeName )  
        tresult.correctBoundaryConditions()
        
        return tresult


    #-----------------------------------------------------------------------------------------        
    # - - Return yield stress
    def sigmaY( self ):
        from Foam.finiteVolume import volScalarField, zeroGradientFvPatchScalarField
        from Foam.OpenFOAM import word, fileName, IOobject, dimensionedScalar, dimForce, dimArea, GREAT
        tresult = volScalarField( IOobject( word( "sigmaY" ),
                                            fileName( self.mesh().time().timeName() ),
                                            self.mesh(),
                                            IOobject.NO_READ,
                                            IOobject.NO_WRITE ),
                                            self.mesh(),
                                            dimensionedScalar( word( "zeroSigmaY" ), dimForce/dimArea, GREAT),
                                            zeroGradientFvPatchScalarField.typeName ) 
        tresult().correctBoundaryConditions()
        
        return tresult


    #------------------------------------------------------------------------------------------- 
    #- Return creep compliance
    def J(self, t):
         try:
            arg = float( t )
         except ValueError:
                raise AttributeError ("The t is not scalar")
            
            
         raise NotImplementedError("J(scalar t)");
         pass


    #------------------------------------------------------------------------------------------- 
    #- Correct the rheological model
    def correct(self):
         pass

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
class rheologyLaw:
    def __init__( self, name, sigma, dict_ ):
        from Foam.OpenFOAM import word, dictionary
        from Foam.finiteVolume import volSymmTensorField 
        
        if name.__class__ != word :
           raise AttributeError("name.__class__ !== word")
        
        if sigma.__class__ != volSymmTensorField :
           raise AttributeError("sigma.__class__ != volSymmTensorField")
           
        if dict_.__class__ != dictionary :
           raise AttributeError("dict_.__class__ != dictionary")
          
        self.name_ = name
        self.sigma_ = sigma
        pass         
            
            
    #-----------------------------------------------------------------------------------------       
    #- Return name
    def name( self ):
        return self.name_


    #------------------------------------------------------------------------------------------
    #- Return reference to stress field
    def sigma( self ):
        return self.sigma_


    #------------------------------------------------------------------------------------------
    #- Return reference to mesh
    def mesh( self ):
        return self.sigma_.mesh()

        
    #-------------------------------------------------------------------------------------------
    def type( self ) :
        from Foam.OpenFOAM import word
        return word( "rheologyLaw" )
    
        
    #-------------------------------------------------------------------------------------------
    #- Return a reference to the selected rheology model
    @staticmethod
    def New( name, sigma, dict_ ):
        from Foam.OpenFOAM import word, dictionary
        from Foam.finiteVolume import volSymmTensorField 
        if name.__class__ != word :
           raise AttributeError("name.__class__ !== word")
        
        if sigma.__class__ != volSymmTensorField :
           raise AttributeError("sigma.__class__ != volSymmTensorField")
           
        if dict_.__class__ != dictionary :
           raise AttributeError("dict_.__class__ != dictionary")
           
        rheoTypeName = dict_.lookup( word( "type" ) )
        
        from Foam.OpenFOAM import ext_Info, nl
        
        key = str( word( rheoTypeName ) )
        
        ext_Info() << "Selecting rheology model " << key << nl

        from Foam.applications.solvers.newStressAnalysis.materialModels.rheologyModel.rheologyLaws import addDictionaryConstructorTable
        if addDictionaryConstructorTable.dictionaryTable.has_key( key ):

           className = addDictionaryConstructorTable.dictionaryTable[ key ]

           return className( name, sigma, dict_ )
        else:
        
          raise IOError("Unknown rheologyLaw type  - %s.\n " %key )
    
    
    #--------------------------------------------------------------------------------------------
    #- Return density
    def rho( self, *args):
        raise NotImplementedError("It is abstract method")
    
    
    #--------------------------------------------------------------------------------------------
    #- Return modulus of elasticity
    def E( self, *args):
        raise NotImplementedError("It is abstract method")
        
        
    #--------------------------------------------------------------------------------------------
    # - Return Poisson's ratio
    def nu( self, *args):
        raise NotImplementedError("It is abstract method")
    
    
    #--------------------------------------------------------------------------------------------
    # - Return creep compliance
    def J( self, *args):
        raise NotImplementedError("It is abstract method")
        
        
    #--------------------------------------------------------------------------------------------
    # - Return yield stress
    def sigmaY( self, *args):
        raise NotImplementedError("It is abstract method")    
        

    #--------------------------------------------------------------------------------------------
    #- Return plastic modulus
    def Ep( self, *args):
        raise NotImplementedError("It is abstract method")
        
        
    #--------------------------------------------------------------------------------------------
    #- Correct the rheological model
    def correct( self, *args):
        raise NotImplementedError("It is abstract method")    

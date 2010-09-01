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

#----------------------------------------------------------------------------
from Foam.OpenFOAM import IOdictionary
#----------------------------------------------------------------------------

class rheologyModel( IOdictionary ):
    def __init__(self, sigma):
        from Foam.finiteVolume import volSymmTensorField
        try:
            volSymmTensorField.ext_isinstance( sigma )
        except TypeError:
            raise AssertionError( "args[ argc ].__class__ != volSymmTensorField" )
        
        from Foam.OpenFOAM import IOobject, word, fileName
        IOdictionary.__init__(self, IOobject( word( "rheologyProperties" ),
                                              fileName( sigma.time().constant() ),
                                              sigma.db(),
                                              IOobject.MUST_READ,
                                              IOobject.NO_WRITE ) )
        self.sigma_ = sigma
        
        self.typeName = word( "rheologyModel" )
        from Foam.OpenFOAM import Switch
        self.planeStress_ = Switch( self.lookup( word( "planeStress" ) ) )

        from Foam.applications.solvers.newStressAnalysis.materialModels.rheologyModel.rheologyLaws import rheologyLaw
        self.lawPtr_ = rheologyLaw.New( word( "law" ), self.sigma_, self.subDict( word( "rheology" ) ) )
        pass
           
    #-------------------------------------------------------------------------
    def type( self ):
        return self.typeName

        
    #-------------------------------------------------------------------------
    #- Return reference to stress field
    def sigma( self ):
        return self.sigma_

        
    #-------------------------------------------------------------------------
    #- Return true for plane stress
    def planeStress( self ):
        return self.planeStress_
    
       
    #-------------------------------------------------------------------------
    #- Return rheology law
    def law( self ):
        return self.lawPtr_
        
    #-------------------------------------------------------------------------
    #- Return density
    def rho( self, *args ):
        if len(args) > 1:
            raise AttributeError("len(args) > 1")
        if len(args) == 1:
            try:
                arg = float(args[0])
            except ValueError:
                raise AttributeError ("The arg is not float")
        return self.lawPtr_.rho()


    #-------------------------------------------------------------------------
    #- Return first Lame's coefficient
    def mu( self, *args ):
        if len(args) > 1:
            raise AttributeError("len(args) > 1")
        flag = False
        if len(args) == 1:
            try:
                t = float(args[0])
                flag = True
            except ValueError:
                raise AttributeError ("The arg is not float")
                
        if flag: 
            lawE = self.lawPtr_.E( t )
            lawNu = self.lawPtr_.nu( t )
        else:
            lawE = self.lawPtr_.E()
            lawNu = self.lawPtr_.nu()

        
        from Foam.finiteVolume import volScalarField
        from Foam.OpenFOAM import word, fileName, IOobject
        result  = volScalarField( IOobject( word( "mu" ),
                                            fileName( self.sigma_.time().timeName() ),
                                            self.sigma_.db(),
                                            IOobject.NO_READ,
                                            IOobject.NO_WRITE ),
                                  lawE / ( 2.0 * ( 1.0 + lawNu ) ) )
        return result


    #-------------------------------------------------------------------------
    #- Return second Lame's coefficient
    def _lambda( self, *args ):    
        if len(args) > 1:
            raise AttributeError("len(args) > 1")
        flag = False
        if len(args) == 1:
            try:
                arg = float(args[0])
                flag = True
            except ValueError:
                raise AttributeError ("The arg is not float")
        
        if flag: 
            lawE = self.lawPtr_.E( t )
            lawNu = self.lawPtr_.nu( t )
        else:
            lawE = self.lawPtr_.E()
            lawNu = self.lawPtr_.nu()
        
        from Foam.finiteVolume import volScalarField
        from Foam.OpenFOAM import word, fileName, IOobject
        
        if self.planeStress():
           result = volScalarField( IOobject( word( "lambda" ),
                                              fileName( self.sigma_.time().timeName() ),
                                              self.sigma_.db(),
                                              IOobject.NO_READ,
                                              IOobject.NO_WRITE ),
                                    lawNu * lawE / ( ( 1.0 + lawNu ) * ( 1.0 - lawNu ) ) )
        else:
           result = volScalarField( IOobject( word( "lambda" ),
                                              fileName( self.sigma_.time().timeName() ),
                                              self.sigma_.db(),
                                              IOobject.NO_READ,
                                              IOobject.NO_WRITE ),
                                    lawNu * lawE / ( ( 1.0 + lawNu ) * ( 1.0 - 2.0 * lawNu ) ) ) 
        return result
        
        
    #-------------------------------------------------------------------------
    #- Return threeK
    def threeK( self ):
        lawRho = self.lawPtr_.rho()
        lawE = self.lawPtr_.E()
        lawNu = self.lawPtr_.nu()
        
        from Foam.finiteVolume import volScalarField
        from Foam.OpenFOAM import word, fileName, IOobject
        if self.planeStress():
           result = volScalarField( IOobject( word( "threeK" ),
                                              fileName( self.sigma_.time().timeName() ),
                                              self.sigma_.db(),
                                              IOobject.NO_READ,
                                              IOobject.NO_WRITE ),
                                    lawE / ( lawRho * ( 1 - lawNu ) ) )
        else:
           result = volScalarField( IOobject( word( "threeK" ),
                                              fileName( self.sigma_.time().timeName() ),
                                              self.sigma_.db(),
                                              IOobject.NO_READ,
                                              IOobject.NO_WRITE ),
                                    lawE / ( lawRho * ( 1 - 2 * lawNu ) ) )
        return result


    #-------------------------------------------------------------------------
    #- Return yield stress
    def sigmaY( self ):
        self.lawPtr_.sigmaY()

    #-------------------------------------------------------------------------
    #- Return plastic modulus
    def Ep( self ):
        self.lawPtr_.Ep()


    #-------------------------------------------------------------------------
    #- Correct the rheological model
    def correct( self ):
        self.lawPtr_.correct()


    #-------------------------------------------------------------------------
    #- Read rheologyProperties dictionary
    def read( self ):
        from Foam.OpenFOAM import regIOobject
        if regIOobject.read( self ):
           self.lookup("planeStress") >> self.planeStress_
           from Foam.OpenFOAM import word
           from Foam.applications.solvers.newStressAnalysis.materialModels.rheologyModel.rheologyLaws import rheologyLaw
           self.lawPtr_ = rheologyLaw.New( word( "law" ), self.sigma_, self.subDict("rheology"));

           return True 
        else:
           return False


    #----------------------------------------------------------------------------
           

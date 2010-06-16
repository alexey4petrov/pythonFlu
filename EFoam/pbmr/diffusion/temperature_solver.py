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


#--------------------------------------------------------------------------------------
"""
 Temperature calculation dummy control class. Provides moderator and fuel temperatures
 for cross-section calculations
"""


#--------------------------------------------------------------------------------------
from Foam.OpenFOAM import IOdictionary, word
class solver( IOdictionary ) :
    dictionaryName = word( "temperatureCalculation" )
    def __init__( self, mesh, isTransient, powerDensity = None ) :
        from Foam.OpenFOAM import IOobject, fileName
        IOdictionary.__init__( self, IOobject( solver.dictionaryName,
                                               fileName( mesh.time().constant() ),
                                               mesh,
                                               IOobject.MUST_READ,
                                               IOobject.AUTO_WRITE ) )
        self.mesh = mesh

        from Foam.finiteVolume import volScalarField
        self.Tmod = volScalarField( IOobject( word( self.lookup( word( "moderatorTemperature" ) ) ),
                                              fileName( mesh.time().timeName() ),
                                              mesh,
                                              IOobject.MUST_READ,
                                              IOobject.AUTO_WRITE ),
                                    mesh )
        
        self.Tfuel = volScalarField( IOobject( word( self.lookup( word( "fuelTemperature" ) ) ),
                                               fileName( mesh.time().timeName() ),
                                               mesh,
                                               IOobject.MUST_READ,
                                               IOobject.AUTO_WRITE ),
                                     mesh )
        
        from Foam.OpenFOAM import dimensionedScalar
        self.kMod = volScalarField( IOobject( word( "kMod" ),
                                              fileName( mesh.time().timeName() ),
                                              mesh ),
                                    mesh,
                                    dimensionedScalar( self.lookup( word( "moderatorConductivity" ) ) ) )
        
        self.rhoMod = volScalarField( IOobject( word( "rhoMod" ),
                                                fileName( mesh.time().timeName() ),
                                                mesh ),
                                      mesh,
                                      dimensionedScalar( self.lookup( word( "moderatorDensity" ) ) ) )
        
        self.cpMod = volScalarField( IOobject( word( "cpMod" ),
                                               fileName( mesh.time().timeName() ),
                                               mesh ),
                                     mesh,
                                     dimensionedScalar( self.lookup( word( "moderatorSpecificHeat" ) ) ) )

        from Foam.OpenFOAM import readScalar
        self.puebh = readScalar( self.lookup( word( "puebh" ) ) )

        self.heatSrc_ptr = powerDensity

        self.isTransient = isTransient
        pass

    def solve( self ):
        """
        Temperature solution
        """
        print "Solve for moderator temperature"
        
        from Foam import fvm
        tEqn = - fvm.laplacian( self.kMod, self.Tmod ) == self.heatSrc()
        
        if self.isTransient :
            aTmp = self.rhoMod * self.cpMod
            tEqn += fvm.ddt( aTmp(), self.Tmod )
            pass

        solverPerf = tEqn().solve()

        for cellI in range( self.heatSrc().size() ) :
            heatSrc_val = self.heatSrc()[ cellI ]
            Tmod_val = self.Tmod[ cellI ]
            if heatSrc_val > 0 :
                self.Tfuel[ cellI ] = Tmod_val + heatSrc_val * self.puebh
            else:
                self.Tfuel[ cellI ] = 0;
                pass
            pass
        
        return solverPerf.initialResidual()

    def heatSrc( self ):
        if not self.heatSrc_ptr :
            from Foam.finiteVolume import volScalarField
            a_name = word( self.lookup( word( "nuclearHeatSource" ) ) )
            self.heatSrc_ptr = volScalarField.ext_lookupObject( self.mesh, a_name )
            pass

        return self.heatSrc_ptr
        
    pass


#--------------------------------------------------------------------------------------
def main_standalone( argc, argv ):

    from Foam.OpenFOAM.include import setRootCase
    args = setRootCase( argc, argv )

    from Foam.OpenFOAM.include import createTime
    runTime = createTime( args )

    from Foam.OpenFOAM.include import createMesh
    mesh = createMesh( runTime )

    from Foam.OpenFOAM import Switch
    nuclCalc = solver( mesh, Switch( True ) )

    print "End\n"

    import os
    return os.EX_OK


#--------------------------------------------------------------------------------------
if __name__ == "__main__" :
    import sys, os
    os._exit( main_standalone( len( sys.argv ), sys.argv ) )
    pass

    
#--------------------------------------------------------------------------------------


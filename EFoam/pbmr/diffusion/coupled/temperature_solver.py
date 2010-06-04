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

#---------------------------------------------------------------------------
from Foam.OpenFOAM import ext_Info, ext_Warning, ext_SeriousError, tab, nl

#--------------------------------------------------------------------------------------
from EFoam.pbmr.diffusion.temperature_solver import solver as temperature_solver
class solver( temperature_solver ) :
    solverCaseName = "temperature"
    def __init__( self, args, isTransient ) :
        from EFoam.pbmr.diffusion.coupled import createTime
        self.runTime = createTime( args.globalCaseName(), self.solverCaseName )

        from Foam.OpenFOAM.include import createMesh
        mesh = createMesh( self.runTime )
        
        #-----------------------------------------------------------------------
        # The fields should be registerd in the "mesh/objectRegistry" from the begining
        # To be able to treat them as "case-native" ones
        from Foam.finiteVolume import volScalarField
        from Foam.OpenFOAM import IOobject, fileName, word
        powerDensity = volScalarField( IOobject( word( "Q'''" ),
                                                 fileName( mesh.time().timeName() ),
                                                 mesh,
                                                 IOobject.MUST_READ,
                                                 IOobject.AUTO_WRITE ),
                                       mesh )
        
        #-----------------------------------------------------------------------
        temperature_solver.__init__( self, mesh, isTransient, powerDensity )

        pass
    
    def loop( self ):
        return not self.runTime.end() 

    def write( self ):
        self.runTime.write()
        pass

    def solve( self ):
        self.runTime += self.runTime.deltaT()
        ext_Info() << "temperature-solve - " << self.runTime.timeName() << "\n"

        residual = temperature_solver.solve( self )

        return residual, self.Tmod, self.Tfuel

    pass


#--------------------------------------------------------------------------------------
def main_standalone( argc, argv ):

    from Foam.OpenFOAM.include import setRootCase
    args = setRootCase( argc, argv )

    from Foam.OpenFOAM import Switch
    nuclCalc = solver( args, Switch( True ) )

    print "End\n"

    import os
    return os.EX_OK


#--------------------------------------------------------------------------------------
if __name__ == "__main__" :
    import sys, os
    os._exit( main_standalone( len( sys.argv ), sys.argv ) )
    pass

    
#--------------------------------------------------------------------------------------


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
"""
Nuclear calculation control class
"""

#---------------------------------------------------------------------------
from Foam.OpenFOAM import ext_Info, ext_Warning, ext_SeriousError, tab, nl

#--------------------------------------------------------------------------------------
from EFoam.pbmr.diffusion.nuclear_solver import solver as nuclear_solver
class solver( nuclear_solver ) :
    solverCaseName = "nuclear"
    def __init__( self, args, isTransient ) :
        from EFoam.pbmr.diffusion.coupled import createTime
        self.runTime = createTime( args.globalCaseName(), self.solverCaseName )

        from Foam.OpenFOAM.include import createMesh
        mesh = createMesh( self.runTime )
        
        #-----------------------------------------------------------------------
        # Needed by 'crossSectionSets' initialized in the base class
        from Foam.finiteVolume import volScalarField
        from Foam.OpenFOAM import IOobject, fileName, word
        self.Tmod = volScalarField( IOobject( word( "Tmod" ),
                                              fileName( mesh.time().timeName() ),
                                              mesh,
                                              IOobject.MUST_READ,
                                              IOobject.AUTO_WRITE ),
                                    mesh )
    
        self.Tfuel = volScalarField( IOobject( word( "Tfuel" ),
                                               fileName( mesh.time().timeName() ),
                                               mesh,
                                               IOobject.MUST_READ,
                                               IOobject.AUTO_WRITE ),
                                     mesh )
        
        #-----------------------------------------------------------------------
        nuclear_solver.__init__( self, mesh, isTransient)
        pass

    def loop( self ):
        return not self.runTime.end() 

    def write( self ):
        self.runTime.write()
        pass

    def solve( self ):
        self.storeOldTime()
        
        self.runTime += self.runTime.deltaT()
        ext_Info() << "nuclear-solve - " << self.runTime.timeName() << "\n"

        residual = nuclear_solver.solve( self )

        self.writeScalars() # Write time-dependent scalar data to file

        heatProduction = self.nuclField.power()
        powerDensity = heatProduction.powerDensity()

        return residual, powerDensity
    
    pass


#--------------------------------------------------------------------------------------
def main_standalone( argc, argv ):
    from Foam.OpenFOAM.include import setRootCase
    args = setRootCase( argc, argv )

    from Foam.OpenFOAM import Switch
    nuclCalc = solver( args, Switch( True ) )

    keffRes = 0; temRes = 0
    runTime = nuclCalc.runTime

    print "Start of time-dependent calculation"

    runTime += runTime.deltaT()
    while not runTime.end() :
        print "Time =", runTime.timeName(), "\n"
        
        # Nuclear Calculation
        nuclCalc.storeOldTime()
        nuclRes, powerDensity = nuclCalc.solve()
        nuclCalc.writeScalars() # Write time-dependent scalar data to file
        
        # Write restart data
        runTime.write()

        print "ExecutionTime =", runTime.elapsedCpuTime(), "s", \
              "  ClockTime =", runTime.elapsedClockTime(), "s", \
              "\n"
        runTime += runTime.deltaT()
        pass
    
    print "End\n"

    import os
    return os.EX_OK


#--------------------------------------------------------------------------------------
if __name__ == "__main__" :
    import sys, os
    os._exit( main_standalone( len( sys.argv ), sys.argv ) )
    pass

    
#--------------------------------------------------------------------------------------


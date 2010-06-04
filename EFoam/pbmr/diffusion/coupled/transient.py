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
Steady state solver to the multigroup neutron diffusion equation
"""


#--------------------------------------------------------------------------------------
class CoupledTime :
    def __init__( self, the_first_solver, the_second_solver ) :
        self.first_solver = the_first_solver
        self.second_solver = the_second_solver
        self.reference_time = the_first_solver.runTime
        pass
    
    def loop( self ) :
        return self.first_solver.loop() and self.second_solver.loop()

    def write( self ) :
        self.first_solver.write()
        self.second_solver.write()
        pass

    def elapsedCpuTime( self ) :
        return self.reference_time.elapsedCpuTime()
    
    def elapsedClockTime( self ) :
        return self.reference_time.elapsedClockTime()
    
    pass


#--------------------------------------------------------------------------------------
def main_standalone( argc, argv, nuclear_solver_factory, temperature_solver_factory ):

    from Foam.OpenFOAM.include import setRootCase
    args = setRootCase( argc, argv )

    from Foam.OpenFOAM import Switch
    nuclCalc = nuclear_solver_factory( args, Switch( True ) )
    temCalc = temperature_solver_factory( args, Switch( True ) )
    
    keffRes = 0; temRes = 0
    coupledTime = CoupledTime( nuclCalc, temCalc )

    print "Start of time-dependent calculation"
    while True :
        # Nuclear Calculation
        nuclRes, powerDensity = nuclCalc.solve()

        # Passing data from nuclear to temperature calculation
        from Foam.applications.utilities.preProcessing.mapFields import mapVolField
        mapVolField( powerDensity, nuclCalc.mesh, temCalc.mesh )
        
        # Temperature Calculation
        temRes, Tmod, Tfuel = temCalc.solve()

        # Passing data from temperature to nuclear calculation
        from Foam.applications.utilities.preProcessing.mapFields import mapVolField
        mapVolField( Tfuel, temCalc.mesh, nuclCalc.mesh )
        mapVolField( Tmod, temCalc.mesh, nuclCalc.mesh )
        
        # Write restart data
        coupledTime.write()

        print "ExecutionTime =", coupledTime.elapsedCpuTime(), "s", \
              "  ClockTime =", coupledTime.elapsedClockTime(), "s", \
              "\n"

        if not coupledTime.loop() :
            break
        
        pass
    
    print "End\n"

    import os
    return os.EX_OK


#--------------------------------------------------------------------------------------
if __name__ == "__main__" :
    from EFoam.pbmr.diffusion.coupled.nuclear_solver import solver as nuclear_solver
    from EFoam.pbmr.diffusion.coupled.temperature_solver import solver as temperature_solver

    import sys, os
    os._exit( main_standalone( len( sys.argv ), sys.argv, nuclear_solver, temperature_solver ) )
    pass

    
#--------------------------------------------------------------------------------------


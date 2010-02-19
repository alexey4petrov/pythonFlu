#!/usr/bin/env python

#--------------------------------------------------------------------------------------
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
## See https://csrcs.pbmr.co.za/svn/nea/prototypes/reaktor/pyfoam
##
## Author : Alexey PETROV
##


#---------------------------------------------------------------------------
"""
Steady state solver to the multigroup neutron diffusion equation
"""

#--------------------------------------------------------------------------------------
def main_standalone( argc, argv, nuclear_solver_factory, temperature_solver_factory ):

    from Foam.OpenFOAM.include import setRootCase
    args = setRootCase( argc, argv )

    from Foam.OpenFOAM.include import createTime
    runTime = createTime( args )

    from Foam.OpenFOAM.include import createMesh
    mesh = createMesh( runTime )

    from Foam.OpenFOAM import Switch
    nuclCalc = nuclear_solver_factory( mesh, Switch( False ) )
    temCalc = temperature_solver_factory( mesh, Switch( False ) )

    maxOuterIters = 1000; keffTolerance = 1E-10; keffRes = 0; temRes = 0

    print "Start of eigenvalue calculation"
    
    for outerIters in range( maxOuterIters ) :
        print "Outer Iterations =", outerIters

        # Nuclear Calculation
        keffRes = nuclCalc.solve()
        print "k-effective residual =", keffRes

        # Temperature Calculation
        temRes = temCalc.solve()
        print "Temperature residual =", keffRes

        # Check Eigenvalue convergence
        if keffRes < keffTolerance :
            print "Converged!"
            break
        
        pass
    
    # Write restart data
    runTime.setTime( 0, 0 );
    runTime.writeNow();

    print "ExecutionTime =", runTime.elapsedCpuTime(), "s", \
          "  ClockTime =", runTime.elapsedClockTime(), "s", \
          "\n"
    
    print "End\n"

    import os
    return os.EX_OK


#--------------------------------------------------------------------------------------
import sys, os
if __name__ == "__main__" :
    if len( sys.argv ) == 1 :
        sys.argv = [ __file__, "/scratch/petrova/diffusionFoam-run/oecd_simplified_2G", "oecd_simplified_2G" ]
        pass

    from EFoam.pbmr.diffusion import nuclearCalculation
    from EFoam.pbmr.diffusion import temperatureCalculation
    
    from EFoam.pbmr.diffusion.nuclear_solver import solver as nuclear_solver
    from EFoam.pbmr.diffusion.temperature_solver import solver as temperature_solver

    os._exit( main_standalone( len( sys.argv ), sys.argv, nuclear_solver, temperature_solver ) )
    pass

    
#--------------------------------------------------------------------------------------


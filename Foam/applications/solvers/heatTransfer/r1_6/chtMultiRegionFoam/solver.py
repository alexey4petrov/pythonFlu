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


#------------------------------------------------------------------------------------
# To import corresponding plugin first
#from Foam.applications.solvers.heatTransfer.chtMultiRegionFoam import plugin
from Foam.applications.solvers.heatTransfer.r1_6.chtMultiRegionFoam import derivedFvPatchFields


#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
def readPIMPLEControls( runTime ):

    from Foam.finiteVolume import fvSolution
    solutionDict = fvSolution( runTime )
    
    from Foam.OpenFOAM import word,readInt
    pimple = solutionDict.subDict( word( "PIMPLE" ) )
    nOuterCorr = readInt( pimple.lookup( word( "nOuterCorrectors" ) ) )
    
    return nOuterCorr


#--------------------------------------------------------------------------------------
def main_standalone( argc, argv ):

    from Foam.OpenFOAM.include import setRootCase
    args = setRootCase( argc, argv )

    from Foam.OpenFOAM.include import createTime
    runTime = createTime( args )
    
    from Foam.applications.solvers.heatTransfer.r1_6.chtMultiRegionFoam import regionProperties
    rp = regionProperties( runTime )
    
    from Foam.applications.solvers.heatTransfer.r1_6.chtMultiRegionFoam.fluid import createFluidMeshes
    fluidRegions = createFluidMeshes( rp, runTime )

    from Foam.applications.solvers.heatTransfer.r1_6.chtMultiRegionFoam.solid import createSolidMeshes,createSolidField
    solidRegions=createSolidMeshes( rp,runTime )

    from Foam.applications.solvers.heatTransfer.r1_6.chtMultiRegionFoam.fluid import createFluidFields

    thermoFluid, rhoFluid, KFluid, UFluid, phiFluid, gFluid, turbulence, DpDtFluid, initialMassFluid = createFluidFields( fluidRegions, runTime )

    from Foam.applications.solvers.heatTransfer.r1_6.chtMultiRegionFoam.solid import createSolidField
    rhos, cps, rhosCps, Ks, Ts = createSolidField( solidRegions, runTime )
    
    from Foam.applications.solvers.heatTransfer.r1_6.chtMultiRegionFoam.fluid import initContinuityErrs
    cumulativeContErr = initContinuityErrs( fluidRegions.size() )
    
    from Foam.finiteVolume.cfdTools.general.include import readTimeControls
    adjustTimeStep, maxCo, maxDeltaT = readTimeControls( runTime )
    
    from Foam.OpenFOAM import ext_Info, nl

    if fluidRegions.size() :
        from Foam.applications.solvers.heatTransfer.r1_6.chtMultiRegionFoam.fluid import compressubibleMultiRegionCourantNo
        CoNum = compressubibleMultiRegionCourantNo( fluidRegions, runTime, rhoFluid, phiFluid )
                
        from Foam.finiteVolume.cfdTools.general.include import setInitialDeltaT
        runTime = setInitialDeltaT( runTime, adjustTimeStep, maxCo, maxDeltaT, CoNum )
        pass
    
    while runTime.run() :
        adjustTimeStep, maxCo, maxDeltaT = readTimeControls(runTime)

        nOuterCorr = readPIMPLEControls( runTime )
        
        if fluidRegions.size() :
            from Foam.applications.solvers.heatTransfer.r1_6.chtMultiRegionFoam.fluid import compressubibleMultiRegionCourantNo
            CoNum = compressubibleMultiRegionCourantNo( fluidRegions, runTime, rhoFluid, phiFluid )

            from Foam.finiteVolume.cfdTools.general.include import setDeltaT   
            runTime = setDeltaT( runTime, adjustTimeStep, maxCo, maxDeltaT, CoNum )
            pass
        
        runTime.increment()
        ext_Info()<< "Time = " << runTime.timeName() << nl << nl      
                
        if nOuterCorr != 1 :
            for i in range( fluidRegions.size() ):
                from Foam.applications.solvers.heatTransfer.r1_6.chtMultiRegionFoam.fluid import setRegionFluidFields
                mesh, thermo, rho, K, U, phi, g, turb, DpDt, p, psi, h, massIni = \
                      setRegionFluidFields( i, fluidRegions, thermoFluid, rhoFluid, KFluid, UFluid, \
                                            phiFluid, gFluid, turbulence, DpDtFluid, initialMassFluid )
                
                from Foam.applications.solvers.heatTransfer.r1_6.chtMultiRegionFoam.fluid import storeOldFluidFields
                storeOldFluidFields( p, rho )
                pass
            pass
        
        # --- PIMPLE loop
        for oCorr in range( nOuterCorr ):
            for i in range( fluidRegions.size() ):
                ext_Info() << "\nSolving for fluid region " << fluidRegions[ i ].name() << nl

                from Foam.applications.solvers.heatTransfer.r1_6.chtMultiRegionFoam.fluid import setRegionFluidFields
                mesh, thermo, rho, K, U, phi, g, turb, DpDt, p, psi, h, massIni = \
                      setRegionFluidFields( i, fluidRegions, thermoFluid, rhoFluid, KFluid, UFluid, \
                                            phiFluid, gFluid, turbulence, DpDtFluid, initialMassFluid )
                
                from Foam.applications.solvers.heatTransfer.r1_6.chtMultiRegionFoam.fluid import readFluidMultiRegionPIMPLEControls
                pimple, nCorr, nNonOrthCorr, momentumPredictor = readFluidMultiRegionPIMPLEControls( mesh ) 
                
                from Foam.applications.solvers.heatTransfer.r1_6.chtMultiRegionFoam.fluid import solveFluid
                cumulativeContErr = solveFluid( i, mesh, thermo, thermoFluid, rho, K, U, phi, g, h, turb, DpDt, p, psi, \
                                                massIni, oCorr, nCorr, nOuterCorr, nNonOrthCorr, momentumPredictor, cumulativeContErr )
                
                pass
                
            for i in range( solidRegions.size() ):
               ext_Info() << "\nSolving for solid region " << solidRegions[ i ].name() << nl
               
               from Foam.applications.solvers.heatTransfer.r1_6.chtMultiRegionFoam.solid import setRegionSolidFields
               mesh, rho, cp, K, T = setRegionSolidFields( i, solidRegions, rhos, cps, Ks, Ts )
               
               from Foam.applications.solvers.heatTransfer.r1_6.chtMultiRegionFoam.solid import readSolidMultiRegionPIMPLEControls
               pimple, nNonOrthCorr = readSolidMultiRegionPIMPLEControls( mesh )
               
               from Foam.applications.solvers.heatTransfer.r1_6.chtMultiRegionFoam.solid import solveSolid
               solveSolid( mesh, rho, cp, K, T, nNonOrthCorr )
               pass                
            pass
        pass
        runTime.write()

        ext_Info()<< "ExecutionTime = " << runTime.elapsedCpuTime() << " s" \
            << "  ClockTime = " << runTime.elapsedClockTime() << " s" \
            << nl << nl    

    ext_Info() << "End\n"
    
    import os
    return os.EX_OK

    
#--------------------------------------------------------------------------------------
argv = None
import sys, os
from Foam import FOAM_REF_VERSION
if FOAM_REF_VERSION( "==", "010600" ):
    if __name__ == "__main__" :
        argv = sys.argv
        
        if len(argv) > 1 and argv[ 1 ] == "-test":
           argv = None
           test_dir= os.path.join( os.environ[ "PYFOAM_TESTING_DIR" ],'cases', 'local', 'r1.6', 'heatTransfer', 'chtMultiRegionFoam', 'multiRegionHeater' )
           argv = [ __file__, "-case", test_dir ]
           pass
        
        os._exit( main_standalone( len( argv ), argv ) )
        pass
else:
    from Foam.OpenFOAM import ext_Info
    ext_Info() << "\n\n To use this solver, it is necessary to SWIG OpenFOAM-1.6 \n"    
    pass


#--------------------------------------------------------------------------------------


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


#--------------------------------------------------------------------------------------
from Foam.OpenFOAM import IOdictionary, word
class solver( IOdictionary ) :
    dictionaryName = word( "nuclearCalculation" )
    def __init__( self, mesh, isTransient ) :
        from Foam.OpenFOAM import IOobject, fileName
        IOdictionary.__init__( self, IOobject( solver.dictionaryName,
                                               fileName( mesh.time().constant() ),
                                               mesh,
                                               IOobject.MUST_READ,
                                               IOobject.AUTO_WRITE
                                               ))
        from Foam.OpenFOAM import readInt, word
        self.maxInnerIter = readInt( self.lookup( word( "maxIterations" ) ) )
        
        from Foam.OpenFOAM import readScalar, word
        self.solutionTol = readScalar( self.lookup( word( "tolerance" ) ) )

        self.mesh = mesh

        from EFoam.pbmr.diffusion import fissionProducts
        self.products = fissionProducts( mesh )

        from EFoam.pbmr.diffusion import crossSectionSets
        self.sigma = crossSectionSets.New( mesh,
                                           self.products,
                                           IOdictionary( IOobject( word( "crossSectionSets" ),
                                                                   fileName( mesh.time().constant() ),
                                                                   mesh,
                                                                   IOobject.MUST_READ,
                                                                   IOobject.NO_WRITE
                                                                   )))
        from EFoam.pbmr.diffusion import nuclearField
        self.nuclField = nuclearField( mesh, self.sigma() )

        from EFoam.pbmr.diffusion import delayNeutrons
        self.dnField = delayNeutrons( mesh )

        self.isTransient = isTransient

        from Foam.OpenFOAM import dimensionedScalar
        self.requestedPower = dimensionedScalar( self.lookup( word( "requestedPower" ) ) )
        
        from Foam.OpenFOAM import Switch
        self.powerIsFixed = Switch( self.lookup( word( "powerIsFixed" ) ) )

        from Foam.OpenFOAM import OFstream
        self.timeData = OFstream( mesh.time().path() / fileName( "timeData" ) )
        self.timeData.write( "Time \t CPU Time \t Global Power \tk-effective \t omega\n" )
        
        self.isFirstCall = True
        pass

    def solve( self ):
        """
        Inner neutron flux iteration

        Performs the neutron flux inner iteration, the coupled solution of neutron
        flux and neutron poison isotopic concentrations.
        """
        # Update cross-sections
        self.sigma().update()

        # For the first call we must update fission rate and neutron production.
        # This is a workaround for calculated cross-sections, whose values are
        # not set at the time when fission rate and neutron production are
        # first constructed.
        # Todo: Improve... these values should be initialized correctly beforehand
        if self.isFirstCall :
            self.nuclField.updateFissionRate()
            self.nuclField.updateNeutronProduction()
            self.nuclField.updatePower()
            self.isFirstCall = False
            pass

        # Delayed neutrons - update production terms: steady state
        self.dnField.updateProductionTerms( self.isTransient )

        print "Inner neutron flux iteration"
        
        residual = 0.0

        for innerIter in range( self.maxInnerIter ) :
            self.storePrevIter()

            # Fission product poisoning
            self.products.updateConcentrations( self.nuclField, self.isTransient )
            self.nuclField.updateIsotopes()

            # Diffusion Equation solution
            from EFoam.pbmr.diffusion import diffusionSolver
            an_engine = diffusionSolver( self.nuclField,
                                         self.dnField,
                                         self.isTransient )
            
            residual = an_engine.solve().initialResidual()

            # Update the neutronic fields and global reactor parameters
            self.nuclField.updateFissionRate()

            # For fixed power transients & steady-state calculation
            if not self.isTransient or self.powerIsFixed :
                # Update & normalize reactor power
                self.nuclField.power().updatePower( self.nuclField.F() )
                self.nuclField.normalizePower( self.requestedPower )

                # Update production, buckling & k-effective
                self.nuclField.updateNeutronProduction()
                self.nuclField.updateLeakage()
                self.nuclField.updateKeff( self.dnField, self.isTransient )
                pass

            # No inner iteration for steady-state calculations
            if not self.isTransient :
                residual = abs( self.nuclField.globalParam().keff()  - self.nuclField.globalParam().keffPrevIter() )
                break
            
            # Check convergence
            if residual < self.solutionTol :
                # Converged
                print "Converged in", innerIter, "iterations"
                break;

            pass
        
        # Update the neutronic fields and global reactor parameters
        # For fixed power transients, these are calculated during the
        # iteration loop so there is no need to repeat this calculation
        if self.isTransient and not self.powerIsFixed :
            # Update reactor power
            self.nuclField.power().updatePower( self.nuclField.F() )

            # Update production, leakage & inverse reactor period
            self.nuclField.updateNeutronProduction()
            self.nuclField.updateLeakage()
            self.nuclField.globalParam().updateReactorPeriod( self.nuclField )
            pass

        # Updated delayed neutron precursor concentrations: transient
        self.dnField.updateConcentrations( self.nuclField.P(), self.isTransient )

        return residual

    def storeOldTime( self ):
        """
        Store the old time values
        """
        self.nuclField.storeOldTime()
        self.dnField.storeOldTime()
        self.products.storeOldTime()
        pass
    
    def storePrevIter( self ):
        """
        Store the previous iteration values
        """
        self.nuclField.storePrevIter()
        self.dnField.storePrevIter()
        self.products.storePrevIter()
        pass
    
    def writeScalars( self ):
        """
        Write the time-dependent scalar data to file
        """
        self.timeData.write( self.mesh.time().time().value() )
        self.timeData.write( '\t' )
        self.timeData.write( self.mesh.time().elapsedCpuTime() )
        self.timeData.write( '\t' )
        self.timeData.write( self.nuclField.power().globalPower().value() )
        self.timeData.write( '\t' )
        self.timeData.write( self.nuclField.globalParam().keff() )
        self.timeData.write( '\t' )
        self.timeData.write( self.nuclField.globalParam().omega().value() )
        self.timeData.write( '\t' )
        self.timeData.write( '\n' )
        pass
    
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


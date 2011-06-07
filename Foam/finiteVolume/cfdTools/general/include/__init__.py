## pythonFlu - Python wrapping for OpenFOAM C++ API
## Copyright (C) 2010- Alexey Petrov
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
## See http://sourceforge.net/projects/pythonflu
##
## Author : Alexey PETROV
##


#---------------------------------------------------------------------------
def initContinuityErrs():
    cumulativeContErr = 0

    return cumulativeContErr


#---------------------------------------------------------------------------
def ContinuityErrs( phi, runTime, mesh, cumulativeContErr ):
    from Foam import fvc
    contErr = fvc.div(phi)

    sumLocalContErr = runTime.deltaT().value() * contErr.mag().weightedAverage( mesh.V() ).value()

    globalContErr = runTime.deltaT().value() * contErr.weightedAverage( mesh.V() ).value();
        
    cumulativeContErr += globalContErr
    from Foam.OpenFOAM import ext_Info, nl
    ext_Info() << "time step continuity errors : sum local = " << sumLocalContErr << ", global = " << globalContErr \
               << ", cumulative = " << cumulativeContErr << nl
    return cumulativeContErr


#---------------------------------------------------------------------------
def readPISOControls( mesh ):
    from Foam import get_proper_function
    fun = get_proper_function( "Foam.finiteVolume.cfdTools.general.include.readPISOControls_impl",
                               "readPISOControls" )
    return fun( mesh )


#---------------------------------------------------------------------------
def readTimeControls( runTime ):
    from Foam import get_proper_function
    fun = get_proper_function( "Foam.finiteVolume.cfdTools.general.include.readTimeControls_impl",
                               "readTimeControls" )
    return fun( runTime )
    

#----------------------------------------------------------------------------
def setInitialDeltaT( runTime, adjustTimeStep, maxCo, maxDeltaT, CoNum ):
    from Foam.OpenFOAM import SMALL 

    if adjustTimeStep :
        if runTime.timeIndex() == 0:
            if CoNum > SMALL :
                runTime.setDeltaT( min( maxCo * runTime.deltaT().value() / CoNum, maxDeltaT ) )
                pass
            pass
	pass
    
    return runTime         


#------------------------------------------------------------------------------------
def setDeltaT( runTime, adjustTimeStep, maxCo, maxDeltaT, CoNum ):
    from Foam.OpenFOAM import SMALL

    if adjustTimeStep :
        maxDeltaTFact = maxCo/(CoNum + SMALL)
        deltaTFact = min( min( maxDeltaTFact, 1.0 + 0.1 * maxDeltaTFact ), 1.2 )
        runTime.setDeltaT( min( deltaTFact * runTime.deltaT().value(), maxDeltaT ) )
        from Foam.OpenFOAM import ext_Info, nl
        ext_Info() << "deltaT = " << runTime.deltaT().value() << nl
        pass
    
    return runTime


#---------------------------------------------------------------------------------------------
def readSIMPLEControls( mesh ):
    from Foam import get_proper_function
    fun = get_proper_function( "Foam.finiteVolume.cfdTools.general.include.readSIMPLEControls_impl",
                               "readSIMPLEControls" )
                      
    return fun( mesh )


#----------------------------------------------------------------------------------------------    
def readPIMPLEControls( mesh ):
    from Foam.OpenFOAM import Switch
    from Foam.OpenFOAM import word
    from Foam.OpenFOAM import readInt
    
    pimple = mesh.solutionDict().subDict( word( "PIMPLE" ) )
    
    nOuterCorr = readInt( pimple.lookup( word( "nOuterCorrectors" ) ) ) 
    
    nCorr =  readInt( pimple.lookup( word( "nCorrectors" ) ) )
    
    nNonOrthCorr = pimple.lookupOrDefault( word( "nNonOrthogonalCorrectors" ), 0 )

    momentumPredictor = pimple.lookupOrDefault( word( "momentumPredictor" ), Switch( True ) )

    transonic = pimple.lookupOrDefault( word( "transonic" ), Switch( False ) )
    
    return pimple, nOuterCorr, nCorr, nNonOrthCorr, momentumPredictor, transonic


#---------------------------------------------------------------------------------------------
def CourantNo( mesh, phi, runTime ):
    from Foam import get_proper_function
    fun = get_proper_function( "Foam.finiteVolume.cfdTools.general.include.CourantNo_impl",
                               "CourantNo" )
    return fun( mesh, phi, runTime )


#---------------------------------------------------------------------------------------------
def readEnvironmentalProperties( runTime, mesh ):
    from Foam.OpenFOAM import ext_Info, nl
    ext_Info() << "\nReading environmentalProperties" << nl
    
    from Foam.OpenFOAM import IOdictionary, fileName, word, IOobject
    environmentalProperties = IOdictionary( IOobject( word( "environmentalProperties" ),
                                                      fileName( runTime.constant() ),
                                                      mesh,
                                                      IOobject.MUST_READ,
                                                      IOobject.NO_WRITE ) )
    from Foam.OpenFOAM import dimensionedVector
    g = dimensionedVector( environmentalProperties.lookup( word( "g" ) ) )
    
    return g, environmentalProperties


#--------------------------------------------------------------------------------------------
def readGravitationalAcceleration( runTime, mesh):
    from Foam.OpenFOAM import ext_Info,  nl
    ext_Info() << "\nReading g" << nl
    from Foam.OpenFOAM import uniformDimensionedVectorField, IOobject, fileName, word
    
    g = uniformDimensionedVectorField( IOobject( word( "g" ),
                                                 fileName( runTime.constant() ),
                                                 mesh,
                                                 IOobject.MUST_READ,
                                                 IOobject.NO_WRITE ) )
    return g

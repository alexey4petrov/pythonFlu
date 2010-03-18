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
    from Foam import dispatcher, WM_PROJECT_VERSION
    fun = dispatcher( "Foam.finiteVolume.cfdTools.general.include.readPISOControls_impl",
                      "readPISOControls",
                      WM_PROJECT_VERSION() )
    return fun( mesh )


#---------------------------------------------------------------------------
def readTimeControls( runTime ):
    from Foam.OpenFOAM import Switch, word, readScalar, GREAT
    
    adjustTimeStep = Switch( runTime.controlDict().lookup( word( "adjustTimeStep" ) ) )
    maxCo = readScalar( runTime.controlDict().lookup( word( "maxCo" ) ) )
    
    from Foam import WM_PROJECT_VERSION
    if WM_PROJECT_VERSION() <="1.5":
       maxDeltaT = GREAT
       if runTime.controlDict().found( word( "maxDeltaT" ) ):
          maxDeltaT = readScalar( runTime.controlDict().lookup( word( "maxDeltaT" ) ) )
          pass

    if WM_PROJECT_VERSION() >="1.6":
       maxDeltaT = runTime.controlDict().lookupOrDefault( word( "maxDeltaT" ), GREAT, 0, 1 )
       pass
    
    
    
    return adjustTimeStep, maxCo, maxDeltaT


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
    from Foam import dispatcher, WM_PROJECT_VERSION
    fun = dispatcher( "Foam.finiteVolume.cfdTools.general.include.readSIMPLEControls_impl",
                      "readSIMPLEControls",
                      WM_PROJECT_VERSION() )
                      
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
    from Foam.OpenFOAM import Time
    from Foam.finiteVolume import fvMesh
    from Foam.finiteVolume import surfaceScalarField

    CoNum = 0.0;
    meanCoNum = 0.0;

    if mesh.nInternalFaces() :
        from Foam import fvc
        SfUfbyDelta = mesh.deltaCoeffs()*phi.mag()
        CoNum =  ( SfUfbyDelta / mesh.magSf() ).ext_max().value() * runTime.deltaT().value()
        meanCoNum = ( SfUfbyDelta.sum() / mesh.magSf().sum() ).value() * runTime.deltaT().value();
        pass

    from Foam.OpenFOAM import ext_Info, nl
    ext_Info() << "Courant Number mean: " << meanCoNum << " max: " << CoNum<< nl

    return CoNum, meanCoNum


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
    
    return g


#--------------------------------------------------------------------------------------------

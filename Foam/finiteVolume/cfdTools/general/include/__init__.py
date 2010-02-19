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

    sumLocalContErr = runTime.deltaT().value()* contErr().mag().weightedAverage(mesh.V()).value()

    globalContErr = runTime.deltaT().value()* contErr().weightedAverage(mesh.V()).value();
        
    cumulativeContErr += globalContErr
    from Foam.OpenFOAM import ext_Info, nl
    ext_Info() << "time step continuity errors : sum local = " << sumLocalContErr << ", global = " << globalContErr \
               << ", cumulative = " << cumulativeContErr << nl
    return cumulativeContErr


#---------------------------------------------------------------------------
def readPISOControls( mesh ):
    from Foam.OpenFOAM import dictionary
    from Foam.OpenFOAM import readInt
    from Foam.OpenFOAM import Switch
    from Foam.OpenFOAM import word

    piso = dictionary( mesh.solutionDict().subDict( word( "PISO" ) ) )

    nCorr = readInt( piso.lookup( word( "nCorrectors" ) ) )

    nNonOrthCorr = 0;
    if piso.found( word( "nNonOrthogonalCorrectors" ) ) :
        nNonOrthCorr = readInt( piso.lookup( word( "nNonOrthogonalCorrectors" ) ) )
        pass

    momentumPredictor = True;
    if piso.found( word( "momentumPredictor" ) ) :
        momentumPredictor = Switch( piso.lookup( word( "momentumPredictor" ) ) )
        pass
    
    transonic = False;
    if piso.found( word( "transonic" ) ) :
        transonic = Switch( piso.lookup( word( "transonic" ) ) )
        pass

    nOuterCorr = 1;
    if piso.found( word( "nOuterCorrectors" ) ) :
        nOuterCorr = readInt( piso.lookup( word( "nOuterCorrectors" ) ) )

    ddtPhiCorr = False;
    if piso.found( word( "ddtPhiCorr" ) ) :
        ddtPhiCorr = Switch( piso.lookup( word( "ddtPhiCorr" ) ) )
        pass

    return piso, nCorr, nNonOrthCorr, momentumPredictor, transonic, nOuterCorr, ddtPhiCorr


#---------------------------------------------------------------------------
def readTimeControls( runTime ):
    from Foam.OpenFOAM import Switch, word, readScalar, GREAT
    
    adjustTimeStep = Switch( runTime.controlDict().lookup( word( "adjustTimeStep" ) ) )
    maxCo = readScalar( runTime.controlDict().lookup( word( "maxCo" ) ) )
    maxDeltaT = runTime.controlDict().lookupOrDefault( word( "maxDeltaT" ), GREAT, 0, 1 )
    
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
        runTime.setDeltaT( min( deltaTFact*runTime.deltaT().value(), maxDeltaT ) )
        from Foam.OpenFOAM import ext_Info, nl
        ext_Info() << "deltaT = " << runTime.deltaT().value()<<nl
        pass
    
    return runTime


#---------------------------------------------------------------------------------------------
def readSIMPLEControls( mesh ):
    from Foam.OpenFOAM import Switch
    from Foam.OpenFOAM import word
    from Foam import WM_PROJECT_VERSION
    
    simple = mesh.solutionDict().subDict( word( "SIMPLE" ) )
    
    if WM_PROJECT_VERSION <= "1.4.1-dev" :
       from Foam.OpenFOAM import readInt
       nNonOrthCorr = 0
       if ( simple.found( word( "nNonOrthogonalCorrectors" ) ) ):
          nNonOrthCorr = readInt(simple.lookup( word( "nNonOrthogonalCorrectors" ) ) )
          pass
 
       momentumPredictor = True
       if ( simple.found( word( "momentumPredictor" ) ) ):
          momentumPredictor = Switch(simple.lookup( word( "momentumPredictor" ) ) )
          pass
 
       fluxGradp = False
       if ( simple.found( word( "fluxGradp" ) ) ):
          fluxGradp = Switch( simple.lookup( word( "fluxGradp" ) ) )
          pass
 
       transonic = False
       if ( simple.found( word( "transSonic" ) ) ):
          transonic = Switch( simple.lookup( word( "transSonic" ) ) )
          pass
       pass
    else:
       
       nNonOrthCorr = simple.lookupOrDefault( word( "nNonOrthogonalCorrectors" ), 0 )

       momentumPredictor = simple.lookupOrDefault( word( "momentumPredictor" ), Switch( True ) )

       fluxGradp = simple.lookupOrDefault( word( "fluxGradp" ), Switch( False ) )

       transonic = simple.lookupOrDefault( word( "transonic" ), Switch( False ) )
       
       pass
          
    return simple, nNonOrthCorr, momentumPredictor, fluxGradp, transonic


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
        tmp_SfUfbyDelta = mesh.deltaCoeffs()*phi.mag()
        SfUfbyDelta = tmp_SfUfbyDelta()

        CoNum = ( SfUfbyDelta / mesh.magSf() ).ext_max().value() * runTime.deltaT().value()
        meanCoNum = ( SfUfbyDelta.sum() / mesh.magSf().sum() ).value() * runTime.deltaT().value();
        pass

    from Foam.OpenFOAM import ext_Info, nl
    ext_Info() << "Courant Number mean: " << meanCoNum << " max: " << CoNum<< nl

    return CoNum, meanCoNum


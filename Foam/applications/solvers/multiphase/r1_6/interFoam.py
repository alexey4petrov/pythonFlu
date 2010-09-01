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


#----------------------------------------------------------------------------
def _createFields( runTime, mesh ):
    from Foam.OpenFOAM import ext_Info, nl
    from Foam.OpenFOAM import IOdictionary, IOobject, word, fileName
    from Foam.finiteVolume import volScalarField
        
    ext_Info() << "Reading field p\n" << nl
    p = volScalarField( IOobject( word( "p" ),
                                  fileName( runTime.timeName() ),
                                  mesh,
                                  IOobject.MUST_READ,
                                  IOobject.AUTO_WRITE ),
                        mesh )
    
    ext_Info() << "Reading field alpha1\n" << nl
    alpha1 = volScalarField( IOobject( word( "alpha1" ),
                                  fileName( runTime.timeName() ),
                                  mesh,
                                  IOobject.MUST_READ,
                                  IOobject.AUTO_WRITE ),
                                mesh )
    
    ext_Info() << "Reading field U\n" << nl
    from Foam.finiteVolume import volVectorField
    U = volVectorField( IOobject( word( "U" ),
                                  fileName( runTime.timeName() ),
                                  mesh,
                                  IOobject.MUST_READ,
                                  IOobject.AUTO_WRITE ),
                        mesh )
                        
    from Foam.finiteVolume.cfdTools.incompressible import createPhi
    phi = createPhi( runTime, mesh, U )
    
    
    ext_Info() << "Reading transportProperties\n" << nl
    from Foam.transportModels import twoPhaseMixture
    twoPhaseProperties = twoPhaseMixture(U, phi)
    
    rho1 = twoPhaseProperties.rho1()
    rho2 = twoPhaseProperties.rho2()
    
    # Need to store rho for ddt(rho, U)
    rho = volScalarField( IOobject( word( "rho" ),
                                    fileName( runTime.timeName() ),
                                    mesh,
                                    IOobject.READ_IF_PRESENT ),
                          alpha1 * rho1 + ( 1.0 - alpha1 ) * rho2,
                          alpha1.ext_boundaryField().types() )
    rho.oldTime()
    
    # Mass flux
    # Initialisation does not matter because rhoPhi is reset after the
    # alpha1 solution before it is used in the U equation.
    from Foam.finiteVolume import surfaceScalarField
    rhoPhi = surfaceScalarField( IOobject( word( "rho*phi" ),
                                           fileName( runTime.timeName() ),
                                           mesh,
                                           IOobject.NO_READ,
                                           IOobject.NO_WRITE ),
                                 rho1 * phi )
                                 
    pRefCell = 0
    pRefValue = 0.0
    
    from Foam.finiteVolume import setRefCell
    pRefCell, pRefValue = setRefCell( p, mesh.solutionDict().subDict( word( "PISO" ) ), pRefCell, pRefValue )
    
    # Construct interface from alpha1 distribution
    from Foam.transportModels import interfaceProperties
    interface = interfaceProperties( alpha1, U, twoPhaseProperties )


    # Construct incompressible turbulence model
    from Foam import incompressible
    turbulence = incompressible.turbulenceModel.New( U, phi, twoPhaseProperties ) 

    return p, alpha1, U, phi, rho1, rho2, rho, rhoPhi, twoPhaseProperties, pRefCell, pRefValue, interface, turbulence
    


#--------------------------------------------------------------------------------------
def correctPhi( runTime, mesh, phi, p, rho, U, cumulativeContErr, nNonOrthCorr, pRefCell, pRefValue ):
    
    from Foam.finiteVolume.cfdTools.incompressible import continuityErrs
    cumulativeContErr = continuityErrs( mesh, phi, runTime, cumulativeContErr )
    from Foam.OpenFOAM import wordList
    from Foam.finiteVolume import zeroGradientFvPatchScalarField
    pcorrTypes = wordList( p.ext_boundaryField().size(), zeroGradientFvPatchScalarField.typeName )
    
    from Foam.finiteVolume import fixedValueFvPatchScalarField
    for i in range( p.ext_boundaryField().size() ):
       if p.ext_boundaryField()[i].fixesValue():
          pcorrTypes[i] = fixedValueFvPatchScalarField.typeName
          pass
       pass
    
    from Foam.OpenFOAM import IOdictionary, IOobject, word, fileName, dimensionedScalar
    from Foam.finiteVolume import volScalarField
    pcorr = volScalarField( IOobject( word( "pcorr" ),
                                      fileName( runTime.timeName() ),
                                      mesh,
                                      IOobject.NO_READ,
                                      IOobject.NO_WRITE ),
                            mesh,
                            dimensionedScalar( word( "pcorr" ), p.dimensions(), 0.0 ),
                            pcorrTypes  )
    
    from Foam.OpenFOAM import dimTime
    rUAf = dimensionedScalar( word( "(1|A(U))" ), dimTime / rho.dimensions(), 1.0)
    
    from Foam.finiteVolume import adjustPhi
    adjustPhi(phi, U, pcorr)
    
    from Foam import fvc, fvm
    for nonOrth in range( nNonOrthCorr + 1 ):
        pcorrEqn = fvm.laplacian( rUAf, pcorr ) == fvc.div( phi )

        pcorrEqn.setReference(pRefCell, pRefValue)
        pcorrEqn.solve()

        if nonOrth == nNonOrthCorr:
           phi.ext_assign( phi  - pcorrEqn.flux() )
           pass
    
    from Foam.finiteVolume.cfdTools.incompressible import continuityErrs
    cumulativeContErr = continuityErrs( mesh, phi, runTime, cumulativeContErr )
    
    pass
    

#--------------------------------------------------------------------------------------
def alphaEqn( mesh, phi, alpha1, rhoPhi, rho1, rho2, interface, nAlphaCorr ):
    from Foam.OpenFOAM import word 
    alphaScheme = word( "div(phi,alpha)" )
    alpharScheme = word( "div(phirb,alpha)" )
    
    from Foam.finiteVolume import surfaceScalarField
    phic = surfaceScalarField( ( phi / mesh.magSf() ).mag() )
    phic.ext_assign( ( interface.cAlpha() * phic ).ext_min( phic.ext_max() ) )
    phir = phic * interface.nHatf()
    
    from Foam import fvc
    from Foam import MULES

    for aCorr in range( nAlphaCorr ):
       phiAlpha = fvc.flux( phi, alpha1, alphaScheme ) + fvc.flux( -fvc.flux( -phir, 1.0 - alpha1, alpharScheme ), alpha1, alpharScheme )
       MULES.explicitSolve( alpha1, phi, phiAlpha, 1, 0 )
       
       rhoPhi.ext_assign( phiAlpha * ( rho1 - rho2 ) + phi * rho2 )

       pass
    from Foam.OpenFOAM import ext_Info, nl
    ext_Info() << "Liquid phase volume fraction = " << alpha1.weightedAverage( mesh.V() ).value() \
               << "  Min(alpha1) = " << alpha1.ext_min().value() \
               << "  Max(alpha1) = " << alpha1.ext_max().value() << nl
    pass


#----------------------------------------------------------------------------------------
def alphaEqnSubCycle( runTime, piso, mesh, phi, alpha1, rho, rhoPhi, rho1, rho2, interface ):
    from Foam.OpenFOAM import word,readLabel
    nAlphaCorr = readLabel( piso.lookup( word( "nAlphaCorr" ) ) )
    nAlphaSubCycles = readLabel( piso.lookup( word( "nAlphaSubCycles" ) ) )
    if (nAlphaSubCycles > 1):
       totalDeltaT = runTime.deltaT()
       rhoPhiSum = 0.0 * rhoPhi
       from Foam.finiteVolume import subCycle_volScalarField
       alphaSubCycle = subCycle_volScalarField( alpha1, nAlphaSubCycles )
       for item in alphaSubCycle:
           alphaEqn( mesh, phi, alpha1, rhoPhi, rho1, rho2, interface, nAlphaCorr )
           rhoPhiSum.ext_assign( rhoPhiSum + ( runTime.deltaT() / totalDeltaT ) * rhoPhi )
           pass
       # To make sure that variable in the local scope will be destroyed
       # - during destruction of this variable it performs some important actions
       # - there is a difference between C++ and Python memory management, namely
       # if C++ automatically destroys stack variables when they exit the scope,
       # Python relay its memory management of some "garbage collection" algorithm
       # that do not provide predictable behavior on the "exit of scope"
       del alphaSubCycle
       
       rhoPhi.ext_assign( rhoPhiSum )
    else:
       alphaEqn( mesh, phi, alpha1, rhoPhi, rho1, rho2, interface, nAlphaCorr )
       pass
    interface.correct()
    
    rho == alpha1 * rho1 + ( 1.0 - alpha1 ) * rho2

    pass


#--------------------------------------------------------------------------------------
def _UEqn( mesh, alpha1, U, p, rho, rhoPhi, turbulence, g, twoPhaseProperties, interface, momentumPredictor ):
    from Foam.OpenFOAM import word
    from Foam.finiteVolume import surfaceScalarField
    from Foam import fvc
    muEff = surfaceScalarField( word( "muEff" ),
                                twoPhaseProperties.muf() + fvc.interpolate( rho * turbulence.ext_nut() ) )
    from Foam import fvm

    UEqn = fvm.ddt( rho, U ) + fvm.div( rhoPhi, U ) - fvm.laplacian( muEff, U ) - ( fvc.grad( U ) & fvc.grad( muEff ) )
    
    UEqn.relax()

    if momentumPredictor:
       from Foam.finiteVolume import solve
       solve( UEqn == \
                   fvc.reconstruct( fvc.interpolate( rho ) * ( g & mesh.Sf() ) + \
                                    ( fvc.interpolate( interface.sigmaK() ) * fvc.snGrad( alpha1 ) - fvc.snGrad( p ) ) * mesh.magSf() ) )
       pass
    
    return UEqn


#--------------------------------------------------------------------------------------
def _pEqn( mesh, UEqn, U, p, phi, alpha1, rho, g, interface, corr, nCorr, nNonOrthCorr, pRefCell, pRefValue ):
    rUA = 1.0/UEqn.A()
     
    from Foam import fvc
    rUAf = fvc.interpolate( rUA )
    
    U.ext_assign( rUA * UEqn.H() )
    
    from Foam.finiteVolume import surfaceScalarField
    from Foam.OpenFOAM import word
    phiU = surfaceScalarField( word( "phiU" ),
                               ( fvc.interpolate( U ) & mesh.Sf() ) + fvc.ddtPhiCorr( rUA, rho, U, phi ) )
                               
    from Foam.finiteVolume import adjustPhi
    adjustPhi(phiU, U, p)
    
    phi.ext_assign( phiU + ( fvc.interpolate( interface.sigmaK() ) * fvc.snGrad( alpha1 ) * mesh.magSf() + fvc.interpolate( rho ) * ( g & mesh.Sf() ) )*rUAf )

    from Foam import fvm
    for nonOrth in range( nNonOrthCorr + 1 ):
        pEqn = fvm.laplacian( rUAf, p ) == fvc.div( phi ) 
        pEqn.setReference( pRefCell, pRefValue )

        if corr == nCorr-1 and nonOrth == nNonOrthCorr:
           pEqn.solve( mesh.solver( word( str( p.name() ) + "Final" ) ) )
           pass
        else:
           pEqn.solve( mesh.solver( p.name() ) )
           pass
        if nonOrth == nNonOrthCorr:
           phi.ext_assign( phi - pEqn.flux() )
           pass
        pass
    
    U.ext_assign( U + rUA * fvc.reconstruct( ( phi - phiU ) / rUAf ) )
    U.correctBoundaryConditions()

    pass
    
    
#--------------------------------------------------------------------------------------
def main_standalone( argc, argv ):

    from Foam.OpenFOAM.include import setRootCase
    args = setRootCase( argc, argv )

    from Foam.OpenFOAM.include import createTime
    runTime = createTime( args )

    from Foam.OpenFOAM.include import createMesh
    mesh = createMesh( runTime )
    
    from Foam.finiteVolume.cfdTools.general.include import readGravitationalAcceleration
    g = readGravitationalAcceleration( runTime, mesh)
    
    from Foam.finiteVolume.cfdTools.general.include import readPISOControls
    piso, nCorr, nNonOrthCorr, momentumPredictor, transonic, nOuterCorr = readPISOControls( mesh )
    
    from Foam.finiteVolume.cfdTools.general.include import initContinuityErrs
    cumulativeContErr = initContinuityErrs()
    
    p, alpha1, U, phi, rho1, rho2, rho, rhoPhi, twoPhaseProperties, pRefCell, pRefValue, interface, turbulence = _createFields( runTime, mesh )

    from Foam.finiteVolume.cfdTools.general.include import readTimeControls
    adjustTimeStep, maxCo, maxDeltaT = readTimeControls( runTime )
    
    correctPhi( runTime, mesh, phi, p, rho, U, cumulativeContErr, nNonOrthCorr, pRefCell, pRefValue )
    
    from Foam.finiteVolume.cfdTools.incompressible import CourantNo
    CoNum, meanCoNum = CourantNo( mesh, phi, runTime )
    
    from Foam.finiteVolume.cfdTools.general.include import setInitialDeltaT
    runTime = setInitialDeltaT( runTime, adjustTimeStep, maxCo, maxDeltaT, CoNum )
    
    from Foam.OpenFOAM import ext_Info, nl
    ext_Info() << "\nStarting time loop\n" << nl
    
    while runTime.run() :
                
        piso, nCorr, nNonOrthCorr, momentumPredictor, transonic, nOuterCorr = readPISOControls( mesh )
        adjustTimeStep, maxCo, maxDeltaT = readTimeControls( runTime )
        CoNum, meanCoNum = CourantNo( mesh, phi, runTime )        
        
        from Foam.finiteVolume.cfdTools.general.include import setDeltaT
        runTime = setDeltaT( runTime, adjustTimeStep, maxCo, maxDeltaT, CoNum )
        
        runTime.step()
        ext_Info() << "Time = " << runTime.timeName() << nl << nl
        
        twoPhaseProperties.correct()
     
        alphaEqnSubCycle( runTime, piso, mesh, phi, alpha1, rho, rhoPhi, rho1, rho2, interface )
        
        UEqn = _UEqn( mesh, alpha1, U, p, rho, rhoPhi, turbulence, g, twoPhaseProperties, interface, momentumPredictor )

        # --- PISO loop
        for corr in range( nCorr ):
            _pEqn( mesh, UEqn, U, p, phi, alpha1, rho, g, interface, corr, nCorr, nNonOrthCorr, pRefCell, pRefValue )
            pass
        
        from Foam.finiteVolume.cfdTools.incompressible import continuityErrs
        cumulativeContErr = continuityErrs( mesh, phi, runTime, cumulativeContErr )

        turbulence.correct()

        runTime.write()

        ext_Info() << "ExecutionTime = " << runTime.elapsedCpuTime() << " s" << \
              "  ClockTime = " << runTime.elapsedClockTime() << " s" << nl << nl
        
        pass

    ext_Info() << "End\n" << nl 

    import os
    return os.EX_OK


#--------------------------------------------------------------------------------------
import sys, os
from Foam import FOAM_VERSION
if FOAM_VERSION( ">=", "010600" ):
   if __name__ == "__main__" :
      argv = sys.argv
      if len( argv ) > 1 and argv[ 1 ] == "-test":
         argv = None
         test_dir= os.path.join( os.environ[ "PYFOAM_TESTING_DIR" ],'cases', 'local', 'r1.6', 'multiphase','interFoam', 'laminar', 'damBreak' )
         argv = [ __file__, "-case", test_dir ]
         pass
      os._exit( main_standalone( len( argv ), argv ) )


#--------------------------------------------------------------------------------------


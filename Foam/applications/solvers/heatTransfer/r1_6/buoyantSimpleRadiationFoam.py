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

from Foam.OpenFOAM import ext_Info, nl
#------------------------------------------------------------------------------------
def readGravitationalAcceleration( runTime, mesh ):
    ext_Info() << "\nReading g" << nl
    
    from Foam.OpenFOAM import UniformDimensionedVectorField
    from Foam.OpenFOAM import word, IOobject,fileName
    g= UniformDimensionedVectorField( IOobject( word("g"),
                                                fileName( runTime.constant() ),
                                                mesh,
                                                IOobject.MUST_READ,
                                                IOobject.NO_WRITE ) )
    return g


#------------------------------------------------------------------------------------
def createFields( runTime, mesh ):
    ext_Info() << "Reading thermophysical properties\n" << nl
    
    from Foam.thermophysicalModels import autoPtr_basicPsiThermo, basicPsiThermo

    thermo = basicPsiThermo.New(mesh)
    
    from Foam.finiteVolume import volScalarField
    from Foam.OpenFOAM import IOobject, word, fileName
    rho =  volScalarField( IOobject( word( "rho" ),
                                     fileName( runTime.timeName() ),
                                     mesh,
                                     IOobject.NO_READ,
                                     IOobject.NO_WRITE),
                           thermo.rho() )
    p = thermo.p()
    h = thermo.h()
    psi = thermo.psi()

    ext_Info()<< "Reading field U\n" << nl
    from Foam.finiteVolume import volVectorField
    U = volVectorField( IOobject( word( "U" ),
                                  fileName( runTime.timeName() ),
                                  mesh,
                                  IOobject.MUST_READ,
                                  IOobject.AUTO_WRITE ),
                        mesh )
    
    from Foam.finiteVolume.cfdTools.compressible import compressibleCreatePhi
    phi = compressibleCreatePhi( runTime, mesh, rho, U )
    
    ext_Info() << "Creating turbulence model\n" << nl
    from Foam import compressible
    turbulence = compressible.RASModel.New( rho, U, phi, thermo() ) 

    thermo.correct()

    pRefCell = 0
    pRefValue = 0.0
    from Foam.finiteVolume import setRefCell
    pRefCell, pRefValue = setRefCell( p, mesh.solutionDict().subDict( word( "SIMPLE" ) ), pRefCell, pRefValue )
    
    from Foam import fvc
    initialMass = fvc.domainIntegrate( rho )
    
                        
    return thermo, rho, p, h, psi, U, phi, turbulence, pRefCell, pRefValue, initialMass 


#------------------------------------------------------------------------------------
def initConvergenceCheck( simple ):
    eqnResidual = 1
    maxResidual = 0
    convergenceCriterion = 0.0
    
    from Foam.OpenFOAM import word
    tmp, convergenceCriterion = simple.readIfPresent( word( "convergence" ), convergenceCriterion )

    return eqnResidual, maxResidual, convergenceCriterion


#-------------------------------------------------------------------------------------
def fun_UEqn( turbulence, phi, U, rho, g, p, mesh, eqnResidual, maxResidual ):
    from Foam import fvm, fvc 
    UEqn = fvm.div(phi, U) - fvm.Sp(fvc.div(phi), U)+ turbulence.divDevRhoReff(U)

    UEqn.relax();
    from Foam.finiteVolume import solve
    eqnResidual = solve( UEqn == fvc.reconstruct( fvc.interpolate(rho)*(g & mesh.Sf()) - fvc.snGrad(p)*mesh.magSf() ) ).initialResidual()

    maxResidual = max(eqnResidual, maxResidual);
    
    return UEqn, eqnResidual, maxResidual
    
    
#------------------------------------------------------------------------------------
def fun_hEqn( turbulence, phi, h, rho, radiation, p, thermo, eqnResidual, maxResidual  ):
    
    from Foam import fvc, fvm    
    left_exp = fvm.div( phi, h ) - fvm.Sp( fvc.div( phi ), h ) - fvm.laplacian( turbulence.alphaEff(), h )
    right_exp = fvc.div( phi/fvc.interpolate( rho )*fvc.interpolate( p ) ) - p*fvc.div( phi/fvc.interpolate( rho ) ) + radiation.Sh( thermo() )
    
    hEqn = (left_exp == right_exp )

    hEqn.relax()

    eqnResidual = hEqn.solve().initialResidual()
    maxResidual = max(eqnResidual, maxResidual)

    thermo.correct()

    radiation.correct()
    
    return hEqn, eqnResidual, maxResidual
    
    
#------------------------------------------------------------------------------------
def fun_pEqn( thermo, g, rho, UEqn, p, U, psi, phi, initialMass, runTime, mesh, nNonOrthCorr, pRefCell, eqnResidual, maxResidual, cumulativeContErr ):

    rho.ext_assign( thermo.rho() )

    rUA = 1.0/UEqn.A()
    
    from Foam.OpenFOAM import word
    from Foam import fvc,fvm
    from Foam.finiteVolume import surfaceScalarField
    rhorUAf = surfaceScalarField(word( "(rho*(1|A(U)))" ) , fvc.interpolate(rho*rUA));
    U.ext_assign(rUA*UEqn.H())
    UEqn.clear()
    
    phi.ext_assign( fvc.interpolate( rho )*(fvc.interpolate(U) & mesh.Sf()) )

    from Foam.finiteVolume import adjustPhi
    closedVolume = adjustPhi(phi, U, p);

    buoyancyPhi =surfaceScalarField( rhorUAf * fvc.interpolate( rho )*( g & mesh.Sf() ) )
    
    phi.ext_assign( phi+buoyancyPhi )

    for nonOrth in range( nNonOrthCorr+1 ):
        from Foam import fvm
        pEqn = fvm.laplacian(rhorUAf, p) == fvc.div(phi)

        pEqn.setReference(pRefCell, p[pRefCell]);


        if (nonOrth == 0):
            eqnResidual = pEqn.solve().initialResidual()
            maxResidual = max(eqnResidual, maxResidual)
        else:
            pEqn.solve()

        if (nonOrth == nNonOrthCorr):
           if (closedVolume):
              p.ext_assign( p + ( initialMass - fvc.domainIntegrate( psi * p ) ) / fvc.domainIntegrate( psi ) ) 
           
           phi.ext_assign( phi - pEqn.flux() )
           p.relax()
           U.ext_assign( U + rUA * fvc.reconstruct( ( buoyancyPhi - pEqn.flux() ) / rhorUAf ) )
           U.correctBoundaryConditions();
    
    from Foam.finiteVolume.cfdTools.general.include import ContinuityErrs
    cumulativeContErr = ContinuityErrs( phi, runTime, mesh, cumulativeContErr )
    rho.ext_assign( thermo.rho() )
    rho.relax()

    ext_Info()<< "rho max/min : " << rho.ext_max().value() << " " << rho.ext_min().value() << nl
    
    return eqnResidual, maxResidual, cumulativeContErr
    
#----------------------------------------------------------------------------------
def convergenceCheck(runTime, maxResidual, convergenceCriterion):
    if (maxResidual < convergenceCriterion):
       ext_Info()<< "reached convergence criterion: " << convergenceCriterion << nl
       runTime.writeAndEnd()
       ext_Info()<< "latestTime = " << runTime.timeName() << nl

    
#------------------------------------------------------------------------------------
def main_standalone( argc, argv ):

    from Foam.OpenFOAM.include import setRootCase
    args = setRootCase( argc, argv )

    from Foam.OpenFOAM.include import createTime
    runTime = createTime( args )
    
    from Foam.OpenFOAM.include import createMesh
    mesh = createMesh( runTime )
    
    g = readGravitationalAcceleration( runTime, mesh )
    
    thermo, rho, p, h, psi, U, phi, turbulence, pRefCell, pRefValue, initialMass = createFields( runTime, mesh )
    
    from Foam.radiation import createRadiationModel
    radiation = createRadiationModel( thermo )
    
    
    from Foam.finiteVolume.cfdTools.general.include import initContinuityErrs
    cumulativeContErr = initContinuityErrs()
    
    ext_Info() << "\nStarting time loop\n" << nl;

    while runTime.loop():
       ext_Info()<< "Time = " << runTime.timeName() << nl << nl

       from Foam.finiteVolume.cfdTools.general.include import readSIMPLEControls
       simple, nNonOrthCorr, momentumPredictor, fluxGradp, transonic = readSIMPLEControls( mesh )
       
       UEqn, eqnResidual, maxResidual = eqnResidual, maxResidual, convergenceCriterion = initConvergenceCheck( simple )
        
       p.storePrevIter()
       rho.storePrevIter()
       
       UEqn, eqnResidual, maxResidual = fun_UEqn( turbulence, phi, U, rho, g, p, mesh, eqnResidual, maxResidual )
       
       hEqn, eqnResidual, maxResidual = fun_hEqn( turbulence, phi, h, rho, radiation, p, thermo, eqnResidual, maxResidual )
       
       eqnResidual, maxResidual, cumulativeContErr = fun_pEqn( thermo, g, rho, UEqn, p, U, psi, phi, initialMass,\
                                                              runTime, mesh, nNonOrthCorr, pRefCell, eqnResidual, maxResidual, cumulativeContErr )
           
       turbulence.correct()

       runTime.write()

       ext_Info()<< "ExecutionTime = " << runTime.elapsedCpuTime() << " s" \
                 << "  ClockTime = " << runTime.elapsedClockTime() << " s" \
                 << nl << nl
                 
       convergenceCheck( runTime, maxResidual, convergenceCriterion)          

    ext_Info() << "End\n"
    
    import os
    return os.EX_OK

    
#--------------------------------------------------------------------------------------
argv = None
import sys, os
from Foam import FOAM_VERSION
if FOAM_VERSION( "==", "010600" ):
    if __name__ == "__main__" :
        argv = sys.argv
        if len(argv) > 1 and argv[ 1 ] == "-test":
           argv = None
           test_dir= os.path.join( os.environ[ "PYFOAM_TESTING_DIR" ],'cases', 'local', 'r1.6', 'heatTransfer', 'buoyantSimpleRadiationFoam', 'hotRadiationRoom' )
           argv = [ __file__, "-case", test_dir ]
           pass
           
        os._exit( main_standalone( len( argv ), argv ) )
        pass
    pass
else:
    from Foam.OpenFOAM import ext_Info, nl
    ext_Info() <<"\n\n The use buoyantSimpleRadiationFoam It is necessary to SWIG OpenFOAM-1.6\n"    
    pass


#--------------------------------------------------------------------------------------


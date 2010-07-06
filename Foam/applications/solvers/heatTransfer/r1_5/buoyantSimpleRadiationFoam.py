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
def createFields( runTime, mesh, g ):
    ext_Info() << "Reading thermophysical properties\n" << nl
    
    from Foam.thermophysicalModels import autoPtr_basicThermo, basicThermo
    thermo = basicThermo.New( mesh )
    
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
    T = thermo.T()

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

    ext_Info() << "Calculating field g.h\n" << nl
    gh = volScalarField ( word( "gh" ), g & mesh.C() )
    
    from Foam.OpenFOAM import dimensionedScalar
    pRef = dimensionedScalar( word( "pRef" ), p.dimensions(), thermo.lookup( word( "pRef" ) ) )
    
    ext_Info() << "Creating field pd\n" << nl
    pd = volScalarField( IOobject( word( "pd" ),
                                   fileName( runTime.timeName() ),
                                   mesh,
                                   IOobject.MUST_READ,
                                   IOobject.AUTO_WRITE ),
                         mesh )
    
    p.ext_assign( pd + rho * gh + pRef )
    thermo.correct()
    
    pdRefCell = 0
    pdRefValue = 0.0
    from Foam.finiteVolume import setRefCell
    pRefCell, pRefValue = setRefCell( pd, mesh.solutionDict().subDict( word( "SIMPLE" ) ), pdRefCell, pdRefValue )
    
    ext_Info() << "Creating radiation model\n" << nl
    
    from Foam.radiation import radiationModel
    radiation =radiationModel.New( T )
    
    from Foam import fvc
    initialMass = fvc.domainIntegrate( rho )
    
                        
    return thermo, rho, p, h, T, U, phi, turbulence, gh, pRef, pd, p, pdRefCell, pdRefValue, radiation, initialMass 


#------------------------------------------------------------------------------------
def initConvergenceCheck( simple ):
    # initialize values for convergence checks
    eqnResidual = 1
    maxResidual = 0
    convergenceCriterion = 0
    
    from Foam.OpenFOAM import word
    tmp, convergenceCriterion = simple.readIfPresent( word( "convergence" ), convergenceCriterion )
    
    return eqnResidual, maxResidual, convergenceCriterion


#-------------------------------------------------------------------------------------
def fun_UEqn( phi, U, turbulence, pd, rho, gh, eqnResidual, maxResidual ):
    from Foam import fvm, fvc 
    UEqn = fvm.div(phi, U) - fvm.Sp(fvc.div(phi), U)+ turbulence.divDevRhoReff(U)

    UEqn.relax();

    from Foam.finiteVolume import solve
    eqnResidual = solve( UEqn == -fvc.grad( pd ) - fvc.grad( rho ) * gh ).initialResidual()

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
def fun_pEqn( runTime, thermo, UEqn, U, phi, rho, gh, pd, p, initialMass, mesh, pRef, nNonOrthCorr, \
              pdRefCell, pdRefValue, eqnResidual, maxResidual, cumulativeContErr ):
    
    rUA = 1.0/UEqn.A()
    U.ext_assign( rUA * UEqn().H() )
    
    UEqn.clear()
    from Foam import fvc
    phi.ext_assign( fvc.interpolate( rho )*(fvc.interpolate(U) & mesh.Sf()) )
    
    from Foam.finiteVolume import adjustPhi
    closedVolume = adjustPhi(phi, U, p)
    
    phi.ext_assign( phi - fvc.interpolate( rho *gh * rUA ) * fvc.snGrad( rho ) * mesh.magSf() )
    
    from Foam import fvm
    for nonOrth in range( nNonOrthCorr + 1):
        pdEqn = ( fvm.laplacian( rho * rUA, pd ) == fvc.div(phi) )
        
        pdEqn.setReference(pdRefCell, pdRefValue)
        # retain the residual from the first iteration    
        
        if nonOrth == 0:
           eqnResidual = pdEqn.solve().initialResidual()
           maxResidual = max(eqnResidual, maxResidual)
           pass
        else:
           pdEqn.solve()
           pass
        
        if nonOrth == nNonOrthCorr:
           phi.ext_assign( phi - pdEqn.flux() )
           pass
        
        pass

    from Foam.finiteVolume.cfdTools.general.include import ContinuityErrs
    cumulativeContErr = ContinuityErrs( phi, runTime, mesh, cumulativeContErr )
    
    # Explicitly relax pressure for momentum corrector
    pd.relax()
    
    p.ext_assign( pd + rho * gh + pRef )
    
    U.ext_assign( U- rUA * ( fvc.grad( pd ) + fvc.grad( rho ) * gh ) )
    U.correctBoundaryConditions()
    
    # For closed-volume cases adjust the pressure and density levels
    # to obey overall mass continuity
    if closedVolume:
       p.ext_assign( p + ( initialMass - fvc.domainIntegrate( thermo.psi() * p ) ) / fvc.domainIntegrate( thermo.psi() ) )
    
    rho.ext_assign( thermo.rho() )
    rho.relax()
    
    from Foam.OpenFOAM import ext_Info, nl
    ext_Info()<< "rho max/min : " << rho.ext_max().value() << " " << rho.ext_min().value() << nl
    
    return eqnResidual, maxResidual, cumulativeContErr
    
#----------------------------------------------------------------------------------
def convergenceCheck(runTime, maxResidual, convergenceCriterion):
    if (maxResidual < convergenceCriterion):
       ext_Info()<< "reached convergence criterion: " << convergenceCriterion << nl
       runTime.writeAndEnd()
       ext_Info()<< "latestTime = " << runTime.timeName() << nl
       pass
    pass
    
#------------------------------------------------------------------------------------
def main_standalone( argc, argv ):
    from Foam.OpenFOAM.include import setRootCase
    args = setRootCase( argc, argv )

    from Foam.OpenFOAM.include import createTime
    runTime = createTime( args )
    
    from Foam.OpenFOAM.include import createMesh
    mesh = createMesh( runTime )
    
    # All "IOobject" (fvMesh, for example)  should overlive all its dependency IOobjects (fields, for exmaple)
    def runSeparateNamespace( runTime, mesh ):
        from Foam.finiteVolume.cfdTools.general.include  import readEnvironmentalProperties
        g, environmentalProperties = readEnvironmentalProperties( runTime, mesh )
    
        thermo, rho, p, h, T, U, phi, turbulence, gh, pRef, pd, p, pdRefCell, pdRefValue, radiation, initialMass  = createFields( runTime, mesh, g )
    
        from Foam.finiteVolume.cfdTools.general.include import initContinuityErrs
        cumulativeContErr = initContinuityErrs()
    
        ext_Info() << "\nStarting time loop\n" << nl;
    
        runTime +=runTime.deltaT()
    
        while not runTime.end():
           ext_Info()<< "Time = " << runTime.timeName() << nl << nl

           from Foam.finiteVolume.cfdTools.general.include import readSIMPLEControls
           simple, nNonOrthCorr, momentumPredictor, fluxGradp, transonic = readSIMPLEControls( mesh )

           eqnResidual, maxResidual, convergenceCriterion = initConvergenceCheck( simple )
        
           pd.storePrevIter()
           rho.storePrevIter()
           # Pressure-velocity SIMPLE corrector
           UEqn, eqnResidual, maxResidual = fun_UEqn( phi, U, turbulence, pd, rho, gh, eqnResidual, maxResidual )
       
           hEqn, eqnResidual, maxResidual = fun_hEqn( turbulence, phi, h, rho, radiation, p, thermo, eqnResidual, maxResidual )
       
           eqnResidual, maxResidual, cumulativeContErr = fun_pEqn( runTime, thermo, UEqn, U, phi, rho, gh, pd, p, initialMass, mesh, pRef, \
                                                               nNonOrthCorr, pdRefCell, pdRefValue, eqnResidual, maxResidual, cumulativeContErr )
           
           turbulence.correct()

           runTime.write()

           ext_Info()<< "ExecutionTime = " << runTime.elapsedCpuTime() << " s" \
                     << "  ClockTime = " << runTime.elapsedClockTime() << " s" \
                     << nl << nl
                 
           convergenceCheck( runTime, maxResidual, convergenceCriterion)          
       
           runTime +=runTime.deltaT()
           pass
    #-----------------------------------------------------------------------------   
    runSeparateNamespace( runTime, mesh )
        
    ext_Info() << "End\n"
    import os
    return os.EX_OK

    
#--------------------------------------------------------------------------------------
argv = None
import sys, os

if os.environ[ "WM_PROJECT_VERSION" ] == "1.5" :
    if __name__ == "__main__" :
        argv = sys.argv
        if len(argv) > 1 and argv[ 1 ] == "-test":
           argv = None
           test_dir= os.path.join( os.environ[ "PYFOAM_TESTING_DIR" ],'cases', 'r1.5', 'heatTransfer', 'buoyantSimpleRadiationFoam', 'hotRadiationRoom' )
           argv = [ __file__, "-case", test_dir ]
           pass
           
        os._exit( main_standalone( len( argv ), argv ) )
        pass
    pass
else:
    from Foam.OpenFOAM import ext_Info, nl
    ext_Info() <<"\n\n The use buoyantSimpleRadiationFoam It is necessary to SWIG OpenFOAM-1.5\n"    
    pass


#--------------------------------------------------------------------------------------


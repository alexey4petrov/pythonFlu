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
#-------------------------------------------------------------------------
def createFields( runTime, mesh, g ):
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

    ext_Info() << "Calculating field g.h\n" << nl
    gh = volScalarField ( word( "gh" ), g & mesh.C() )
    from Foam.finiteVolume import surfaceScalarField
    ghf = surfaceScalarField( word( "ghf" ), g & mesh.Cf() )

    ext_Info() << "Reading field p_rgh\n" << nl
    p_rgh = volScalarField( IOobject( word( "p_rgh" ),
                                      fileName( runTime.timeName() ),
                                      mesh,
                                      IOobject.MUST_READ,
                                      IOobject.AUTO_WRITE ),
                            mesh )

    #Force p_rgh to be consistent with p
    p_rgh.ext_assign( p - rho*gh )

    pRefCell = 0
    pRefValue = 0.0
    from Foam.finiteVolume import setRefCell
    pRefCell, pRefValue = setRefCell( p, p_rgh, mesh.solutionDict().subDict( word( "SIMPLE" ) ), pRefCell, pRefValue )
    
    from Foam import fvc
    initialMass = fvc.domainIntegrate( rho )
    totalVolume = mesh.V().ext_sum()
    
                        
    return thermo, rho, p, h, psi, U, phi, turbulence, gh, ghf, p_rgh, pRefCell, pRefValue, initialMass, totalVolume


#--------------------------------------------------------------------------------------
def initConvergenceCheck( simple ):
    eqnResidual = 1
    maxResidual = 0
    convergenceCriterion = 0
    
    from Foam.OpenFOAM import word
    tmp, convergenceCriterion = simple.readIfPresent( word( "convergence" ), convergenceCriterion )
    
    return eqnResidual, maxResidual, convergenceCriterion


#--------------------------------------------------------------------------------------
def fun_UEqn( turbulence, phi, U, rho, g, p, ghf, p_rgh, mesh, eqnResidual, maxResidual, momentumPredictor ):
    from Foam import fvm, fvc 
    UEqn = fvm.div(phi, U) + turbulence.divDevRhoReff(U)

    UEqn.relax()
    if momentumPredictor:
       from Foam.finiteVolume import solve
       eqnResidual = solve( UEqn == fvc.reconstruct( (- ghf * fvc.snGrad( rho ) - fvc.snGrad( p_rgh ) ) * mesh.magSf() ) ).initialResidual()

       maxResidual = max(eqnResidual, maxResidual)
       pass
    
    return UEqn, eqnResidual, maxResidual


#--------------------------------------------------------------------------------------
def _hEqn( phi, h, turbulence, rho, p, thermo, eqnResidual, maxResidual ):
    from Foam import fvc, fvm
    hEqn = fvm.div( phi, h ) - fvm.Sp( fvc.div( phi ), h ) - fvm.laplacian( turbulence.alphaEff(), h ) \
            ==  fvc.div( phi / fvc.interpolate( rho ) * fvc.interpolate( p ) ) - p * fvc.div( phi / fvc.interpolate( rho ) ) 

    hEqn.relax()

    eqnResidual = hEqn.solve().initialResidual()
    maxResidual = max(eqnResidual, maxResidual)

    thermo.correct()
    
    return hEqn, eqnResidual, maxResidual
    

#--------------------------------------------------------------------------------------    
def fun_pEqn( thermo, g, rho, UEqn, p, p_rgh, U, psi, phi, ghf, gh, initialMass, runTime, mesh, nNonOrthCorr, pRefCell, eqnResidual, maxResidual, cumulativeContErr ):

    rho.ext_assign( thermo.rho() )
    rho.relax()

    rUA = 1.0/UEqn.A()
    
    from Foam.OpenFOAM import word
    from Foam import fvc,fvm
    from Foam.finiteVolume import surfaceScalarField
    rhorUAf = surfaceScalarField(word( "(rho*(1|A(U)))" ) , fvc.interpolate(rho*rUA));
    U.ext_assign(rUA*UEqn.H())
    UEqn.clear()
    
    phi.ext_assign( fvc.interpolate( rho )*(fvc.interpolate(U) & mesh.Sf()) )

    from Foam.finiteVolume import adjustPhi
    closedVolume = adjustPhi(phi, U, p_rgh );

    buoyancyPhi =surfaceScalarField( rhorUAf * ghf * fvc.snGrad( rho ) * mesh.magSf() )
    
    phi.ext_assign( phi - buoyancyPhi )

    for nonOrth in range( nNonOrthCorr+1 ):
        from Foam import fvm
        p_rghEqn = fvm.laplacian(rhorUAf, p_rgh) == fvc.div(phi)
        
        from Foam.finiteVolume import getRefCellValue
        p_rghEqn.setReference(pRefCell, getRefCellValue( p_rgh, pRefCell ) )

        eqnResidual = p_rghEqn.solve().initialResidual()
        
        if (nonOrth == 0):
            maxResidual = max(eqnResidual, maxResidual)
            pass

        if (nonOrth == nNonOrthCorr):
           # Calculate the conservative fluxes
           phi.ext_assign( phi - p_rghEqn.flux() )
           # Explicitly relax pressure for momentum corrector
           p_rgh.relax()
           U.ext_assign( U - rUA * fvc.reconstruct( ( buoyancyPhi + p_rghEqn.flux() ) / rhorUAf ) )
           U.correctBoundaryConditions()
           pass
    
    from Foam.finiteVolume.cfdTools.general.include import ContinuityErrs
    cumulativeContErr = ContinuityErrs( phi, runTime, mesh, cumulativeContErr )
    
    p.ext_assign( p_rgh + rho * gh )

    # For closed-volume cases adjust the pressure level
    # to obey overall mass continuity
    if closedVolume:
       p.ext_assign( p + (initialMass - fvc.domainIntegrate( psi * p ) ) / fvc.domainIntegrate( psi ) )
       p_rgh.ext_assign( p - rho * gh )

    rho.ext_assign( thermo.rho() )
    rho.relax()

    ext_Info()<< "rho max/min : " << rho.ext_max().value() << " " << rho.ext_min().value() << nl
    
    return eqnResidual, maxResidual, cumulativeContErr


#--------------------------------------------------------------------------------------
def convergenceCheck( maxResidual, convergenceCriterion ):
    from Foam.OpenFOAM import ext_Info, nl
    
    if (maxResidual < convergenceCriterion):
       ext_Info() << "reached convergence criterion: " << convergenceCriterion << nl
       runTime.writeAndEnd();
       ext_Info   << "latestTime = " << runTime.timeName() << nl
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
    
    thermo, rho, p, h, psi, U, phi, turbulence, gh, ghf, p_rgh, pRefCell, pRefValue, initialMass, totalVolume = createFields( runTime, mesh, g )
    
    from Foam.finiteVolume.cfdTools.general.include import initContinuityErrs
    cumulativeContErr = initContinuityErrs()

    from Foam.OpenFOAM import ext_Info, nl
    ext_Info() << "\nStarting time loop\n" <<nl
    
    while runTime.loop():
        ext_Info() << "Time = " << runTime.timeName() << nl << nl

        from Foam.finiteVolume.cfdTools.general.include import readSIMPLEControls
        simple, nNonOrthCorr, momentumPredictor, transonic = readSIMPLEControls( mesh )
        
        eqnResidual, maxResidual, convergenceCriterion = initConvergenceCheck( simple )
                
        p_rgh.storePrevIter()
        rho.storePrevIter()
        
        # Pressure-velocity SIMPLE corrector
        UEqn, eqnResidual, maxResidual = fun_UEqn( turbulence, phi, U, rho, g, p, ghf, p_rgh, mesh, eqnResidual, maxResidual, momentumPredictor )
        
        hEqn, eqnResidual, maxResidual = _hEqn( phi, h, turbulence, rho, p, thermo, eqnResidual, maxResidual )
        
        eqnResidual, maxResidual, cumulativeContErr = fun_pEqn( thermo, g, rho, UEqn, p, p_rgh, U, psi, phi, ghf, gh, initialMass,\
                                                               runTime, mesh, nNonOrthCorr, pRefCell, eqnResidual, maxResidual, cumulativeContErr )
        
        turbulence.correct()

        runTime.write()
        
        ext_Info() << "ExecutionTime = " << runTime.elapsedCpuTime() << " s" << \
              "  ClockTime = " << runTime.elapsedClockTime() << " s" << nl << nl
        
        convergenceCheck( maxResidual, convergenceCriterion ) 
        
        pass
        
    ext_Info() << "End\n" << nl 

    import os
    return os.EX_OK


#--------------------------------------------------------------------------------------
from Foam import FOAM_VERSION
import sys, os
if FOAM_VERSION( ">=", "010700" ):
   if __name__ == "__main__" :
      argv = sys.argv
      if len( argv ) > 1 and argv[ 1 ] == "-test":
         argv = None
         test_dir= os.path.join( os.environ[ "PYFOAM_TESTING_DIR" ],'cases', 'propogated', 'r1.7.0', 'heatTransfer', 'buoyantSimpleFoam', 'hotRoom' )
         argv = [ __file__, "-case", test_dir ]
         pass
      os._exit( main_standalone( len( argv ), argv ) )
else:
   from Foam.OpenFOAM import ext_Info
   ext_Info()<< "\nTo use this solver, It is necessary to SWIG OpenFoam1.7.0 or higher\n "

    
#--------------------------------------------------------------------------------------


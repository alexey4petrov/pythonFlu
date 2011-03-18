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


#-------------------------------------------------------------------------
def _createFields( runTime, mesh, g ):
    from Foam.OpenFOAM import ext_Info, nl
    ext_Info() << "Reading thermophysical properties\n" << nl 

    from Foam.thermophysicalModels import basicRhoThermo
    thermo = basicRhoThermo.New( mesh )

    from Foam.OpenFOAM import IOdictionary, IOobject, word, fileName
    from Foam.finiteVolume import volScalarField

    rho= volScalarField( IOobject( word( "rho" ),
                                   fileName( runTime.timeName() ),
                                   mesh,
                                   IOobject.NO_READ,
                                   IOobject.NO_WRITE ),
                         thermo.rho() )

    p = thermo.p()
    h = thermo.h()
    psi = thermo.psi()
    
    ext_Info() << "Reading field U\n" << nl
    
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
    turbulence = compressible.turbulenceModel.New( rho, U, phi, thermo() )
    
    ext_Info() << "Creating field DpDt\n" << nl
    from Foam import fvc
    from Foam.finiteVolume import surfaceScalarField
    DpDt = volScalarField( word( "DpDt" ),
                           fvc.DDt( surfaceScalarField( word( "phiU" ), phi / fvc.interpolate( rho ) ), p ) )
    
    thermo.correct()

    initialMass = fvc.domainIntegrate(rho);
    
    totalVolume = mesh.V().ext_sum()
    
    return thermo, p, h, psi, phi, rho, U, turbulence, DpDt, initialMass, totalVolume


#--------------------------------------------------------------------------------------
def _Ueqn( U, phi, turbulence, p, rho, g, mesh, momentumPredictor ):
    from Foam import fvm
    # Solve the momentum equation

    UEqn = fvm.ddt( rho, U ) + fvm.div( phi, U ) + turbulence.divDevRhoReff( U )
    
    
    UEqn.relax()

    from Foam.finiteVolume import solve
    from Foam import fvc
    if momentumPredictor:
       solve( UEqn == fvc.reconstruct( fvc.interpolate( rho ) * ( g & mesh.Sf() ) - fvc.snGrad( p ) * mesh.magSf() ) )
       pass
       
    return UEqn


#--------------------------------------------------------------------------------------
def _hEqn( rho, h, phi, turbulence, thermo, DpDt ):
    from Foam import fvm
    hEqn = fvm.ddt( rho, h ) + fvm.div(phi, h) - fvm.laplacian( turbulence.alphaEff(), h ) == DpDt 

    hEqn.relax()
    hEqn.solve()

    thermo.correct()
    
    return hEqn
    

#--------------------------------------------------------------------------------------    
def _pEqn( runTime, mesh, UEqn, thermo, p, psi, U, rho, phi, DpDt, g, initialMass, totalVolume, corr, nCorr, nNonOrthCorr, cumulativeContErr ): 
    closedVolume = p.needReference()
    rho.ext_assign( thermo.rho() )

    # Thermodynamic density needs to be updated by psi*d(p) after the
    # pressure solution - done in 2 parts. Part 1:
    thermo.rho().ext_assign( thermo.rho() - psi * p )
    
    rUA = 1.0/UEqn.A()
    from Foam.OpenFOAM import word
    from Foam.finiteVolume import surfaceScalarField
    from Foam import fvc
    rhorUAf = surfaceScalarField( word( "(rho*(1|A(U)))" ), fvc.interpolate( rho * rUA ) )

    U.ext_assign( rUA * UEqn.H() )

    phiU = fvc.interpolate( rho ) * ( (fvc.interpolate( U ) & mesh.Sf() ) + fvc.ddtPhiCorr( rUA, rho, U, phi ) ) 

    phi.ext_assign( phiU + rhorUAf * fvc.interpolate( rho ) * (g & mesh.Sf() ) )
    
    for nonOrth in range( nNonOrthCorr+1 ):
        
        from Foam import fvm
        from Foam.finiteVolume import correction
        pEqn = fvc.ddt( rho ) + psi * correction( fvm.ddt( p ) ) + fvc.div( phi ) - fvm.laplacian( rhorUAf, p )
        
        if corr == nCorr-1  and nonOrth == nNonOrthCorr:
           pEqn.solve( mesh.solver( word( str( p.name() ) + "Final" ) ) )
           pass
        else:
           pEqn.solve( mesh.solver( p.name() ) )
           pass
        if nonOrth == nNonOrthCorr:
           phi.ext_assign( phi + pEqn.flux() )
           pass

    # Second part of thermodynamic density update
    thermo.rho().ext_assign( thermo.rho() + psi * p )

    U.ext_assign( U + rUA * fvc.reconstruct( ( phi - phiU ) / rhorUAf ) )
    U.correctBoundaryConditions()
    
    DpDt.ext_assign( fvc.DDt( surfaceScalarField( word( "phiU" ), phi / fvc.interpolate( rho ) ), p ) )
    
    from Foam.finiteVolume.cfdTools.compressible import rhoEqn  
    rhoEqn( rho, phi )
    
    from Foam.finiteVolume.cfdTools.compressible import compressibleContinuityErrs
    cumulativeContErr = compressibleContinuityErrs( rho, thermo, cumulativeContErr )

    # For closed-volume cases adjust the pressure and density levels
    # to obey overall mass continuity
    if closedVolume:
       p.ext_assign( p + ( initialMass - fvc.domainIntegrate( psi * p ) ) / fvc.domainIntegrate( psi ) )
       thermo.rho().ext_assign(  psi * p )
       rho.ext_assign( rho + ( initialMass - fvc.domainIntegrate( rho ) ) / totalVolume )
       pass

    return cumulativeContErr


   
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
    
    thermo, p, h, psi, phi, rho, U, turbulence, DpDt, initialMass, totalVolume = _createFields( runTime, mesh, g )
    
    from Foam.finiteVolume.cfdTools.general.include import initContinuityErrs
    cumulativeContErr = initContinuityErrs()
    
    from Foam.finiteVolume.cfdTools.general.include import readTimeControls
    adjustTimeStep, maxCo, maxDeltaT = readTimeControls( runTime )
    
    from Foam.finiteVolume.cfdTools.compressible import compressibleCourantNo
    CoNum, meanCoNum = compressibleCourantNo( mesh, phi, rho, runTime )
    
    from Foam.finiteVolume.cfdTools.general.include import setInitialDeltaT
    runTime = setInitialDeltaT( runTime, adjustTimeStep, maxCo, maxDeltaT, CoNum )

    from Foam.OpenFOAM import ext_Info, nl
    ext_Info() << "\nStarting time loop\n" <<nl
    
    while runTime.run():
        from Foam.finiteVolume.cfdTools.general.include import readTimeControls
        adjustTimeStep, maxCo, maxDeltaT = readTimeControls( runTime )
    
        from Foam.finiteVolume.cfdTools.general.include import readPISOControls
        piso, nCorr, nNonOrthCorr, momentumPredictor, transonic, nOuterCorr = readPISOControls( mesh )
        
        from Foam.finiteVolume.cfdTools.compressible import compressibleCourantNo
        CoNum, meanCoNum = compressibleCourantNo( mesh, phi, rho, runTime )
        
        from Foam.finiteVolume.cfdTools.general.include import setDeltaT
        runTime = setDeltaT( runTime, adjustTimeStep, maxCo, maxDeltaT, CoNum )
        
        runTime.increment()
        ext_Info() << "Time = " << runTime.timeName() << nl << nl
        
        from Foam.finiteVolume.cfdTools.compressible import rhoEqn  
        rhoEqn( rho, phi )
        
        UEqn = _Ueqn(  U, phi, turbulence, p, rho, g, mesh, momentumPredictor )
        
        hEqn = _hEqn( rho, h, phi, turbulence, thermo, DpDt )
        
        # --- PISO loop
        for corr in range( nCorr ):
            cumulativeContErr = _pEqn( runTime, mesh, UEqn, thermo, p, psi, U, rho, phi, DpDt, g,\
                                       initialMass, totalVolume, corr, nCorr, nNonOrthCorr, cumulativeContErr )
            pass

        turbulence.correct()

        rho.ext_assign( thermo.rho() )
        
        runTime.write()
        
        ext_Info() << "ExecutionTime = " << runTime.elapsedCpuTime() << " s" << \
              "  ClockTime = " << runTime.elapsedClockTime() << " s" << nl << nl
        
        pass
        
    ext_Info() << "End\n" << nl 

    import os
    return os.EX_OK


#--------------------------------------------------------------------------------------
from Foam import FOAM_REF_VERSION
import sys, os
if FOAM_REF_VERSION( "==", "010600" ):
   if __name__ == "__main__" :
      argv = sys.argv
      if len( argv ) > 1 and argv[ 1 ] == "-test":
         argv = None
         test_dir= os.path.join( os.environ[ "PYFOAM_TESTING_DIR" ],'cases', 'local', 'r1.6', 'heatTransfer', 'buoyantPisoFoam', 'hotRoom' )
         argv = [ __file__, "-case", test_dir ]
         pass
      os._exit( main_standalone( len( argv ), argv ) )
else:
   from Foam.OpenFOAM import ext_Info
   ext_Info()<< "\nTo use this solver, It is necessary to SWIG OpenFoam1.6 \n "

    
#--------------------------------------------------------------------------------------


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
def _createFields( runTime, mesh ):
    from Foam.OpenFOAM import ext_Info, nl
    ext_Info() << "Reading thermophysical properties\n" << nl

    from Foam.thermophysicalModels import basicPsiThermo, autoPtr_basicPsiThermo
    thermo = basicPsiThermo.New( mesh )

    p = thermo.p()
    h = thermo.h()
    psi = thermo.psi()

    from Foam.OpenFOAM import IOdictionary, IOobject, word, fileName
    from Foam.finiteVolume import volScalarField
    rho = volScalarField( IOobject( word( "rho" ),
                                    fileName( runTime.timeName() ),
                                    mesh,
                                    IOobject.READ_IF_PRESENT,
                                    IOobject.AUTO_WRITE ),
                          thermo.rho() )

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
    
    from Foam.OpenFOAM import dimensionedScalar
    pMin = dimensionedScalar( mesh.solutionDict().subDict( word( "PIMPLE" ) ).lookup( word( "pMin" ) ) )
    
    ext_Info() << "Creating turbulence model\n" << nl
    from Foam import compressible
    turbulence = compressible.turbulenceModel.New( rho,
                                                    U,
                                                    phi,
                                                    thermo() )
    
    ext_Info() << "Creating field DpDt\n" << nl
    from Foam import fvc
    from Foam.finiteVolume import surfaceScalarField
    DpDt = fvc.DDt( surfaceScalarField( word( "phiU" ) , phi / fvc.interpolate( rho ) ), p )
    
    return p, h, psi, rho, U, phi, turbulence, thermo, pMin, DpDt


#--------------------------------------------------------------------------------------
def _UEqn( mesh, U, rho, phi, turbulence, p, oCorr, nOuterCorr, momentumPredictor ):
    from Foam import fvm
    # Solve the Momentum equation

    # The initial C++ expression does not work properly, because of
    #  1. turbulence.divDevRhoReff( U ) - changes values for the U boundaries
    #  2. the order of expression arguments computation differs with C++
    #UEqn = fvm.ddt( rho, U ) + fvm.div( phi, U ) + turbulence.divDevRhoReff( U )
    
    UEqn = turbulence.divDevRhoReff( U ) + ( fvm.ddt( rho, U ) + fvm.div( phi, U ) )
        
    if oCorr == nOuterCorr-1:
       UEqn().relax( 1.0 )
       pass
    else:
       UEqn().relax()
       pass
    
    rUA = 1.0 / UEqn.A()
    
    from Foam.finiteVolume import solve
    from Foam.OpenFOAM import word
    from Foam import fvc
    if momentumPredictor:
       if oCorr == nOuterCorr-1:
          solve( UEqn == -fvc.grad( p ), mesh.solver( word( "UFinal" ) ) ) 
          pass
       else:
          solve( UEqn == -fvc.grad( p ) )
          pass
    else:
       U.ext_assign( rUA * ( UEqn.H() - fvc.grad( p ) ) )
       U.correctBoundaryConditions()
       pass
   
    return UEqn


#--------------------------------------------------------------------------------------
def _hEqn( mesh, rho, h, phi, turbulence, DpDt, thermo, oCorr, nOuterCorr ):
    from Foam import fvm
    hEqn = fvm.ddt(rho, h) + fvm.div( phi, h ) - fvm.laplacian( turbulence.alphaEff(), h ) == DpDt

    if oCorr == nOuterCorr-1:
       hEqn.relax()
       from Foam.OpenFOAM import word
       hEqn.solve(mesh.solver( word( "hFinal" ) ) )
       pass
    else:
       hEqn.relax()
       hEqn.solve()
       pass
    thermo.correct()
    pass
    
    return hEqn


#--------------------------------------------------------------------------------------
def _pEqn( rho, thermo, UEqn, nNonOrthCorr, psi, U, mesh, phi, p, DpDt, pMin, corr, cumulativeContErr, nCorr, oCorr, nOuterCorr, transonic ):
    rho.ext_assign( thermo.rho() )

    rUA = 1.0 / UEqn.A()
    U.ext_assign( rUA * UEqn.H() )
    
    if nCorr <= 1:
       UEqn.clear()
       pass

    from Foam import fvc, fvm
    from Foam.OpenFOAM import word
    from Foam.finiteVolume import surfaceScalarField
    if transonic: 
       
       phid = surfaceScalarField( word( "phid" ), 
                                  fvc.interpolate( psi ) * ( ( fvc.interpolate( U ) & mesh.Sf() ) + fvc.ddtPhiCorr( rUA, rho, U, phi ) ) )
       
       for nonOrth in range( nNonOrthCorr + 1 ) :
           pEqn = fvm.ddt( psi, p ) + fvm.div( phid, p ) - fvm.laplacian( rho * rUA, p )
           
           if oCorr == nOuterCorr-1 and corr == nCorr-1 and nonOrth == nNonOrthCorr :
              pEqn.solve( mesh.solver( word( "pFinal" ) ) )
              pass
           else:
              pEqn.solve()
              pass
           if nonOrth == nNonOrthCorr:
              phi == pEqn.flux()
              pass
           pass
       pass
    else:
       phi.ext_assign( fvc.interpolate( rho ) * ( ( fvc.interpolate( U ) & mesh.Sf() ) ) )
       
       for nonOrth in range( nNonOrthCorr + 1 ) :
           # Pressure corrector
           pEqn = fvm.ddt( psi, p ) + fvc.div( phi ) - fvm.laplacian( rho * rUA, p )
           if oCorr == nOuterCorr-1 and corr == nCorr-1 and nonOrth == nNonOrthCorr:
              pEqn.solve(mesh.solver( word( "pFinal" ) ) )
              pass
           else:
              pEqn.solve()
              pass
           
           if nonOrth == nNonOrthCorr:
              phi.ext_assign( phi + pEqn.flux() )
              pass
           pass
       pass
    
    from Foam.finiteVolume.cfdTools.compressible import rhoEqn
    rhoEqn( rho, phi )
    
    from Foam.finiteVolume.cfdTools.compressible import compressibleContinuityErrs
    cumulativeContErr = compressibleContinuityErrs( rho, thermo, cumulativeContErr )
    
    p.relax()

    rho.ext_assign( thermo.rho() )
    rho.relax()
    from Foam.OpenFOAM import ext_Info, nl
    ext_Info() << "rho max/min : " << rho.ext_max().value() << " " << rho.ext_min().value() << nl 
    
    
    U.ext_assign( U - rUA * fvc.grad( p ) )
    U.correctBoundaryConditions()

    DpDt.ext_assign( fvc.DDt( surfaceScalarField( word( "phiU" ), phi / fvc.interpolate( rho ) ), p ) )

    from Foam.finiteVolume import bound
    bound(p, pMin)
    
    return cumulativeContErr


#--------------------------------------------------------------------------------------
def main_standalone( argc, argv ):

    from Foam.OpenFOAM.include import setRootCase
    args = setRootCase( argc, argv )

    from Foam.OpenFOAM.include import createTime
    runTime = createTime( args )

    from Foam.OpenFOAM.include import createMesh
    mesh = createMesh( runTime )

    p, h, psi, rho, U, phi, turbulence, thermo, pMin, DpDt = _createFields( runTime, mesh )
    
    from Foam.finiteVolume.cfdTools.general.include import initContinuityErrs
    cumulativeContErr = initContinuityErrs()

    from Foam.OpenFOAM import ext_Info, nl
    ext_Info() << "\nStarting time loop\n" << nl
    
    while runTime.run() :
        
        from Foam.finiteVolume.cfdTools.general.include import readTimeControls
        adjustTimeStep, maxCo, maxDeltaT = readTimeControls( runTime )

        from Foam.finiteVolume.cfdTools.general.include import readPIMPLEControls
        pimple, nOuterCorr, nCorr, nNonOrthCorr, momentumPredictor, transonic = readPIMPLEControls( mesh )

        from Foam.finiteVolume.cfdTools.compressible import compressibleCourantNo
        CoNum, meanCoNum = compressibleCourantNo( mesh, phi, rho, runTime )
        
        from Foam.finiteVolume.cfdTools.general.include import setDeltaT
        runTime = setDeltaT( runTime, adjustTimeStep, maxCo, maxDeltaT, CoNum )
        
        runTime.step()
        ext_Info() << "Time = " << runTime.timeName() << nl << nl
        
        if nOuterCorr != 1:
           p.storePrevIter()
           rho.storePrevIter()
           pass
        
        # --- Pressure-velocity PIMPLE corrector loop
        for oCorr in range( nOuterCorr ):
            UEqn = _UEqn( mesh, U, rho, phi, turbulence, p, oCorr, nOuterCorr, momentumPredictor )
            
            hEqn = _hEqn( mesh, rho, h, phi, turbulence, DpDt, thermo, oCorr, nOuterCorr )
        
            # --- PISO loop

            for corr in range( nCorr ) :
                cumulativeContErr = _pEqn( rho, thermo, UEqn, nNonOrthCorr, psi, U, mesh, phi, p, DpDt, pMin,\
                                           corr, cumulativeContErr, nCorr, oCorr, nOuterCorr, transonic )
                pass

            turbulence.correct()
            pass

        runTime.write()

        ext_Info() << "ExecutionTime = " << runTime.elapsedCpuTime() << " s" << \
              "  ClockTime = " << runTime.elapsedClockTime() << " s" << nl << nl
        
        pass

    ext_Info() << "End\n"

    import os
    return os.EX_OK


#--------------------------------------------------------------------------------------
import sys, os
from Foam import WM_PROJECT_VERSION
if WM_PROJECT_VERSION() == "1.6":
   if __name__ == "__main__" :
      argv = sys.argv
      if len(argv) > 1 and argv[ 1 ] == "-test":
         argv = None
         test_dir= os.path.join( os.environ[ "PYFOAM_TESTING_DIR" ],'cases', 'r1.6', 'compressible', 'rhoPimpleFoam', 'angledDuct' )
         argv = [ __file__, "-case", test_dir ]
         pass
      os._exit( main_standalone( len( argv ), argv ) )
      pass
   pass   
else:
   from Foam.OpenFOAM import ext_Info
   ext_Info()<< "\nTo use this solver, It is necessary to SWIG OpenFoam1.6\n "


    
#--------------------------------------------------------------------------------------


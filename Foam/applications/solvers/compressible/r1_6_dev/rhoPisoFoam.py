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
                                    IOobject.NO_READ,
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
    
    return p, h, psi, rho, U, phi, turbulence, thermo, DpDt


#--------------------------------------------------------------------------------------
def _UEqn( U, rho, phi, turbulence, p, momentumPredictor ):
    from Foam import fvm
    # Solve the Momentum equation
    
    # The initial C++ expression does not work properly, because of
    #  1. turbulence.divDevRhoReff( U ) - changes values for the U boundaries
    #  2. the order of expression arguments computation differs with C++
    #UEqn = fvm.ddt( rho, U ) + fvm.div( phi, U ) + turbulence.divDevRhoReff( U )
    
    UEqn = turbulence.divDevRhoReff( U ) + ( fvm.ddt( rho, U ) + fvm.div( phi, U ) )

    from Foam.finiteVolume import solve
    if momentumPredictor:
       from Foam.finiteVolume import solve
       from Foam import fvc
       solve( UEqn == -fvc.grad( p ) )
       pass
   
    return UEqn


#--------------------------------------------------------------------------------------
def _hEqn( rho, h, phi, turbulence, DpDt, thermo ):
    from Foam import fvm
    from Foam.finiteVolume import solve
    solve( fvm.ddt(rho, h) + fvm.div( phi, h ) - fvm.laplacian( turbulence.alphaEff(), h ) == DpDt )

    thermo.correct()
    pass


#--------------------------------------------------------------------------------------
def _pEqn( rho, thermo, UEqn, nNonOrthCorr, psi, U, mesh, phi, p, DpDt, cumulativeContErr, corr, nCorr, nOuterCorr, transonic ):
    rho.ext_assign( thermo.rho() )

    rUA = 1.0/UEqn.A()
    U.ext_assign( rUA * UEqn.H() )

    from Foam import fvc, fvm
    from Foam.OpenFOAM import word
    from Foam.finiteVolume import surfaceScalarField
    if transonic: 
       phid = surfaceScalarField( word( "phid" ), 
                                  fvc.interpolate( psi ) * ( ( fvc.interpolate( U ) & mesh.Sf() ) + fvc.ddtPhiCorr( rUA, rho, U, phi ) ) )
       
       for nonOrth in range( nNonOrthCorr + 1 ) :
           pEqn = fvm.ddt( psi, p ) + fvm.div( phid, p ) - fvm.laplacian( rho * rUA, p )
           
           pEqn.solve()
           
           if nonOrth == nNonOrthCorr:
              phi == pEqn.flux()
              pass
           pass
       pass
    else:
       phi.ext_assign( fvc.interpolate( rho ) * ( ( fvc.interpolate(U) & mesh.Sf() ) + fvc.ddtPhiCorr( rUA, rho, U, phi ) ) )
       
       for nonOrth in range( nNonOrthCorr + 1 ) :
           pEqn = fvm.ddt( psi, p ) + fvc.div( phi ) - fvm.laplacian( rho * rUA, p )
           
           pEqn.solve()
                      
           if nonOrth == nNonOrthCorr:
              phi.ext_assign( phi + pEqn.flux() )
              pass
           pass
       pass
        
    from Foam.finiteVolume.cfdTools.compressible import rhoEqn
    rhoEqn( rho, phi )
    
    from Foam.finiteVolume.cfdTools.compressible import compressibleContinuityErrs
    cumulativeContErr = compressibleContinuityErrs( rho, thermo, cumulativeContErr )

    U.ext_assign( U - rUA * fvc.grad( p ) )
    U.correctBoundaryConditions()
    
    DpDt.ext_assign( fvc.DDt( surfaceScalarField( word( "phiU" ), phi / fvc.interpolate( rho ) ), p ) )

    return cumulativeContErr


#--------------------------------------------------------------------------------------
def main_standalone( argc, argv ):

    from Foam.OpenFOAM.include import setRootCase
    args = setRootCase( argc, argv )

    from Foam.OpenFOAM.include import createTime
    runTime = createTime( args )

    from Foam.OpenFOAM.include import createMesh
    mesh = createMesh( runTime )

    p, h, psi, rho, U, phi, turbulence, thermo, DpDt = _createFields( runTime, mesh )
    
    from Foam.finiteVolume.cfdTools.general.include import initContinuityErrs
    cumulativeContErr = initContinuityErrs()
    
    from Foam.finiteVolume.cfdTools.general.include import readTimeControls
    adjustTimeStep, maxCo, maxDeltaT = readTimeControls( runTime )
    
    from Foam.finiteVolume.cfdTools.compressible import compressibleCourantNo
    CoNum, meanCoNum, velMag = compressibleCourantNo( mesh, phi, rho, runTime )
    
    from Foam.finiteVolume.cfdTools.general.include import setInitialDeltaT
    runTime = setInitialDeltaT( runTime, adjustTimeStep, maxCo, maxDeltaT, CoNum )
    
    from Foam.OpenFOAM import ext_Info, nl
    ext_Info() << "\nStarting time loop\n" << nl
    
    while runTime.run() :
        
        from Foam.finiteVolume.cfdTools.general.include import readTimeControls
        adjustTimeStep, maxCo, maxDeltaT = readTimeControls( runTime )

        from Foam.finiteVolume.cfdTools.general.include import readPISOControls
        piso, nCorr, nNonOrthCorr, momentumPredictor, transonic, nOuterCorr = readPISOControls( mesh )

        CoNum, meanCoNum, velMag = compressibleCourantNo( mesh, phi, rho, runTime )
        
        from Foam.finiteVolume.cfdTools.general.include import setDeltaT
        runTime = setDeltaT( runTime, adjustTimeStep, maxCo, maxDeltaT, CoNum )
        
        runTime.increment()
        ext_Info() << "Time = " << runTime.timeName() << nl << nl
        
        from Foam.finiteVolume.cfdTools.compressible import rhoEqn  
        rhoEqn( rho, phi )
        
        UEqn = _UEqn( U, rho, phi, turbulence, p, momentumPredictor )
         
        # --- PISO loop
        for corr in range( nCorr ):
            _hEqn( rho, h, phi, turbulence, DpDt, thermo )
            
            cumulativeContErr = _pEqn( rho, thermo, UEqn, nNonOrthCorr, psi, U, mesh, \
                                phi, p, DpDt, cumulativeContErr, corr, nCorr, nOuterCorr, transonic )
        
        turbulence.correct()
        
        rho.ext_assign( thermo.rho() )
        
        runTime.write()

        ext_Info() << "ExecutionTime = " << runTime.elapsedCpuTime() << " s" << \
              "  ClockTime = " << runTime.elapsedClockTime() << " s" << nl << nl
        
        pass

    ext_Info() << "End\n"

    import os
    return os.EX_OK


#--------------------------------------------------------------------------------------
import sys, os
from Foam import FOAM_BRANCH_VERSION
if FOAM_BRANCH_VERSION( "dev", ">=", "010600" ):
   if __name__ == "__main__" :
      argv = sys.argv
      if len(argv) > 1 and argv[ 1 ] == "-test":
         argv = None
         test_dir= os.path.join( os.environ[ "PYFOAM_TESTING_DIR" ],'cases', 'propogated', 'r1.6-dev', 'compressible', 'rhoPisoFoam', 'ras', 'cavity' )
         argv = [ __file__, "-case", test_dir ]
         pass
      os._exit( main_standalone( len( argv ), argv ) )
      pass
   pass   
else:
   from Foam.OpenFOAM import ext_Info
   ext_Info() << "\n\n To use this solver it is necessary to SWIG OpenFOAM-1.6-ext or higher\n"
   pass
 
    
#--------------------------------------------------------------------------------------


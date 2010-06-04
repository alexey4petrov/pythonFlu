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
def createFields( runTime, mesh ):
    from Foam.OpenFOAM import ext_Info, nl
    ext_Info() <<  "Reading thermophysical properties\n" << nl

    from Foam.thermophysicalModels import  basicThermo, autoPtr_basicThermo
    thermo = basicThermo.New( mesh )

    p = thermo.p()
    h = thermo.h()
    psi = thermo.psi()
    rho = thermo.rho()
    
    from Foam.OpenFOAM import IOdictionary, IOobject, word, fileName
    from Foam.finiteVolume import volScalarField
    
    rho = volScalarField( IOobject( word( "rho" ),
                                    fileName( runTime.timeName() ),
                                    mesh ),
                          rho )
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
    turbulence = compressible.RASModel.New( rho,
                                                    U,
                                                    phi,
                                                    thermo() )
    ext_Info() << "Creating field DpDt\n" << nl
    
    from Foam import fvc
    from Foam.finiteVolume import surfaceScalarField
    
    DpDt = fvc.DDt( surfaceScalarField(word( "phiU" ), phi / fvc.interpolate( rho ) ), p );
        
    return thermo, p, h, psi, rho, U, phi, turbulence, DpDt


#--------------------------------------------------------------------------------------
def _UEqn( U, rho, phi, turbulence, p ):
    from Foam import fvm    
    UEqn = fvm.ddt( rho, U ) + fvm.div( phi, U ) + turbulence.divDevRhoReff( U )
    
    from Foam import fvc
    from Foam.finiteVolume import solve
    solve( UEqn == -fvc.grad( p ) )
    return UEqn


#--------------------------------------------------------------------------------------
def _hEqn( rho, h, phi, turbulence, DpDt, thermo ):
    from Foam import fvm
    from Foam.finiteVolume import solve
    solve( fvm.ddt( rho, h ) + fvm.div( phi, h ) - fvm.laplacian( turbulence.alphaEff(), h ) == DpDt )
    thermo.correct() 
    pass 
    
    
#---------------------------------------------------------------------------------------
def _pEqn( rho, thermo, UEqn, nNonOrthCorr, psi, U, mesh, phi, p, cumulativeContErr ):
    from Foam.finiteVolume import volScalarField
    rUA = 1.0/UEqn.A()
    U.ext_assign( rUA*UEqn.H() )
            
    from Foam import fvc
    from Foam.finiteVolume import surfaceScalarField
    from Foam.OpenFOAM import word
    phid = surfaceScalarField( word( "phid" ), 
                               fvc.interpolate( thermo.psi() ) * ( (fvc.interpolate( U ) & mesh.Sf() ) + fvc.ddtPhiCorr( rUA, rho, U, phi ) ) )
    
    
    for nonOrth in range( nNonOrthCorr + 1 ) :
        from Foam import fvm
        pEqn = ( fvm.ddt(psi, p) + fvm.div(phid, p) - fvm.laplacian(rho*rUA, p) )
        pEqn.solve()
        if (nonOrth == nNonOrthCorr) :
           phi.ext_assign( pEqn.flux() )
           pass
        pass
    from Foam.finiteVolume.cfdTools.compressible import rhoEqn
    rhoEqn( rho, phi )               
    
    from Foam.finiteVolume.cfdTools.compressible import compressibleContinuityErrs
    cumulativeContErr = compressibleContinuityErrs( rho, thermo, cumulativeContErr )
           
    U.ext_assign( U - rUA * fvc.grad(p) )
    U.correctBoundaryConditions()
    
    return cumulativeContErr


#--------------------------------------------------------------------------------------
def main_standalone( argc, argv ):

    from Foam.OpenFOAM.include import setRootCase
    args = setRootCase( argc, argv )

    from Foam.OpenFOAM.include import createTime
    runTime = createTime( args )
    
    from Foam.OpenFOAM.include import createMesh
    mesh = createMesh( runTime )

    thermo, p, h, psi, rho, U, phi, turbulence, DpDt = createFields( runTime, mesh )
    
    from Foam.finiteVolume.cfdTools.general.include import initContinuityErrs
    cumulativeContErr = initContinuityErrs()

    from Foam.OpenFOAM import ext_Info, nl
    ext_Info() <<  "\nStarting time loop\n" << nl

    runTime += runTime.deltaT()
    while not runTime.end() :
        ext_Info() << "Time = " << runTime.timeName() << nl << nl
        
        from Foam.finiteVolume.cfdTools.general.include import readPISOControls
        piso, nCorr, nNonOrthCorr, momentumPredictor, transonic, nOuterCorr, ddtPhiCorr = readPISOControls( mesh )

        from Foam.finiteVolume.cfdTools.compressible import compressibleCourantNo
        CoNum, meanCoNum = compressibleCourantNo( mesh, phi, rho, runTime )
        
        from Foam.finiteVolume.cfdTools.compressible import rhoEqn
        rhoEqn( rho, phi )
        
        UEqn = _UEqn( U, rho, phi, turbulence, p )
        
        _hEqn( rho, h, phi, turbulence, DpDt,thermo )
        

        # -------PISO loop
        for corr in range( nCorr ):
            cumulativeContErr = _pEqn( rho, thermo, UEqn, nNonOrthCorr, psi, U, mesh, phi, p, cumulativeContErr )          
            pass
        from Foam import fvc
        from Foam.finiteVolume import surfaceScalarField
        from Foam.OpenFOAM import word
        DpDt = fvc.DDt( surfaceScalarField( word("phiU"), phi / fvc.interpolate( rho ) ), p )

        
        turbulence.correct()

        rho.ext_assign( psi * p )
                
        runTime.write()

        ext_Info() << "ExecutionTime = " << runTime.elapsedCpuTime() << " s" << \
                      "  ClockTime = " << runTime.elapsedClockTime() << " s" << nl << nl
              
        
        runTime += runTime.deltaT()
        

    ext_Info() << "End\n"

    import os
    return os.EX_OK

    
#--------------------------------------------------------------------------------------
import sys, os
if os.environ["WM_PROJECT_VERSION"] == "1.5" :
   if __name__ == "__main__" :
      argv = sys.argv
      if len(argv) > 1 and argv[ 1 ] == "-test":
         argv = None
         test_dir= os.path.join( os.environ[ "PYFOAM_TESTING_DIR" ],'cases', 'r1.5', 'compressible', 'sonicTurbFoam', 'prism' )
         argv = [ __file__, "-case", test_dir ]
         pass
      os._exit( main_standalone( len( argv ), argv ) )
      pass
   pass
else :
   from Foam.OpenFOAM import ext_Info
   ext_Info() << "\n\n To use this solver it is necessary to SWIG OpenFOAM-1.5\n"
   pass


#--------------------------------------------------------------------------------------


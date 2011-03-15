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
    
    from Foam.OpenFOAM import IOdictionary, IOobject, word, fileName
    from Foam.finiteVolume import volScalarField
    rho = volScalarField( IOobject( word( "rho" ),
                                    fileName( runTime.timeName() ),
                                    mesh,
                                    IOobject.READ_IF_PRESENT,
                                    IOobject.AUTO_WRITE ),
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
    
    pRefCell = 0;
    pRefValue = 0.0;
    from Foam.finiteVolume import setRefCell
    pRefCell, pRefValue = setRefCell( p, mesh.solutionDict().subDict( word( "SIMPLE" ) ), pRefCell, pRefValue )
    
    from Foam.OpenFOAM import dimensionedScalar
    pMin = dimensionedScalar( mesh.solutionDict().subDict( word( "SIMPLE" ) ).lookup( word( "pMin" ) ) )
       
    ext_Info() << "Creating turbulence model\n" << nl
    from Foam import compressible
    turbulence = compressible.RASModel.New( rho, U, phi, thermo() )
    
    from Foam import fvc
    initialMass = fvc.domainIntegrate( rho )
    
    from Foam.finiteVolume import porousZones
    pZones = porousZones( mesh )
    
    from Foam.OpenFOAM import Switch
    pressureImplicitPorosity = Switch( False )

    nUCorr = 0
    
    if pZones.size() :
       # nUCorrectors for pressureImplicitPorosity
       if (mesh.solutionDict().subDict( word( "SIMPLE" ) ).found( word( "nUCorrectors" ) ) ) :
          from Foam.OpenFOAM import readInt
          nUCorr = readInt( mesh.solutionDict().subDict( word( "SIMPLE" ) ).lookup( word( "nUCorrectors" ) ) )
          pass
       if nUCorr > 0 :
          pressureImplicitPorosity = True
          pass
       pass
    
    return p, h, psi, rho, U, phi, turbulence, thermo, pZones, pMin, pressureImplicitPorosity, initialMass, nUCorr, pRefCell, pRefValue


#------------------------------------------------------------------------------------------------------
def initConvergenceCheck( simple ):
    eqnResidual = 1
    maxResidual = 0
    convergenceCriterion = 0.0
    
    from Foam.OpenFOAM import word
    tmp, convergenceCriterion = simple.readIfPresent( word( "convergence" ), convergenceCriterion )

    return eqnResidual, maxResidual, convergenceCriterion


#------------------------------------------------------------------------------------- 
def _UEqn( phi, U, p, turbulence, pZones, pressureImplicitPorosity, nUCorr, eqnResidual, maxResidual ):
    
    from Foam import fvm, fvc    
    # Construct the Momentum equation

    # The initial C++ expression does not work properly, because of
    #  1. turbulence.divDevRhoReff( U ) - changes values for the U boundaries
    #  2. the order of expression arguments computation differs with C++
    #UEqn = fvm.div( phi, U ) + turbulence.divDevRhoReff( U ) 

    UEqn = turbulence.divDevRhoReff( U ) + fvm.div( phi, U ) 

    UEqn.relax()

    # Include the porous media resistance and solve the momentum equation
    # either implicit in the tensorial resistance or transport using by
    # including the spherical part of the resistance in the momentum diagonal

    trAU = None
    trTU = None
    if pressureImplicitPorosity :
        from Foam.finiteVolume import sphericalTensor, tensor
        tTU = tensor( sphericalTensor.I ) * UEqn.A()

        pZones.addResistance( UEqn, tTU )
    
        trTU = tTU.inv()
               
        from Foam.OpenFOAM import word
        trTU.rename( word( "rAU" ) )
        
        for UCorr in range ( nUCorr ):
            U.ext_assign( trTU & ( UEqn.H() - fvc.grad( p ) ) )
            pass
        
        U.correctBoundaryConditions()
    else:
        pZones.addResistance( UEqn )
        
        from Foam.finiteVolume import solve
        eqnResidual =  solve( UEqn == - fvc.grad( p ) ).initialResidual()
        
        maxResidual = max( eqnResidual, maxResidual )
        
        trAU = 1.0 / UEqn.A()
        
        from Foam.OpenFOAM import word
        trAU.rename( word( "rAU" ) )
        
        pass
    
    return UEqn, trTU, trAU, eqnResidual, maxResidual


#---------------------------------------------------------------------------------------
def _hEqn( thermo, phi, h, turbulence, p, rho, eqnResidual, maxResidual):
    from Foam.finiteVolume import fvScalarMatrix
    from Foam import fvc, fvm
    
    
    left_expr = fvm.div( phi, h ) - fvm.Sp( fvc.div( phi ), h ) - fvm.laplacian( turbulence.alphaEff(), h )
    from Foam.OpenFOAM import word
    right_expr = fvc.div( phi / fvc.interpolate( rho ) * fvc.interpolate( p, word( "div(U,p)" ) ) ) - p * fvc.div( phi / fvc.interpolate( rho ) )
    
    hEqn =  ( left_expr == right_expr ) 
        
    hEqn.relax()
    
    eqnResidual = hEqn.solve().initialResidual()
    maxResidual = max( eqnResidual, maxResidual )

    thermo.correct()
    
    return hEqn, eqnResidual, maxResidual 


#----------------------------------------------------------------------------------------    
def _pEqn( mesh, rho, thermo, p, U, trTU, trAU, UEqn, phi, \
           runTime, pMin, pressureImplicitPorosity, nNonOrthCorr, eqnResidual, maxResidual, cumulativeContErr, initialMass, pRefCell, pRefValue ):
   
    if pressureImplicitPorosity :
       U.ext_assign( trTU & UEqn.H() )
    else:
       U.ext_assign( trAU * UEqn.H() )
       pass
    
    UEqn.clear() 
    
    from Foam import fvc, fvm
    phi.ext_assign( fvc.interpolate( rho * U ) & mesh.Sf() )

    from Foam.finiteVolume import adjustPhi
    closedVolume = adjustPhi( phi, U, p )
    
    for nonOrth in range( nNonOrthCorr + 1 ) :
        tpEqn = None
        if pressureImplicitPorosity :
            tpEqn = ( fvm.laplacian( rho * trTU, p ) == fvc.div( phi ) )
        else:
            tpEqn = (fvm.laplacian( rho * trAU, p ) == fvc.div( phi ) )
            pass
        
        tpEqn.setReference( pRefCell, pRefValue )
        # retain the residual from the first iteration
        if nonOrth == 0 :
            eqnResidual = tpEqn.solve().initialResidual()
            maxResidual = max( eqnResidual, maxResidual )
        else:
            tpEqn.solve()
            pass
        
        if nonOrth == nNonOrthCorr :
            phi.ext_assign( phi - tpEqn.flux() )
            pass
        
        pass
    
    from Foam.finiteVolume.cfdTools.incompressible import continuityErrs
    cumulativeContErr = continuityErrs( mesh, phi, runTime, cumulativeContErr )

    # Explicitly relax pressure for momentum corrector
    p.relax()
           
    if pressureImplicitPorosity :
        U.ext_assign( U - ( trTU & fvc.grad( p ) ) )
    else:
        U.ext_assign( U - ( trAU * fvc.grad( p ) ) )
        pass
       
    U.correctBoundaryConditions()

    from Foam.finiteVolume import bound
    bound( p, pMin )
    
    # For closed-volume cases adjust the pressure and density levels
    # to obey overall mass continuity
    if closedVolume :
       p.ext_assign( p + ( initialMass - fvc.domainIntegrate( psi * p ) ) / fvc.domainIntegrate( psi ) )
       pass
   
    rho.ext_assign( thermo.rho() )
    rho.relax()
    
    from Foam.OpenFOAM import ext_Info, nl
    ext_Info()<< "rho max/min : " << rho.ext_max().value() << " " << rho.ext_min().value() << nl
    
    return  eqnResidual, maxResidual
        
    
#----------------------------------------------------------------------------------------    
def convergenceCheck( runTime, maxResidual, convergenceCriterion ):
    if maxResidual < convergenceCriterion :
        from Foam.OpenFOAM import ext_Info, nl
        ext_Info << "reached convergence criterion: " << convergenceCriterion <<nl
        runTime.writeAndEnd()
        ext_Info << "latestTime =" << runTime.timeName()
        pass
    
    pass
    

#-----------------------------------------------------------------------------------------
def main_standalone( argc, argv ):

    from Foam.OpenFOAM.include import setRootCase
    args = setRootCase( argc, argv )

    from Foam.OpenFOAM.include import createTime
    runTime = createTime( args )

    from Foam.OpenFOAM.include import createMesh
    mesh = createMesh( runTime )

    p, h, psi, rho, U, phi, turbulence, thermo, pZones, pMin,\
    pressureImplicitPorosity, initialMass, nUCorr, pRefCell, pRefValue  = _createFields( runTime, mesh )
      
    from Foam.finiteVolume.cfdTools.general.include import initContinuityErrs
    cumulativeContErr = initContinuityErrs()
    
    from Foam.OpenFOAM import ext_Info, nl
    ext_Info()<< "\nStarting time loop\n" << nl
    
    while runTime.loop() :
        ext_Info() << "Time = " << runTime.timeName() << nl << nl
        
        from Foam.finiteVolume.cfdTools.general.include import readSIMPLEControls
        simple, nNonOrthCorr, momentumPredictor, fluxGradp, transonic = readSIMPLEControls( mesh )
        
        eqnResidual, maxResidual, convergenceCriterion = initConvergenceCheck( simple )
        
        p.storePrevIter()
        rho.storePrevIter()
        # Pressure-velocity SIMPLE corrector
        
        UEqn, trTU, trAU, eqnResidual, maxResidual = _UEqn( phi, U, p, turbulence, pZones,\
                                                                        pressureImplicitPorosity, nUCorr, eqnResidual, maxResidual )
        
        hEqn, eqnResidual, maxResidual = _hEqn( thermo, phi, h, turbulence, p, rho, eqnResidual, maxResidual )
        
        eqnResidual, maxResidual = _pEqn( mesh, rho, thermo, p, U, trTU, trAU, UEqn, phi, \
                                          runTime, pMin, pressureImplicitPorosity, nNonOrthCorr, eqnResidual,\
                                          maxResidual, cumulativeContErr, initialMass, pRefCell, pRefValue )
        
        turbulence.correct();

        runTime.write()
        ext_Info() << "ExecutionTime = " << runTime.elapsedCpuTime() << " s" \
                   << "  ClockTime = " << runTime.elapsedClockTime() << " s" \
                   << nl << nl
        
        convergenceCheck( runTime, maxResidual, convergenceCriterion)
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
         test_dir= os.path.join( os.environ[ "PYFOAM_TESTING_DIR" ],'cases', 'propogated', 'r1.6-dev', 'compressible', 'rhoPorousSimpleFoam', 'angledDuctExplicit' )
         argv = [ __file__, "-case", test_dir ]
         pass
      os._exit( main_standalone( len( argv ), argv ) )
      pass
   pass
else:
   from Foam.OpenFOAM import ext_Info
   ext_Info()<< "\nTo use this solver, It is necessary to SWIG OpenFoam1.6-ext or higher \n "


#--------------------------------------------------------------------------------------


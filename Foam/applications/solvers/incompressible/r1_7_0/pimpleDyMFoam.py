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
    from Foam.OpenFOAM import IOdictionary, IOobject, word, fileName
    from Foam.finiteVolume import volScalarField
    
    ext_Info() << "Reading field p\n" << nl
    p = volScalarField( IOobject( word( "p" ),
                                  fileName( runTime.timeName() ),
                                  mesh(),
                                  IOobject.MUST_READ,
                                  IOobject.AUTO_WRITE ),
                        mesh() )
    
    from Foam.finiteVolume import volVectorField
    ext_Info() << "Reading field U\n" << nl
    U = volVectorField( IOobject( word( "U" ),
                                  fileName( runTime.timeName() ),
                                  mesh() ,
                                  IOobject.MUST_READ,
                                  IOobject.AUTO_WRITE ),
                        mesh() )
    
    from Foam.finiteVolume.cfdTools.incompressible import createPhi
    phi = createPhi( runTime, mesh(), U )
    
    pRefCell = 0
    pRefValue = 0.0
    
    from Foam.finiteVolume import setRefCell
    pRefCell, pRefValue = setRefCell( p, mesh.solutionDict().subDict( word( "PIMPLE" ) ), pRefCell, pRefValue )
    
    from Foam.transportModels import singlePhaseTransportModel
    laminarTransport = singlePhaseTransportModel( U, phi )
    
    from Foam import incompressible
    turbulence = incompressible.turbulenceModel.New( U, phi, laminarTransport )
    
    from Foam.finiteVolume import zeroGradientFvPatchScalarField
    ext_Info() << "Reading field rAU if present\n" << nl
    rAU = volScalarField( IOobject( word( "rAU" ),
                                    fileName( runTime.timeName() ),
                                    mesh(),
                                    IOobject.READ_IF_PRESENT,
                                    IOobject.AUTO_WRITE ),
                          mesh(),
                          runTime.deltaT(),
                          zeroGradientFvPatchScalarField.typeName )
    
    return p, U, phi, laminarTransport, turbulence, rAU, pRefCell, pRefValue


#--------------------------------------------------------------------------------------
def readControls( runTime, mesh ):
    from Foam.finiteVolume.cfdTools.general.include import readTimeControls
    adjustTimeStep, maxCo, maxDeltaT = readTimeControls( runTime )
    
    from Foam.finiteVolume.cfdTools.general.include import readPIMPLEControls
    pimple, nOuterCorr, nCorr, nNonOrthCorr, momentumPredictor, transonic = readPIMPLEControls( mesh )
    
    correctPhi = False
    from Foam.OpenFOAM import word
    if (pimple.found( word( "correctPhi" ) ) ):
       correctPhi = Switch( pimple.lookup( word( "correctPhi" ) ) )
       pass
  
    checkMeshCourantNo = False
    if ( pimple.found( word( "checkMeshCourantNo" ) ) ):
        checkMeshCourantNo = Switch( pimple.lookup( "checkMeshCourantNo" ) )
        pass

    return adjustTimeStep, maxCo, maxDeltaT, pimple, nOuterCorr, nCorr, nNonOrthCorr, \
           momentumPredictor, transonic, correctPhi, checkMeshCourantNo
    
#--------------------------------------------------------------------------------------
def _correctPhi( runTime, mesh, p, rAU, phi, nNonOrthCorr, pRefCell, pRefValue, cumulativeContErr ):
    if mesh.changing():
       for patchi in range( U.boundaryField().size() ):
           if U.boundaryField()[patchi].fixesValue():
              U.boundaryField()[patchi].initEvaluate()
              pass
           pass
       for patchi in range( U.boundaryField().size() ):
           if U.boundaryField()[patchi].fixesValue():
              U.boundaryField()[patchi].evaluate()
              phi.boundaryField()[patchi].ext_assign( U.boundaryField()[patchi] & mesh.Sf().boundaryField()[patchi] )
              pass
           pass
       pass
       
    from Foam.OpenFOAM import wordList
    from Foam.finiteVolume import zeroGradientFvPatchScalarField
    pcorrTypes = wordList( p.ext_boundaryField().size(), zeroGradientFvPatchScalarField.typeName )
    
    from Foam.finiteVolume import fixedValueFvPatchScalarField
    for i in range( p.ext_boundaryField().size() ):
        if p.ext_boundaryField()[i].fixesValue():
           pcorrTypes[i] = fixedValueFvPatchScalarField.typeName
           pass
        pass
    
    from Foam.finiteVolume import volScalarField
    from Foam.OpenFOAM import IOobject, word, fileName, dimensionedScalar
    pcorr = volScalarField( IOobject( word( "pcorr" ),
                                      fileName( runTime.timeName() ),
                                      mesh(),
                                      IOobject.NO_READ,
                                      IOobject.NO_WRITE ),
                            mesh(),
                            dimensionedScalar( word( "pcorr" ), p.dimensions(), 0.0),
                            pcorrTypes )
     
    for nonOrth in range( nNonOrthCorr + 1 ):
        from Foam import fvm,fvc
        pcorrEqn = ( fvm.laplacian( rAU, pcorr ) == fvc.div( phi ) )

        pcorrEqn.setReference(pRefCell, pRefValue)
        pcorrEqn.solve()

        if nonOrth == nNonOrthCorr:
           phi.ext_assign( phi - pcorrEqn.flux() )
           pass
        pass
    from Foam.finiteVolume.cfdTools.general.include import ContinuityErrs
    cumulativeContErr = ContinuityErrs( phi, runTime, mesh, cumulativeContErr )     

    return cumulativeContErr

#--------------------------------------------------------------------------------------
def _UEqn( mesh, phi, U, p, turbulence, ocorr, nOuterCorr, momentumPredictor ):
    from Foam import fvm
    UEqn = fvm.ddt(U) + fvm.div(phi, U) + turbulence.divDevReff( U ) 
    
    if ocorr != nOuterCorr - 1:
       UEqn.relax()
       pass
    
    if momentumPredictor:
       from Foam.finiteVolume import solve
       from Foam import fvc
       solve( UEqn == -fvc.grad( p ) )
       pass
    
    return UEqn


#--------------------------------------------------------------------------------------
def main_standalone( argc, argv ):

    from Foam.OpenFOAM.include import setRootCase
    args = setRootCase( argc, argv )

    from Foam.OpenFOAM.include import createTime
    runTime = createTime( args )

    from Foam.dynamicFvMesh import createDynamicFvMesh
    mesh = createDynamicFvMesh( runTime )
    
    from Foam.finiteVolume.cfdTools.general.include import readPIMPLEControls
    pimple, nOuterCorr, nCorr, nNonOrthCorr, momentumPredictor, transonic = readPIMPLEControls( mesh )
    
    from Foam.finiteVolume.cfdTools.general.include import initContinuityErrs
    cumulativeContErr = initContinuityErrs()

    p, U, phi, laminarTransport, turbulence, rAU, pRefCell, pRefValue = _createFields( runTime, mesh )    
    
    from Foam.finiteVolume.cfdTools.general.include import readTimeControls
    adjustTimeStep, maxCo, maxDeltaT = readTimeControls( runTime )
    
    from Foam.OpenFOAM import ext_Info, nl
    ext_Info() << "\nStarting time loop\n" <<nl
    
    while runTime.run() :
        
        adjustTimeStep, maxCo, maxDeltaT, pimple, nOuterCorr, nCorr, nNonOrthCorr, \
                        momentumPredictor, transonic, correctPhi, checkMeshCourantNo = readControls( runTime, mesh )
        
        from Foam.finiteVolume.cfdTools.general.include import CourantNo
        CoNum, meanCoNum = CourantNo( mesh, phi, runTime )
        
        # Make the fluxes absolute
        from Foam import fvc
        fvc.makeAbsolute(phi, U)
      
        from Foam.finiteVolume.cfdTools.general.include import setDeltaT
        runTime = setDeltaT( runTime, adjustTimeStep, maxCo, maxDeltaT, CoNum )
        
        runTime.increment()
                
        ext_Info() << "Time = " << runTime.timeName() << nl << nl
        
        mesh.update()
        
        if mesh.changing() and correctPhi :
           cumulativeContErr = _correctPhi( runTime, mesh, p, rAU, phi, nNonOrthCorr, pRefCell, pRefValue, cumulativeContErr  )
           pass
        
        # Make the fluxes relative to the mesh motion
        fvc.makeRelative( phi, U )
        
        
        if mesh.changing() and checkMeshCourantNo :
           from Foam.dynamicFvMesh import meshCourantNo
           meshCoNum, meanMeshCoNum = meshCourantNo( runTime, mesh, phi )
           pass
        
        from Foam import fvm
        #PIMPLE loop
        for ocorr in range( nOuterCorr ):
           if nOuterCorr != 1:
              p.storePrevIter()
              pass
           UEqn = _UEqn( mesh, phi, U, p, turbulence, ocorr, nOuterCorr, momentumPredictor )
           
           # --- PISO loop
           for corr in range( nCorr ):
              rAU.ext_assign( 1.0 / UEqn.A() )
              
              U.ext_assign( rAU * UEqn.H() )
              phi.ext_assign( fvc.interpolate( U ) & mesh.Sf() )
              
              if p.needReference() :
                 fvc.makeRelative( phi, U )
                 adjustPhi( phi, U, p )
                 fvc.makeAbsolute( phi, U )
                 pass
              
              for nonOrth in range( nNonOrthCorr + 1 ):
                 pEqn = ( fvm.laplacian( rAU, p ) == fvc.div( phi ) )
                 
                 pEqn.setReference( pRefCell, pRefValue )
                 
                 if ocorr == nOuterCorr - 1 and corr == nCorr - 1 \
                                            and nonOrth == nNonOrthCorr :
                    from Foam.OpenFOAM import word
                    pEqn.solve( mesh.solver( word( str( p.name() ) + "Final" ) ) )
                    pass
                 else:
                    pEqn.solve( mesh.solver( p.name() ) )
                    pass
                    
                 if nonOrth == nNonOrthCorr:
                    phi.ext_assign( phi - pEqn.flux() )
                    pass
                 
                 pass
                 
              from Foam.finiteVolume.cfdTools.general.include import ContinuityErrs
              cumulativeContErr = ContinuityErrs( phi, runTime, mesh, cumulativeContErr )
                 
              # Explicitly relax pressure for momentum corrector
              if ocorr != nOuterCorr - 1:
                 p.relax()
                 pass
                 
              # Make the fluxes relative to the mesh motion
              fvc.makeRelative( phi, U )
              U.ext_assign( U - rAU * fvc.grad( p ) )
              U.correctBoundaryConditions()
              pass
           turbulence.correct()   
           pass

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
if FOAM_VERSION( ">=", "010700" ):
   if __name__ == "__main__" :
      argv = sys.argv
      if len( argv ) > 1 and argv[ 1 ] == "-test":
         argv = None
         test_dir= os.path.join( os.environ[ "PYFOAM_TESTING_DIR" ],'cases', 'propogated', 'r1.6', 'incompressible', 'pimpleDyMFoam', 'movingCone' )
         argv = [ __file__, "-case", test_dir ]
         pass
      os._exit( main_standalone( len( argv ), argv ) )
else :
   from Foam.OpenFOAM import ext_Info
   ext_Info() << "\n\n To use this solver it is necessary to SWIG OpenFOAM-1.7.0\n"
   pass

    
#--------------------------------------------------------------------------------------


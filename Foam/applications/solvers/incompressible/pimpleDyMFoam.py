#!/usr/bin/env python

#--------------------------------------------------------------------------------------
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
## See https://csrcs.pbmr.co.za/svn/nea/prototypes/reaktor/pyfoam
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
    setRefCell( p, mesh.solutionDict().subDict( word( "PIMPLE" ) ), pRefCell, pRefValue )
    
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
       correctPhi = Switch(pimple.lookup( word( "correctPhi" ) ) )
  
    checkMeshCourantNo = False
    if ( pimple.found( word( "checkMeshCourantNo" ) ) ):
        checkMeshCourantNo = Switch(pimple.lookup("checkMeshCourantNo"));

    return adjustTimeStep, maxCo, maxDeltaT, pimple, nOuterCorr, nCorr, nNonOrthCorr, \
           momentumPredictor, transonic, correctPhi, checkMeshCourantNo
    
#--------------------------------------------------------------------------------------
def Ueqn( mesh, phi, U, p, turbulence, oCorr, nOuterCorr, momentumPredictor ):
    from Foam import fvm, fvc

    pass


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
        
        runTime += runTime.deltaT()
                
        ext_Info() << "Time = " << runTime.timeName() << nl << nl
        
        mesh.update()
        
        if mesh.changing() and correctPhi :
           pass

        runTime.write();
        
        ext_Info() << "ExecutionTime = " << runTime.elapsedCpuTime() << " s" << \
              "  ClockTime = " << runTime.elapsedClockTime() << " s" << nl << nl
        
        pass

    ext_Info() << "End\n" << nl 

    import os
    return os.EX_OK


#--------------------------------------------------------------------------------------
import sys, os
from Foam import WM_PROJECT_VERSION
if WM_PROJECT_VERSION() >= "1.6" :
   if __name__ == "__main__" :
     argv = sys.argv
     os._exit( main_standalone( len( argv ), argv ) )
     pass
   else :
      argv = None
      test_dir= os.path.join( os.environ[ "PYFOAM_TESTING_DIR" ],'cases', 'r1.6', 'incompressible', 'pimpleDyMFoam', 'movingCone' )
      argv = [ __file__, "-case", test_dir ]
      os._exit( main_standalone( len( argv ), argv ) )
      pass
else :
   from Foam.OpenFOAM import ext_Info
   ext_Info() << "\n\n To use this solver it is necessary to SWIG OpenFOAM-1.6\n"
   pass

    
#--------------------------------------------------------------------------------------


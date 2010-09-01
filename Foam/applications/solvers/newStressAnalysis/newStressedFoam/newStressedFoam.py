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
from Foam.OpenFOAM import ext_Info, nl,word
from Foam.applications.solvers.newStressAnalysis.materialModels.fvPatchFields import tractionDisplacement


from Foam.applications.solvers.newStressAnalysis.materialModels.rheologyModel.rheologyLaws import multiMaterial, linearElastic
from Foam.applications.solvers.newStressAnalysis.materialModels.rheologyModel.rheologyLaws import addDictionaryConstructorTable
multiMaterial_addDictionaryConstructorTable = addDictionaryConstructorTable( "multiMaterial", multiMaterial )
linearElastic_addDictionaryConstructorTable = addDictionaryConstructorTable( "linearElastic", linearElastic )

#---------------------------------------------------------------------------
def createFields( runTime, mesh ):
    ext_Info() << "Reading field U\n" << nl
    
    from Foam.finiteVolume import volVectorField
    from Foam.OpenFOAM import IOobject, fileName, word
    U = volVectorField( IOobject( word( "U" ),
                                  fileName( runTime.timeName() ),
                                  mesh,
                                  IOobject.MUST_READ,
                                  IOobject.AUTO_WRITE ),
                        mesh )

    from Foam.finiteVolume import volSymmTensorField
    from Foam.OpenFOAM import dimensionedSymmTensor, symmTensor
    from Foam.OpenFOAM import dimForce, dimArea
    sigma = volSymmTensorField( IOobject( word( "sigma" ),
                                          fileName( runTime.timeName() ),
                                          mesh,
                                          IOobject.READ_IF_PRESENT,
                                          IOobject.AUTO_WRITE ),
                                mesh,
                                dimensionedSymmTensor( word( "zero" ), dimForce/dimArea, symmTensor.zero)
                              )
    
    from Foam.applications.solvers.newStressAnalysis.materialModels.rheologyModel import rheologyModel
    rheology = rheologyModel( sigma )

    return U, sigma, rheology


#--------------------------------------------------------------------------------------
def readStressedFoamControls( mesh):
    from Foam.OpenFOAM import word
    stressControl = mesh.solutionDict().subDict( word( "stressedFoam" ) )
    
    from Foam.OpenFOAM import readInt
    nCorr = readInt( stressControl.lookup( word( "nCorrectors" ) ) )
    
    from Foam.OpenFOAM import readScalar
    convergenceTolerance = readScalar(stressControl.lookup( word( "U" ) ) )
    
    from Foam.applications.solvers.newStressAnalysis.materialModels.componentReference import componentReference
    from Foam.template import PtrList
    
    cr = PtrList( componentReference )( stressControl.lookup( word( "componentReference" ) ), componentReference.iNew(mesh) )

    return stressControl, nCorr, convergenceTolerance, cr


#--------------------------------------------------------------------------------------
def setComponentReference( cr, UEqn ):
    for crI in cr:
        UEqn.setComponentReference( crI.patchIndex(),
                                    crI.faceIndex(),
                                    crI.dir(),
                                    crI.value() )
    pass


#--------------------------------------------------------------------------------------
def calculateSigma( sigma, mu, gradU, _lambda ):
    from Foam.OpenFOAM import I
    sigma.ext_assign( 2*mu*gradU.symm() + _lambda*(I*gradU.tr()) )
    pass
    

#--------------------------------------------------------------------------------------
def calculateStress( runTime, mesh, sigma, _lambda ):
    if (runTime.outputTime()):
       from Foam.finiteVolume import volScalarField
       from Foam.OpenFOAM import word, IOobject, fileName
       sigmaEq = volScalarField( IOobject( word( "sigmaEq" ),
                                           fileName( runTime.timeName() ),
                                           mesh,
                                           IOobject.NO_READ,
                                           IOobject.AUTO_WRITE ),
                                  (  (3.0/2.0)*sigma.dev() .magSqr() ).sqrt() )
       ext_Info() << "Max sigmaEq = " << sigmaEq.ext_max().value() << nl
       
       from Foam.OpenFOAM import symmTensor
       sigmaxx = volScalarField( IOobject( word( "sigmaxx" ),
                                           fileName( runTime.timeName() ),
                                           mesh,
                                           IOobject.NO_READ,
                                           IOobject.AUTO_WRITE ),
                                 sigma.component(symmTensor.XX) )
       
       sigmayy = volScalarField( IOobject( word( "sigmayy" ),
                                           fileName( runTime.timeName() ),
                                           mesh,
                                           IOobject.NO_READ,
                                           IOobject.AUTO_WRITE ),
                                 sigma.component(symmTensor.YY) )

       sigmazz = volScalarField( IOobject( word( "sigmazz" ),
                                           fileName( runTime.timeName() ),
                                           mesh,
                                           IOobject.NO_READ,
                                           IOobject.AUTO_WRITE ),
                                 sigma.component(symmTensor.ZZ) )
       ext_Info() << "Max sigmazz = " << sigmazz.ext_max().value() << nl
       
       sigmaxy = volScalarField( IOobject( word( "sigmaxy" ),
                                           fileName( runTime.timeName() ),
                                           mesh,
                                           IOobject.NO_READ,
                                           IOobject.AUTO_WRITE ),
                                 sigma.component(symmTensor.XY) )

       sigmaxz = volScalarField( IOobject( word( "sigmaxz" ),
                                           fileName( runTime.timeName() ),
                                           mesh,
                                           IOobject.NO_READ,
                                           IOobject.AUTO_WRITE ),
                                 sigma.component(symmTensor.XZ) )

       sigmayz = volScalarField( IOobject( word( "sigmayz" ),
                                           fileName( runTime.timeName() ),
                                           mesh,
                                           IOobject.NO_READ,
                                           IOobject.AUTO_WRITE ),
                                 sigma.component(symmTensor.YZ) )
       
       runTime.write()
    pass
    

#--------------------------------------------------------------------------------------

def main_standalone( argc, argv ):

    from Foam.OpenFOAM.include import setRootCase
    args = setRootCase( argc, argv )

    from Foam.OpenFOAM.include import createTime
    runTime = createTime( args )
    
    from Foam.OpenFOAM.include import createMesh
    mesh = createMesh( runTime )

    U, sigma, rheology = createFields( runTime, mesh )
    
    ext_Info() << "\nCalculating displacement field\n" << nl
    
    from Foam import fvc
    gradU = fvc.grad( U )
    
    rho = rheology.rho()
    runTime += runTime.deltaT()
    while not runTime.end() :
        
        ext_Info() << "Iteration: " << runTime.timeName() << nl << nl
        stressControl, nCorr, convergenceTolerance, cr = readStressedFoamControls( mesh )
        
        mu = rheology.mu()
        _lambda = rheology._lambda()

        iCorr = 0
        initialResidual = 0
        
        while True:
            from Foam import fvm
            from Foam.OpenFOAM import word
            from Foam.OpenFOAM import I
            
            UEqn = fvm.d2dt2( rho,U ) == fvm.laplacian( 2*mu + _lambda, U, word( "laplacian(DU,U)" ) ) \
                                       + fvc.div( mu*gradU.T() + _lambda*( I * gradU.tr() ) - ( mu + _lambda )*gradU , \
                                                  word("div(sigma)") )
            
            setComponentReference( cr, UEqn )
            
            initialResidual = UEqn.solve().initialResidual()
                        
            gradU.ext_assign( fvc.grad( U ) )
            
            calculateSigma( sigma, mu, gradU, _lambda )
            
            rheology.correct()

            rho.ext_assign( rheology.rho() )
            mu.ext_assign( rheology.mu() )
            _lambda.ext_assign( rheology._lambda() )
            
            if  (initialResidual > convergenceTolerance) and (++iCorr < nCorr):
               break
        
        calculateStress( runTime, mesh, sigma, _lambda )

        ext_Info() << "ExecutionTime = " << runTime.elapsedCpuTime() << " s\n\n" << nl
        
        runTime += runTime.deltaT()
        
        pass

    ext_Info() << "End\n"

    import os
    return os.EX_OK

    
#--------------------------------------------------------------------------------------
import sys, os
from Foam import FOAM_VERSION
if FOAM_VERSION( "<", "010500" ):
   if __name__ == "__main__" :
      argv = sys.argv
      if len( argv ) >1 and argv[ 1 ]=="-test":
        argv = None
        test_dir= os.path.join( os.environ[ "PYFOAM_TESTING_DIR" ],'cases', 'local', 'r1.4.1-dev', 'newStressedFoam' )
        argv = [ __file__, test_dir, 'plateHole' ] 
        pass
      os._exit( main_standalone( len( argv ), argv ) )
      pass
else :
   from Foam.OpenFOAM import ext_Info
   ext_Info() << "\n\n To use this solver it is necessary to SWIG OpenFOAM-1.4.X\n"
   pass


#--------------------------------------------------------------------------------------


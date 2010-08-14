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


#----------------------------------------------------------------------------
def _createFields( runTime, mesh ):
    from Foam.OpenFOAM import ext_Info, nl
    from Foam.OpenFOAM import IOdictionary, IOobject, word, fileName
    from Foam.finiteVolume import volVectorField
        
    ext_Info() << "Reading field U\n" << nl
    U = volVectorField( IOobject( word( "U" ),
                                  fileName( runTime.timeName() ),
                                  mesh,
                                  IOobject.MUST_READ,
                                  IOobject.AUTO_WRITE ),
                        mesh )
    
    ext_Info() << "Creating face flux\n" << nl
    from Foam.OpenFOAM import dimensionedScalar
    from Foam.finiteVolume import surfaceScalarField
    phi = surfaceScalarField( IOobject( word( "phi" ),
                                        fileName( runTime.timeName() ),
                                        mesh,
                                        IOobject.NO_READ,
                                        IOobject.NO_WRITE ),
                              mesh,
                              dimensionedScalar( word( "zero" ), mesh.Sf().dimensions()*U.dimensions(), 0.0) )

    
    from Foam.transportModels import singlePhaseTransportModel
    laminarTransport = singlePhaseTransportModel( U, phi )
    
    from Foam import incompressible
    turbulence = incompressible.RASModel.New( U, phi, laminarTransport )
    
    transportProperties = IOdictionary( IOobject( word( "transportProperties" ),
                                        fileName( runTime.constant() ),
                                        mesh,
                                        IOobject.MUST_READ,
                                        IOobject.NO_WRITE ) )
    from Foam.OpenFOAM import dimensionedVector, vector
    Ubar = dimensionedVector( transportProperties.lookup( word( "Ubar" ) ) )
    
    flowDirection = ( Ubar / Ubar.mag() ).ext_value()
    flowMask = flowDirection.sqr()
    
    nWallFaces = 0.0
    from Foam.OpenFOAM import vector
    wallNormal = vector.zero
    
    patches = mesh.boundary()
    
    for patchi in range( mesh.boundary().size() ):
        currPatch = patches[patchi]
        
        from Foam.finiteVolume import wallFvPatch
        if wallFvPatch.ext_isType( currPatch ):
           
           for facei in range( currPatch.size() ):
               nWallFaces = nWallFaces +1
               
               if nWallFaces == 1:
                  wallNormal = - mesh.Sf().ext_boundaryField()[patchi][facei] / mesh.magSf().ext_boundaryField()[patchi][facei]
                  pass
               elif nWallFaces == 2:
                  wallNormal2 = mesh.Sf().ext_boundaryField()[patchi][facei] / mesh.magSf().ext_boundaryField()[patchi][facei]
                  
                  #- Check that wall faces are parallel
                  from Foam.OpenFOAM import mag
                  if mag(wallNormal & wallNormal2) > 1.01 or mag(wallNormal & wallNormal2) < 0.99:
                     ext_Info() << "boundaryFoam: wall faces are not parallel" << nl
                     import os
                     os.abort()
                     pass
                  pass
               else:
                  ext_Info() << "boundaryFoam: number of wall faces > 2" << nl
                  import os
                  os.abort()
               pass
           pass
        pass
    #- create position array for graph generation
    y = wallNormal & mesh.C().internalField()
    
    from Foam.OpenFOAM import dimensionSet, vector, word
    gradP = dimensionedVector( word( "gradP" ),
                               dimensionSet( 0.0, 1.0, -2.0, 0.0, 0.0 ),
                               vector( 0.0, 0.0, 0.0 ) )
              
    return U, phi, laminarTransport, turbulence, Ubar, wallNormal, flowDirection, flowMask, y, gradP


#--------------------------------------------------------------------------------------
def main_standalone( argc, argv ):

    from Foam.OpenFOAM.include import setRootCase
    args = setRootCase( argc, argv )

    from Foam.OpenFOAM.include import createTime
    runTime = createTime( args )

    from Foam.OpenFOAM.include import createMesh
    mesh = createMesh( runTime )
    
    U, phi, laminarTransport, turbulence, Ubar, wallNormal, flowDirection, flowMask, y, gradP = _createFields( runTime, mesh )
    
    from Foam.OpenFOAM import ext_Info, nl
    ext_Info() << "\nStarting time loop\n" << nl 
    
    while runTime.loop() :
        ext_Info() << "\nTime = " << runTime.timeName() << nl << nl
        
        divR = turbulence.divDevReff( U )
        divR.source().ext_assign( flowMask & divR.source() )
        
        UEqn = divR == gradP 
        UEqn.relax()

        UEqn.solve()
        
        # Correct driving force for a constant mass flow rate

        UbarStar = flowMask & U.weightedAverage(mesh.V())
        
        U.ext_assign( U + ( Ubar - UbarStar ) )
        gradP += ( Ubar - UbarStar ) / ( 1.0 / UEqn.A() ).weightedAverage( mesh.V() )
        
        id_ = y.size() - 1
        
        wallShearStress = flowDirection & turbulence.R()()[id_] & wallNormal
        from Foam.OpenFOAM import  mag
        from math import sqrt
        yplusWall = sqrt( mag( wallShearStress ) )  * y()[ id_ ] / turbulence.nuEff()()[ id_ ]
        
        ext_Info() << "Uncorrected Ubar = " << ( flowDirection & UbarStar.value() )<< "       " \
            << "pressure gradient = " << ( flowDirection & gradP.value() ) << "      " \
            << "min y+ = " << yplusWall << nl
        
        turbulence.correct()
        
        if runTime.outputTime():
           from Foam.finiteVolume import  volSymmTensorField
           from Foam.OpenFOAM import IOdictionary, IOobject, word, fileName
           R = volSymmTensorField( IOobject( word( "R" ),
                                             fileName( runTime.timeName() ),
                                             mesh,
                                             IOobject.NO_READ,
                                             IOobject.AUTO_WRITE ),
                                   turbulence.R() )
           
           runTime.write()
            
           gFormat = runTime.graphFormat()
           
           from Foam.sampling import makeGraph
            
           makeGraph( y, flowDirection & U, word( "Uf" ), gFormat )
           
           makeGraph( y, laminarTransport.ext_nu(), gFormat )
           
           makeGraph( y, turbulence.ext_k(), gFormat )

           makeGraph( y, turbulence.ext_epsilon(), gFormat )
           
           from Foam.OpenFOAM import tensor
           makeGraph( y, R.component( tensor.XY ), word( "uv" ), gFormat )
           from Foam import fvc
           makeGraph( y, fvc.grad(U).mag(), word( "gammaDot" ), gFormat )

           runTime.write()
           
           pass
        
        ext_Info() << "ExecutionTime = " << runTime.elapsedCpuTime() << " s" << \
              "  ClockTime = " << runTime.elapsedClockTime() << " s" << nl << nl
        
        pass

    ext_Info() << "End\n" << nl 

    import os
    return os.EX_OK


#--------------------------------------------------------------------------------------
import sys, os
from Foam import FOAM_VERSION
if FOAM_VERSION( "==", "010600" ):
   if __name__ == "__main__" :
     argv = sys.argv
     if len( argv ) >1 and argv[ 1 ]=="-test":
        argv = None
        test_dir= os.path.join( os.environ[ "PYFOAM_TESTING_DIR" ],'cases', 'propogated', 'r1.6', 'incompressible', 'boundaryFoam', 'boundaryLaunderSharma' )
        argv = [ __file__, "-case", test_dir ]  
        pass
     os._exit( main_standalone( len( argv ), argv ) )
     pass
else :
   from Foam.OpenFOAM import ext_Info
   ext_Info() << "\n\n To use this solver it is necessary to SWIG OpenFOAM-1.6\n"
   pass

    
#--------------------------------------------------------------------------------------


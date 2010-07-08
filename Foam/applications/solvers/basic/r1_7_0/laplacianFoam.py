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
    from Foam.finiteVolume import volScalarField
        
    ext_Info() << "Reading field T\n" << nl

    T = volScalarField( IOobject( word( "T" ),
                                  fileName( runTime.timeName() ),
                                  mesh,
                                  IOobject.MUST_READ,
                                  IOobject.AUTO_WRITE ),
                        mesh )
    
    ext_Info() << "Reading transportProperties\n" << nl

    transportProperties = IOdictionary( IOobject( word( "transportProperties" ),
                                        fileName( runTime.constant() ),
                                        mesh,
                                        IOobject.MUST_READ,
                                        IOobject.NO_WRITE ) )

    ext_Info() << "Reading diffusivity DT\n" << nl
    from Foam.OpenFOAM import dimensionedScalar
    DT = dimensionedScalar( transportProperties.lookup( word( "DT" ) ) )
        
    return T, transportProperties, DT


#--------------------------------------------------------------------------------------
def write( runTime, mesh, T ):
    if runTime.outputTime():
       from Foam import fvc
       gradT = fvc.grad(T)
       
       from Foam.OpenFOAM import IOdictionary, IOobject, word, fileName
       from Foam.finiteVolume import volScalarField
       from Foam.OpenFOAM import vector
       gradTx = volScalarField( IOobject( word( "gradTx" ), 
                                          fileName( runTime.timeName() ),
                                          mesh,
                                          IOobject.NO_READ,
                                          IOobject.AUTO_WRITE ),
                                          gradT.component( vector.X ) )
       gradTy = volScalarField( IOobject( word( "gradTy" ),
                                          fileName( runTime.timeName() ),
                                          mesh,
                                          IOobject.NO_READ,
                                          IOobject.AUTO_WRITE ),
                                gradT.component( vector.Y ) )

       gradTz = volScalarField( IOobject( word( "gradTz" ),
                                          fileName( runTime.timeName() ),
                                          mesh,
                                          IOobject.NO_READ,
                                          IOobject.AUTO_WRITE ),
                                gradT.component( vector.Z ) )
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
    
    T, transportProperties, DT = _createFields( runTime, mesh )

    from Foam.OpenFOAM import ext_Info, nl
    ext_Info() << "\nCalculating temperature distribution\n" << nl
    
    while runTime.loop() :
        ext_Info() << "Time = " << runTime.timeName() << nl << nl
        
        from Foam.finiteVolume.cfdTools.general.include import readSIMPLEControls
        simple, nNonOrthCorr, momentumPredictor, transonic = readSIMPLEControls( mesh )
        
        from Foam.finiteVolume import solve
        from Foam import fvm
        for nonOrth in range( nNonOrthCorr + 1 ):
            solve( fvm.ddt( T ) - fvm.laplacian( DT, T ) )
            pass
        
        write( runTime, mesh, T )
        
        ext_Info() << "ExecutionTime = " << runTime.elapsedCpuTime() << " s" << \
              "  ClockTime = " << runTime.elapsedClockTime() << " s" << nl << nl
        
        pass

    ext_Info() << "End\n" << nl 

    import os
    return os.EX_OK


#--------------------------------------------------------------------------------------
import sys, os
from Foam import WM_PROJECT_VERSION
if WM_PROJECT_VERSION() >= "1.7.0" :
   if __name__ == "__main__" :
      argv = sys.argv
      if len( argv ) > 1 and argv[ 1 ] == "-test":
         argv = None
         test_dir= os.path.join( os.environ[ "PYFOAM_TESTING_DIR" ],'cases', 'r1.7.0', 'basic', 'laplacianFoam', 'flange' )
         argv = [ __file__, "-case", test_dir ]
         pass
      os._exit( main_standalone( len( argv ), argv ) )
      pass
else:
   from Foam.OpenFOAM import ext_Info
   ext_Info()<< "\nTo use this solver, It is necessary to SWIG OpenFoam1.7.0 or higher \n "
   pass

#--------------------------------------------------------------------------------------


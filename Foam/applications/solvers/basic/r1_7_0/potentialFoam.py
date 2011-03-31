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
        
    ext_Info() << "Reading field p\n" << nl
    p = volScalarField( IOobject( word( "p" ),
                                  fileName( runTime.timeName() ),
                                  mesh,
                                  IOobject.MUST_READ,
                                  IOobject.NO_WRITE ),
                        mesh )
    
    from Foam.OpenFOAM import dimensionedScalar
    p.ext_assign( dimensionedScalar( word( "zero" ), p.dimensions(), 0.0 ) )

    ext_Info() << "Reading field U\n" << nl
    from Foam.finiteVolume import volVectorField
    U = volVectorField( IOobject( word( "U" ),
                                  fileName( runTime.timeName() ),
                                  mesh,
                                  IOobject.MUST_READ,
                                  IOobject.AUTO_WRITE ),
                        mesh )
    from Foam.OpenFOAM import dimensionedVector, vector
    U.ext_assign( dimensionedVector( word( "0" ), U.dimensions(), vector.zero ) )

    from Foam.finiteVolume import surfaceScalarField
    from Foam import fvc
    phi = surfaceScalarField( IOobject( word( "phi" ),
                                        fileName( runTime.timeName() ),
                                        mesh,
                                        IOobject.NO_READ,
                                        IOobject.AUTO_WRITE ),
                              fvc.interpolate( U ) & mesh.Sf() )


    pRefCell = 0
    pRefValue = 0.0
    from Foam.finiteVolume import setRefCell
    pRefCell, pRefValue = setRefCell( p, mesh.solutionDict().subDict( word( "SIMPLE" ) ), pRefCell, pRefValue )

    return p, U, phi, pRefCell, pRefValue


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

    from Foam.OpenFOAM import argList, word
    argList.validOptions.fget().insert( word( "writep" ), "" )
    
    from Foam.OpenFOAM.include import setRootCase
    args = setRootCase( argc, argv )

    from Foam.OpenFOAM.include import createTime
    runTime = createTime( args )

    from Foam.OpenFOAM.include import createMesh
    mesh = createMesh( runTime )
    
    p, U, phi, pRefCell, pRefValue = _createFields( runTime, mesh )

    from Foam.OpenFOAM import ext_Info, nl
    ext_Info() << nl << "Calculating potential flow" << nl
        
    from Foam.finiteVolume.cfdTools.general.include import readSIMPLEControls
    simple, nNonOrthCorr, momentumPredictor, transonic = readSIMPLEControls( mesh )
    
    from Foam.finiteVolume import adjustPhi
    adjustPhi(phi, U, p)
    
    from Foam.OpenFOAM import dimensionedScalar, word, dimTime, dimensionSet
    from Foam import fvc, fvm
    for nonOrth in range( nNonOrthCorr + 1):
        pEqn = fvm.laplacian( dimensionedScalar( word( "1" ), dimTime / p.dimensions() * dimensionSet( 0.0, 2.0, -2.0, 0.0, 0.0 ), 1.0 ), p ) == fvc.div( phi )
        
        pEqn.setReference( pRefCell, pRefValue )
        pEqn.solve()

        if nonOrth == nNonOrthCorr:
           phi.ext_assign( phi - pEqn.flux() )
           pass
        pass
    
    ext_Info() << "continuity error = " << fvc.div( phi ).mag().weightedAverage( mesh.V() ).value() << nl

    U.ext_assign( fvc.reconstruct( phi ) )
    U.correctBoundaryConditions()
    ext_Info() << "Interpolated U error = " << ( ( ( fvc.interpolate( U ) & mesh.Sf() ) - phi ).sqr().sum().sqrt()  /mesh.magSf().sum() ).value() << nl

    # Force the write
    U.write()
    phi.write()
    
    if args.optionFound( word( "writep" ) ):
       p.write()
       pass
       
    ext_Info() << "ExecutionTime = " << runTime.elapsedCpuTime() << " s" << \
              "  ClockTime = " << runTime.elapsedClockTime() << " s" << nl << nl
        
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
         test_dir= os.path.join( os.environ[ "PYFOAM_TESTING_DIR" ],'cases', 'propogated', 'r1.6', 'basic', 'potentialFoam', 'cylinder' )
         argv = [ __file__, "-case", test_dir ]
         pass
      os._exit( main_standalone( len( argv ), argv ) )
else:
   from Foam.OpenFOAM import ext_Info
   ext_Info()<< "\nTo use this solver, It is necessary to SWIG OpenFoam1.7.0 or higher\n "
   pass



#--------------------------------------------------------------------------------------


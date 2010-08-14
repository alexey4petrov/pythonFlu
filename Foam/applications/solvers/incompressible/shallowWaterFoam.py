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
def readGravitationalAcceleration( runTime, mesh ):
    from Foam.OpenFOAM import IOdictionary, word, fileName, IOobject
    from Foam.OpenFOAM import ext_Info, nl
    ext_Info() << "\nReading gravitationalProperties" << nl
    
    gravitationalProperties = IOdictionary( IOobject( word( "gravitationalProperties" ),
                                            fileName( runTime.constant() ),
                                            mesh,
                                            IOobject.MUST_READ,
                                            IOobject.NO_WRITE ) )
    
    from Foam.OpenFOAM import dimensionedVector,Switch, dimTime
    g = dimensionedVector( gravitationalProperties.lookup( word( "g" ) ) )
    rotating = Switch( gravitationalProperties.lookup( word( "rotating" ) ) )
    
    if rotating:
       Omega = dimensionedVector( gravitationalProperties.lookup( word( "Omega" ) ) )
    else:
       Omega = dimensionedVector( word( "Omega" ), -dimTime, vector( 0,0,0 ) )
    
    magg = g.mag()
    gHat = g / magg
    
    return gravitationalProperties, g, rotating, Omega, magg, gHat


#----------------------------------------------------------------------------
def createPhi( runTime, hU, mesh ):
    from Foam.OpenFOAM import ext_Info, nl
    from Foam.OpenFOAM import IOdictionary, IOobject, word, fileName
    from Foam.finiteVolume import surfaceScalarField
    ext_Info() << "Reading/calculating face flux field phi\n" << nl
    
    from Foam.finiteVolume import linearInterpolate
    phi = surfaceScalarField( IOobject( word( "phi" ),
                                        fileName( runTime.timeName() ),
                                        mesh,
                                        IOobject.READ_IF_PRESENT,
                                        IOobject.AUTO_WRITE ),
                              linearInterpolate( hU ) & mesh.Sf() )
    return phi
    

#----------------------------------------------------------------------------
def _createFields( runTime, mesh, Omega, gHat ):
    from Foam.OpenFOAM import ext_Info, nl
    from Foam.OpenFOAM import IOdictionary, IOobject, word, fileName
    from Foam.finiteVolume import volScalarField
    
    ext_Info() << "Reading field h\n" << nl
    h = volScalarField( IOobject( word( "h" ),
                                    fileName( runTime.timeName() ),
                                    mesh,
                                    IOobject.MUST_READ,
                                    IOobject.AUTO_WRITE ),
                        mesh )
    from Foam.OpenFOAM import dimLength, dimensionedScalar
    ext_Info() << "Reading field h0 if present\n" << nl
    h0 = volScalarField( IOobject( word( "h0" ),
                                   fileName( runTime.findInstance( fileName( word( "polyMesh" ) ), word( "points" ) ) ) ,
                                   mesh,
                                   IOobject.READ_IF_PRESENT ),
                         mesh,
                         dimensionedScalar( word( "h0" ), dimLength, 0.0 ) )
    
    from Foam.finiteVolume import volVectorField
    ext_Info() << "Reading field U\n" << nl
    U = volVectorField( IOobject( word( "U" ),
                                  fileName( runTime.timeName() ),
                                  mesh,
                                  IOobject.MUST_READ,
                                  IOobject.AUTO_WRITE ),
                        mesh )
    
    ext_Info() << "Creating field hU\n" << nl
    hU = volVectorField( IOobject( word( "hU" ),
                                   fileName( runTime.timeName() ),
                                   mesh ),
                         h * U,
                         U.ext_boundaryField().types() )
    
    ext_Info() << "Creating field hTotal for post processing\n" << nl
    hTotal = volScalarField( IOobject( word( "hTotal" ),
                                       fileName( runTime.timeName() ),
                                       mesh, 
                                       IOobject.READ_IF_PRESENT,
                                       IOobject.AUTO_WRITE ),
                             h + h0 )
                             
    hTotal.write()
    
    phi = createPhi( runTime, hU, mesh )
    
    ext_Info() << "Creating Coriolis Force" << nl
    from Foam.OpenFOAM import dimensionedVector
    F = dimensionedVector( word( "F" ), ( ( 2.0 * Omega ) & gHat ) * gHat )
    
    return h, h0, U, hU, hTotal, phi, F


#--------------------------------------------------------------------------------------
def CourantNo( runTime, mesh, h, phi, magg ):
    CoNum = 0.0
    meanCoNum = 0.0
    waveCoNum = 0.0
    
    
    if mesh.nInternalFaces():
       from Foam import fvc
       SfUfbyDelta = mesh.deltaCoeffs() * phi.mag() / fvc.interpolate(h)
       
       CoNum = ( SfUfbyDelta / mesh.magSf() ).ext_max().value() * runTime.deltaT().value()
       
       meanCoNum = ( SfUfbyDelta.sum() / mesh.magSf().sum() ).value() * runTime.deltaT().value()

       # Gravity wave Courant number
       waveCoNum = 0.5 * ( mesh.deltaCoeffs() * fvc.interpolate( h ).sqrt() ).ext_max().value() * magg.sqrt().value() * runTime.deltaT().value()
    
    from Foam.OpenFOAM import ext_Info, nl
    ext_Info() << "Courant number mean: " << meanCoNum  << " max: " << CoNum << nl
    ext_Info() << "Gravity wave Courant number max: " << waveCoNum  << nl
    
    return CoNum, meanCoNum, waveCoNum
    

#--------------------------------------------------------------------------------------
def main_standalone( argc, argv ):

    from Foam.OpenFOAM.include import setRootCase
    args = setRootCase( argc, argv )

    from Foam.OpenFOAM.include import createTime
    runTime = createTime( args )

    from Foam.OpenFOAM.include import createMesh
    mesh = createMesh( runTime )
    
    gravitationalProperties, g, rotating, Omega, magg, gHat = readGravitationalAcceleration( runTime, mesh )

    h, h0, U, hU, hTotal, phi, F = _createFields( runTime, mesh, Omega, gHat )

    from Foam.OpenFOAM import ext_Info, nl
    ext_Info() << "\nStarting time loop\n" << nl 
    
    while runTime.loop() :
        ext_Info() << "\nTime = " << runTime.timeName() << nl << nl
        
        from Foam.finiteVolume.cfdTools.general.include import readPISOControls
        piso, nCorr, nNonOrthCorr, momentumPredictor, transonic, nOuterCorr = readPISOControls( mesh ) 
        
        CoNum, meanCoNum, waveCoNum = CourantNo( runTime, mesh, h, phi, magg )
        
        for ucorr in range( nOuterCorr ):
           from Foam.finiteVolume import surfaceScalarField
           from Foam import fvc
           from Foam.OpenFOAM import word
           
           phiv = surfaceScalarField( word( "phiv" ), phi / fvc.interpolate( h ) )
           
           from Foam import fvm
           hUEqn = fvm.ddt( hU ) + fvm.div( phiv, hU ) 
           
           hUEqn.relax()
           
           if momentumPredictor:
              from Foam.finiteVolume import solve
              from Foam import fvc
              if rotating:
                  solve( hUEqn + ( F ^ hU ) == -magg * h * fvc.grad( h + h0 ) )
                  pass
              else:
                  solve( hUEqn == -magg * h * fvc.grad( h + h0 ) ) 
                  pass
              
              # Constrain the momentum to be in the geometry if 3D geometry
              if mesh.nGeometricD() == 3 :
                 hU.ext_assign( hU - ( gHat & hU ) * gHat )
                 hU.correctBoundaryConditions();
                 pass
           
           for corr in range( nCorr ): 
               hf = fvc.interpolate( h )
               rUA = 1.0 / hUEqn.A()
               ghrUAf = magg * fvc.interpolate( h * rUA )
               
               phih0 = ghrUAf * mesh.magSf() * fvc.snGrad( h0 )
               if rotating:
                  hU.ext_assign( rUA * ( hUEqn .H() - ( F ^ hU ) ) )
                  pass
               else:
                  hU = rUA * hUEqn.H()
                  pass
               
               phi.ext_assign( ( fvc.interpolate( hU ) & mesh.Sf() ) + fvc.ddtPhiCorr( rUA, h, hU, phi )- phih0 )
               
               for nonOrth in range(nNonOrthCorr + 1):
                   hEqn = fvm.ddt( h ) + fvc.div( phi ) - fvm.laplacian( ghrUAf, h )
                   
                   if ucorr < nOuterCorr-1 or corr < nCorr-1 :
                      hEqn.solve()
                      pass
                   else:
                      hEqn.solve( mesh.solver( word( str( h.name() ) + "Final" ) ) )
                      pass
                   if nonOrth == nNonOrthCorr:
                      phi.ext_assign( phi + hEqn.flux() )
                   pass
               
               hU.ext_assign( hU - rUA * h * magg * fvc.grad( h + h0 ) )
               
               #Constrain the momentum to be in the geometry if 3D geometry
               if mesh.nGeometricD() == 3:
                  hU.ext_assign( hU - ( gHat & hU ) * gHat )
                  pass
               
               hU.correctBoundaryConditions()
               pass
           pass
        
        U == hU / h
        hTotal == h + h0

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
if FOAM_VERSION( "<", "010600" ):
   from Foam.OpenFOAM import ext_Info
   ext_Info() << "\n\n To use this solver it is necessary to SWIG OpenFOAM-1.6 or higher\n"
   pass


#--------------------------------------------------------------------------------------
if FOAM_VERSION( ">=", "010600" ):
   if __name__ == "__main__" :
     argv = sys.argv
     if len( argv ) >1 and argv[ 1 ]=="-test":
        argv = None
        test_dir= os.path.join( os.environ[ "PYFOAM_TESTING_DIR" ],'cases', 'propogated', 'r1.6', 'incompressible', 'shallowWaterFoam', 'squareBump' )
        argv = [ __file__, "-case", test_dir ]
        pass
     os._exit( main_standalone( len( argv ), argv ) )
     pass
   pass

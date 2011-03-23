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
def readTransportProperties( runTime, mesh):
    from Foam.OpenFOAM import ext_Info, nl
    from Foam.OpenFOAM import IOdictionary, IOobject, word, fileName
    ext_Info() << "\nReading transportProperties\n" << nl
    
    transportProperties = IOdictionary( IOobject( word( "transportProperties" ),
                                                  fileName( runTime.constant() ),
                                                  mesh,
                                                  IOobject.MUST_READ,
                                                  IOobject.NO_WRITE,
                                                  False ) )
    
    from Foam.OpenFOAM import dimensionedScalar, dimensionedVector
    nu = dimensionedScalar( transportProperties.lookup( word( "nu" ) ) )
    
    #  Read centerline velocity for channel simulations
    Ubar = dimensionedVector( transportProperties.lookup( word( "Ubar" ) ) )

    magUbar = Ubar.mag()
    from Foam.OpenFOAM import vector
    flowDirection = ( Ubar / magUbar ).ext_value()
    
    return transportProperties, nu, Ubar, magUbar, flowDirection


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
                                  IOobject.AUTO_WRITE ),
                        mesh )

    ext_Info() << "Reading field U\n" << nl
    from Foam.finiteVolume import volVectorField
    U = volVectorField( IOobject( word( "U" ),
                                  fileName( runTime.timeName() ),
                                  mesh,
                                  IOobject.MUST_READ,
                                  IOobject.AUTO_WRITE ),
                        mesh )
    
    from Foam.finiteVolume.cfdTools.incompressible import createPhi
    phi = createPhi( runTime, mesh, U )
    
    pRefCell = 0
    pRefValue = 0.0
    
    from Foam.finiteVolume import setRefCell
    pRefCell, pRefValue = setRefCell( p, mesh.solutionDict().subDict( word( "PISO" ) ), pRefCell, pRefValue )

    from Foam.transportModels import singlePhaseTransportModel
    laminarTransport = singlePhaseTransportModel( U, phi )
    
    from Foam import incompressible
    sgsModel = incompressible.LESModel.New( U, phi, laminarTransport )
        
    return p, U, phi, laminarTransport, sgsModel, pRefCell, pRefValue


#--------------------------------------------------------------------------------------
def createGradP( runTime ):
    from Foam.OpenFOAM import dimensionedScalar, dimensionSet, IFstream, word
    gradP = dimensionedScalar( word( "gradP" ),
                               dimensionSet( 0.0, 1.0, -2.0, 0.0, 0.0 ),
                               0.0 )
    from Foam.OpenFOAM import word, fileName, ext_Info, nl
    gradPFile = IFstream( runTime.path()/fileName( runTime.timeName() )/fileName( "uniform" )/ fileName( "gradP.raw" ) )
    
    if gradPFile.good():
       gradPFile >> gradP
       ext_Info() << "Reading average pressure gradient" << nl << nl
       pass
    else:
       ext_Info() << "Initializing with 0 pressure gradient" << nl << nl
       pass
    
    return gradP, gradPFile


#-------------------------------------------------------------------------------------
def writeGradP( runTime, gradP ):
    if runTime.outputTime():
       from Foam.OpenFOAM import OFstream, fileName
       gradPFile = OFstream( runTime.path()/fileName( runTime.timeName() )/fileName( "uniform" )/fileName( "gradP.raw" ) )
       
       from Foam.OpenFOAM import nl, ext_Info
       if gradPFile.good():
          gradPFile << gradP << nl
          pass
       else:
          ext_Info() << "Cannot open file " << runTime.path()/fileName( runTime.timeName() )/fileName( "uniform" )/fileName( "gradP.raw" )
          import os
          os.abort()

#--------------------------------------------------------------------------------------
def main_standalone( argc, argv ):

    from Foam.OpenFOAM.include import setRootCase
    args = setRootCase( argc, argv )

    from Foam.OpenFOAM.include import createTime
    runTime = createTime( args )

    from Foam.OpenFOAM.include import createMesh
    mesh = createMesh( runTime )
    
    transportProperties, nu, Ubar, magUbar, flowDirection = readTransportProperties( runTime, mesh)
    
    p, U, phi, laminarTransport, sgsModel, pRefCell, pRefValue = _createFields( runTime, mesh )
    
    from Foam.finiteVolume.cfdTools.general.include import initContinuityErrs
    cumulativeContErr = initContinuityErrs()
    
    gradP, gradPFile = createGradP( runTime)
    
    from Foam.OpenFOAM import ext_Info, nl
    ext_Info() << "\nStarting time loop\n" << nl 

    while runTime.loop() :
        ext_Info() << "Time = " << runTime.timeName() << nl << nl

        from Foam.finiteVolume.cfdTools.general.include import readPISOControls
        piso, nCorr, nNonOrthCorr, momentumPredictor, transonic, nOuterCorr = readPISOControls( mesh ) 

        from Foam.finiteVolume.cfdTools.incompressible import CourantNo
        CoNum, meanCoNum = CourantNo( mesh, phi, runTime )

        sgsModel.correct()

        from Foam import fvm
        UEqn = fvm.ddt( U ) + fvm.div( phi, U ) + sgsModel.divDevBeff( U ) == flowDirection * gradP

        if momentumPredictor:
           from Foam.finiteVolume import solve
           from Foam import fvc
           solve( UEqn == -fvc.grad( p ) )
           pass

        rUA = 1.0 / UEqn.A()

        for corr in range( nCorr ):
            U.ext_assign( rUA * UEqn.H() )
            from Foam import fvc
            phi.ext_assign( ( fvc.interpolate( U ) & mesh.Sf() ) + fvc.ddtPhiCorr( rUA, U, phi ) )

            from Foam.finiteVolume import adjustPhi
            adjustPhi(phi, U, p)

            from Foam.OpenFOAM import word

            for nonOrth in range( nNonOrthCorr + 1 ):
                pEqn = fvm.laplacian( rUA, p ) == fvc.div( phi ) 
                pEqn.setReference( pRefCell, pRefValue )

                if corr == nCorr-1 and nonOrth == nNonOrthCorr:
                   pEqn.solve( mesh.solver( word( str( p.name() ) + "Final" ) ) )
                   pass
                else:
                   pEqn.solve( mesh.solver( p.name() ) )
                   pass

                if nonOrth == nNonOrthCorr:
                   phi.ext_assign( phi - pEqn.flux() )
                   pass
                pass

            from Foam.finiteVolume.cfdTools.incompressible import continuityErrs
            cumulativeContErr = continuityErrs( mesh, phi, runTime, cumulativeContErr )

            U.ext_assign( U - rUA * fvc.grad( p ) )
            U.correctBoundaryConditions()
            pass

        # Correct driving force for a constant mass flow rate

        # Extract the velocity in the flow direction
        magUbarStar = ( flowDirection & U ).weightedAverage( mesh.V() )

        # Calculate the pressure gradient increment needed to
        # adjust the average flow-rate to the correct value
        gragPplus = ( magUbar - magUbarStar ) / rUA.weightedAverage( mesh.V() )

        U.ext_assign( U + flowDirection * rUA * gragPplus )

        gradP +=gragPplus
        ext_Info() << "Uncorrected Ubar = " << magUbarStar.value() << " " << "pressure gradient = " << gradP.value() << nl

        runTime.write()

        writeGradP( runTime, gradP )

        ext_Info() << "ExecutionTime = " << runTime.elapsedCpuTime() << " s" << \
              "  ClockTime = " << runTime.elapsedClockTime() << " s" << nl << nl

        pass

    ext_Info() << "End\n" << nl 

    import os
    return os.EX_OK


#--------------------------------------------------------------------------------------
import sys, os
from Foam import FOAM_REF_VERSION
if FOAM_REF_VERSION( ">=", "010600" ):
   if __name__ == "__main__" :
     argv = sys.argv
     if len( argv ) >1 and argv[ 1 ]=="-test":
        argv = None
        test_dir= os.path.join( os.environ[ "PYFOAM_TESTING_DIR" ],'cases', 'propogated', 'r1.6', 'incompressible', 'channelFoam', 'channel395' )
        argv = [ __file__, "-case", test_dir ]  
        pass
     os._exit( main_standalone( len( argv ), argv ) )
     pass
else:
   from Foam.OpenFOAM import ext_Info
   ext_Info() << "\n\n To use this solver it is necessary to SWIG OpenFOAM-1.6 or higher\n"
   pass 
   
     
#--------------------------------------------------------------------------------------


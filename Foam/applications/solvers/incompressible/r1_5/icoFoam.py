#!/usr/bin/env python

#---------------------------------------------------------------------------
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
class solver( object ):
    def __init__( self, getTime, getMesh, getFields ):
        self.runTime = getTime()
        
        self.mesh = getMesh( self.runTime )
        
        self.transportProperties, self.nu, self.p, self.U, self.phi, self.pRefCell, self.pRefValue = getFields( self.runTime, self.mesh )
                                          
        from Foam.finiteVolume.cfdTools.general.include import initContinuityErrs
        self.cumulativeContErr = initContinuityErrs()
        
        self.runTime += self.runTime.deltaT()
        pass

    def step( self, getPISOControls ):
        from Foam.OpenFOAM import ext_Info, nl
        ext_Info() << "Time = " << self.runTime.timeName() << nl << nl
        
        piso, nCorr, nNonOrthCorr, momentumPredictor, transSonic, nOuterCorr = getPISOControls( self.mesh )

        from Foam.finiteVolume.cfdTools.incompressible import CourantNo
        CoNum, meanCoNum = CourantNo( self.mesh, self.phi, self.runTime )

        from Foam import fvm
        UEqn = ( fvm.ddt( self.U ) + fvm.div( self.phi, self.U ) - fvm.laplacian( self.nu, self.U ) )

        from Foam import fvc
        from Foam.finiteVolume import solve
        solve( UEqn == -fvc.grad( self.p ) )

        # --- PISO loop

        for corr in range( nCorr ) :
            rUA = 1.0 / UEqn.A()

            self.U.ext_assign( rUA * UEqn.H() )
            self.phi.ext_assign( ( fvc.interpolate( self.U ) & self.mesh.Sf() ) + fvc.ddtPhiCorr( rUA, self.U, self.phi ) )

            from Foam.finiteVolume import adjustPhi
            adjustPhi( self.phi, self.U, self.p )

            for nonOrth in range( nNonOrthCorr + 1 ) :
                pEqn = ( fvm.laplacian( rUA, self.p ) == fvc.div( self.phi ) )
                
                pEqn.setReference( self.pRefCell, self.pRefValue )
                pEqn.solve()

                if nonOrth == nNonOrthCorr:
                    self.phi.ext_assign( self.phi - pEqn.flux() )
                    pass
                
                pass
                        
            from Foam.finiteVolume.cfdTools.incompressible import continuityErrs
            cumulativeContErr = continuityErrs( self.mesh, self.phi, self.runTime, self.cumulativeContErr )

            self.U.ext_assign( self.U - rUA * fvc.grad( self.p ) )
            self.U.correctBoundaryConditions();

            pass

        self.runTime.write()
        
        ext_Info() << "ExecutionTime = " << self.runTime.elapsedCpuTime() << " s" << \
              "  ClockTime = " << self.runTime.elapsedClockTime() << " s" << nl << nl

        self.runTime += self.runTime.deltaT()
        
        return self.runTime.value()

    def run( self, getPISOControls ):
        from Foam.OpenFOAM import ext_Info, nl
        ext_Info() << "\nStarting time loop\n" << nl
        
        while not self.runTime.end() :
            self.step( getPISOControls )
            pass

        from Foam.OpenFOAM import ext_Info, nl
        ext_Info() << "End\n"

        return True
    
    pass


#---------------------------------------------------------------------------
def createFields( runTime, mesh ):
    from Foam.OpenFOAM import ext_Info, nl
    ext_Info() << "Reading transportProperties\n"

    from Foam.OpenFOAM import IOdictionary, IOobject, word, fileName
    transportProperties = IOdictionary( IOobject( word( "transportProperties" ),
                                                  fileName( runTime.constant() ),
                                                  mesh,
                                                  IOobject.MUST_READ,
                                                  IOobject.NO_WRITE ) )

    from Foam.OpenFOAM import dimensionedScalar
    nu = dimensionedScalar( transportProperties.lookup( word( "nu" ) ) );

    ext_Info() << "Reading field p\n" << nl
    from Foam.finiteVolume import volScalarField
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
    setRefCell( p, mesh.solutionDict().subDict( word( "PISO" ) ), pRefCell, pRefValue )

    return transportProperties, nu, p, U, phi, pRefCell, pRefValue

    
#--------------------------------------------------------------------------------------
def main_embedded( argc, argv ):
    from Foam.OpenFOAM.include import setRootCase
    args = setRootCase( argc, argv )

    from Foam.OpenFOAM.include import createTime
    getTime = lambda : createTime( args )

    from Foam.OpenFOAM.include import createMesh

    from Foam.finiteVolume.cfdTools.general.include import readPISOControls

    import os
    if solver( getTime, createMesh, createFields ).run( readPISOControls ) :
        return os.EX_OK

    return os.EX_USAGE


#--------------------------------------------------------------------------------------
def main_standalone( argc, argv ):

    from Foam.OpenFOAM.include import setRootCase
    args = setRootCase( argc, argv )

    from Foam.OpenFOAM.include import createTime
    runTime = createTime( args )

    from Foam.OpenFOAM.include import createMesh
    mesh = createMesh( runTime )

    transportProperties, nu, p, U, phi, pRefCell, pRefValue = createFields( runTime, mesh )

    from Foam.finiteVolume.cfdTools.general.include import initContinuityErrs
    cumulativeContErr = initContinuityErrs()
    
    from Foam.OpenFOAM import ext_Info, nl
    ext_Info() << "\nStarting time loop\n"

    runTime += runTime.deltaT()
    while not runTime.end() :
        ext_Info() << "Time = " <<  runTime.timeName() << nl << nl

        from Foam.finiteVolume.cfdTools.general.include import readPISOControls
        piso, nCorr, nNonOrthCorr, momentumPredictor, transonic, nOuterCorr, ddtPhiCorr = readPISOControls( mesh )

        from Foam.finiteVolume.cfdTools.incompressible import CourantNo
        CoNum, meanCoNum = CourantNo( mesh, phi, runTime )

        from Foam import fvm
        UEqn = ( fvm.ddt( U ) + fvm.div( phi, U ) - fvm.laplacian( nu, U ) )

        from Foam import fvc
        from Foam.finiteVolume import solve
        solve( UEqn == -fvc.grad( p ) )

        # --- PISO loop

        for corr in range( nCorr ) :
            rUA = 1.0 / UEqn.A()

            U.ext_assign( rUA * UEqn.H() )
            phi.ext_assign( ( fvc.interpolate( U ) & mesh.Sf() ) + fvc.ddtPhiCorr( rUA, U, phi ) )

            from Foam.finiteVolume import adjustPhi
            adjustPhi( phi, U, p )

            for nonOrth in range( nNonOrthCorr + 1 ) :
                pEqn = ( fvm.laplacian( rUA, p ) == fvc.div( phi ) )

                pEqn.setReference( pRefCell, pRefValue )
                pEqn.solve()

                if nonOrth == nNonOrthCorr:
                    phi.ext_assign( phi - pEqn.flux() )
                    pass
                
                pass
            
            from Foam.finiteVolume.cfdTools.incompressible import continuityErrs
            cumulativeContErr = continuityErrs( mesh, phi, runTime, cumulativeContErr )

            U.ext_assign( U - rUA * fvc.grad( p ) )
            U.correctBoundaryConditions();

            pass

        runTime.write()
        
        ext_Info() << "ExecutionTime = " << runTime.elapsedCpuTime() << " s" << \
                      "  ClockTime = " << runTime.elapsedClockTime() << " s" << nl << nl

        runTime += runTime.deltaT()
        pass

    ext_Info() << "End\n"

    import os
    return os.EX_OK

    
#--------------------------------------------------------------------------------------
from Foam import WM_PROJECT_VERSION
import os,sys
if WM_PROJECT_VERSION() == "1.5" :
   if __name__ == "__main__" :
      argv = sys.argv
      if len( argv ) > 1 and argv[ 1 ] == "-test":
         argv = None
         test_dir= os.path.join( os.environ[ "PYFOAM_TESTING_DIR" ],'cases', 'r1.5', 'incompressible', 'icoFoam', 'cavity' )
         argv = [ __file__, "-case", test_dir ]
         pass
      os._exit( main_standalone( len( argv ), argv ) )
      pass
   pass
else:
   from Foam.OpenFOAM import ext_Info
   ext_Info()<< "\nTo use this solver, It is necessary to SWIG OpenFoam1.5 \n "     

    
#--------------------------------------------------------------------------------------


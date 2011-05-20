## pythonFlu - Python wrapping for OpenFOAM C++ API
## Copyright (C) 2010- Alexey Petrov
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
## See http://sourceforge.net/projects/pythonflu
##
## Author : Alexey PETROV
##


#---------------------------------------------------------------------------
def createPhi( runTime, mesh, U ):
    print "Reading/calculating face flux field phi\n"

    from Foam.OpenFOAM import Time
    from Foam.OpenFOAM import word
    from Foam.OpenFOAM import fileName
    from Foam.OpenFOAM import IOobject
    
    from Foam.finiteVolume import fvMesh
    from Foam.finiteVolume import volScalarField
    from Foam.finiteVolume import surfaceScalarField
    from Foam.finiteVolume import linearInterpolate

    phi = surfaceScalarField( IOobject( word( "phi" ),
                                        fileName( runTime.timeName() ),
                                        mesh,
                                        IOobject.READ_IF_PRESENT,
                                        IOobject.AUTO_WRITE ),
                              linearInterpolate( U ) & mesh.Sf() )
    return phi


#---------------------------------------------------------------------------
def CourantNo( mesh, phi, runTime ):
    from Foam import get_proper_function
    fun = get_proper_function( "Foam.finiteVolume.cfdTools.general.include.CourantNo_impl",
                               "CourantNo" )
    return fun( mesh, phi, runTime )


#---------------------------------------------------------------------------
def continuityErrs( mesh, phi, runTime, cumulativeContErr ):
    from Foam.OpenFOAM import Time
    from Foam.finiteVolume import fvMesh
    from Foam.finiteVolume import surfaceScalarField

    from Foam import fvm, fvc

    contErr = fvc.div( phi )
    sumLocalContErr = runTime.deltaT().value() * contErr.mag().weightedAverage( mesh.V() ).value()
    globalContErr = runTime.deltaT().value() * contErr.weightedAverage( mesh.V() ).value()
    cumulativeContErr += globalContErr

    from Foam.OpenFOAM import ext_Info, nl
    ext_Info() << "time step continuity errors : sum local = " << sumLocalContErr \
               << ", global = " << globalContErr \
               << ", cumulative = " << cumulativeContErr << nl
               
    return cumulativeContErr


#---------------------------------------------------------------------------



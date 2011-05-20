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
def compressibleCreatePhi( runTime, mesh, rho, U ):
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
                              linearInterpolate( rho * U ) & mesh.Sf() )
    
    return phi


#---------------------------------------------------------------------------
def compressibleCourantNo( mesh, phi, rho, runTime ):
    from Foam import get_proper_function
    fun = get_proper_function( "Foam.finiteVolume.cfdTools.compressible.compressibleCourantNo_impl",
                               "compressibleCourantNo" )
    
    return fun( mesh, phi, rho, runTime )
    

#---------------------------------------------------------------------------
def compressibleContinuityErrs( rho, thermo, cumulativeContErr ):
    from Foam import fvc
    totalMass = fvc.domainIntegrate( rho )

    sumLocalContErr = ( fvc.domainIntegrate( ( rho - thermo.rho() ).mag() ) / totalMass ).value()

    globalContErr = ( fvc.domainIntegrate( rho - thermo.rho() ) / totalMass ).value()

    cumulativeContErr += globalContErr

    from Foam.OpenFOAM import ext_Info, nl
    ext_Info() << "time step continuity errors : sum local = " << sumLocalContErr\
               << ", global = " << globalContErr \
               << ", cumulative = " << cumulativeContErr << nl

    return cumulativeContErr


#---------------------------------------------------------------------------
def rhoEqn( rho, phi ):
    from Foam import fvm, fvc
    from Foam.finiteVolume import solve
    solve( fvm.ddt( rho ) + fvc.div( phi ) )

    pass


#---------------------------------------------------------------------------
    

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
## Author : Alexey PETROV, Andrey SIMURZIN
##


#--------------------------------------------------------------------------
from Foam.ext.common.managedFlu.Deps import *

#--------------------------------------------------------------------------
from Foam.OpenFOAM import TimeHolder as Time
from Foam.OpenFOAM import IOobjectHolder as IOobject
from Foam.OpenFOAM import dictionaryHolder as dictionary
from Foam.OpenFOAM import IOdictionaryHolder as IOdictionary
	
#---------------------------------------------------------------------------
from Foam.finiteVolume import GeometricFieldHolder_scalar_fvPatchField_volMesh as volScalarField
from Foam.finiteVolume import GeometricFieldHolder_vector_fvPatchField_volMesh as volVectorField
from Foam.finiteVolume import GeometricFieldHolder_scalar_fvsPatchField_surfaceMesh as surfaceScalarField
from Foam.finiteVolume import GeometricFieldHolder_vector_fvsPatchField_surfaceMesh as surfaceVectorField

from Foam.finiteVolume import fvScalarMatrixHolder as fvScalarMatrix
from Foam.finiteVolume import fvVectorMatrixHolder as fvVectorMatrix

from Foam.finiteVolume import simpleControlHolder as simpleControl

from Foam.ext.common.finiteVolume.managedFlu.linear import linearInterpolate


#---------------------------------------------------------------------------
from Foam.man import fvc
from Foam.man import fvm


#---------------------------------------------------------------------------
from Foam.transportModels import singlePhaseTransportModelHolder as singlePhaseTransportModel


#---------------------------------------------------------------------------
from Foam.thermophysicalModels import basicPsiThermoHolder as basicPsiThermo
from Foam.thermophysicalModels import basicThermoHolder as basicThermo


#---------------------------------------------------------------------------
from Foam.man import compressible
from Foam.man import incompressible


#---------------------------------------------------------------------------
from Foam.man import radiation


#---------------------------------------------------------------------------
def createPhi( runTime, mesh, U ):
    from Foam.OpenFOAM import ext_Info, nl
    ext_Info() << "Reading/calculating face flux field phi\n" << nl;

    from Foam.OpenFOAM import fileName, word
    from Foam.OpenFOAM import IOobject as ref_IOobject
    phi = surfaceScalarField( IOobject( word( "phi" ),
                                        fileName( runTime.timeName() ),
                                        mesh,
                                        ref_IOobject.READ_IF_PRESENT,
                                        ref_IOobject.AUTO_WRITE ),
                              linearInterpolate(U) & surfaceVectorField( mesh.Sf(), Deps( mesh ) ) ) 
    
    return phi


#---------------------------------------------------------------------------
def compressibleCreatePhi( runTime, mesh, U, rho ):
     from Foam.OpenFOAM import ext_Info, nl
     ext_Info() << "Reading/calculating face flux field phi\n" << nl
     from Foam.OpenFOAM import fileName, word
     from Foam.OpenFOAM import IOobject as ref_IOobject
     from Foam.managedFlu import Deps

     phi = surfaceScalarField( IOobject( word( "phi" ),
                                         fileName( runTime.timeName() ),
                                         mesh,
                                         ref_IOobject.READ_IF_PRESENT,
                                         ref_IOobject.AUTO_WRITE ),
                               linearInterpolate( rho * U ) & surfaceVectorField( mesh.Sf(), Deps( mesh ) ) ) 
     
     return phi


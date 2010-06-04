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
from Foam import get_module_initializtion_command
exec get_module_initializtion_command( "dynamicFvMesh_" ) 


#---------------------------------------------------------------------------
dynamicFvMesh.defaultRegion = dynamicFvMesh.defaultRegion.fget()

dynamicFvMesh.meshSubDir = dynamicFvMesh.meshSubDir.fget()


#---------------------------------------------------------------------------
def createDynamicFvMesh( runTime ):
    from Foam.OpenFOAM import ext_Info, nl, IOobject, fileName
    ext_Info() << "Create mesh for time = " << runTime.timeName() << nl << nl

    mesh = dynamicFvMesh.New( IOobject( dynamicFvMesh.defaultRegion,
                                        fileName( runTime.timeName() ),
                                        runTime ) ) 

    return mesh


#------------------------------------------------------------------------------
def meshCourantNo( runTime, mesh, phi ):
    meshCoNum = 0.0
    meanMeshCoNum = 0.0
    
    if mesh.nInternalFaces():
       SfUfbyDelta = mesh.deltaCoeffs() * mesh.phi().mag()
       meshCoNum = (SfUfbyDelta/mesh.magSf()).ext_max().value() * runTime.deltaT().value()
       meanMeshCoNum = ( SfUfbyDelta.sum() / mesh.magSf().sum() ).value() * runTime.deltaT().value()
       pass
    
    from Foam.OpenFOAM import ext_Info, nl
    ext_Info() << "Mesh Courant Number mean: " << meanMeshCoNum << " max: " << meshCoNum << nl << nl
    
    return meshCoNum, meanMeshCoNum
#----------------------------------------------------------------------------


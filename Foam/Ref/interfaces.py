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


#--------------------------------------------------------------------------------------
from Foam.helper import TLoadHelper

attr2interface={}


#--------------------------------------------------------------------------------------
from Foam.Ref import OpenFOAM_interfaces
attr2interface.update( OpenFOAM_interfaces.attr2interface )

from Foam.Ref import meshTools_interfaces
attr2interface.update( meshTools_interfaces.attr2interface )

from Foam.Ref import finiteVolume_interfaces
attr2interface.update( finiteVolume_interfaces.attr2interface )

from Foam.Ref import dynamicFvMesh_interfaces
attr2interface.update( dynamicFvMesh_interfaces.attr2interface )

from Foam.Ref import randomProcesses_interfaces
attr2interface.update( randomProcesses_interfaces.attr2interface )

from Foam.Ref import sampling_interfaces
attr2interface.update( sampling_interfaces.attr2interface )

from Foam.Ref import thermophisycalModels_interfaces
attr2interface.update( thermophisycalModels_interfaces.attr2interface )

from Foam.Ref import transportModels_interfaces
attr2interface.update( transportModels_interfaces.attr2interface )

from Foam.Ref import compressible_interfaces
attr2interface.update( { 'compressible': TLoadHelper( compressible_interfaces.attr2interface ) } )

from Foam.Ref import incompressible_interfaces
attr2interface.update( { 'incompressible': TLoadHelper( incompressible_interfaces.attr2interface ) } )

from Foam.Ref import fvc_interfaces
attr2interface.update( { 'fvc' : TLoadHelper( fvc_interfaces.attr2interface ) } )

from Foam.Ref import fvm_interfaces
attr2interface.update( { 'fvm' : TLoadHelper( fvm_interfaces.attr2interface ) } )

from Foam.Ref import fv_interfaces
attr2interface.update( { 'fv' : TLoadHelper( fv_interfaces.attr2interface ) } )

from Foam.Ref import radiation_interfaces
attr2interface.update( { 'radiation': TLoadHelper( radiation_interfaces.attr2interface ) } )

from Foam.Ref import MULES_interfaces
attr2interface.update( { 'MULES': TLoadHelper( MULES_interfaces.attr2interface ) } )

from Foam.Ref import SRF_interfaces
attr2interface.update( { 'SRF': TLoadHelper( SRF_interfaces.attr2interface ) } )
                


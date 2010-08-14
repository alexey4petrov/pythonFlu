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
exec get_module_initializtion_command( "compressible_" ) 


#---------------------------------------------------------------------------
from Foam import FOAM_VERSION, FOAM_BRANCH_VERSION, FOAM_REF_VERSION
if FOAM_VERSION( "<=", "010401" ):
   turbulenceModel = compressible_turbulenceModel
   autoPtr_turbulenceModel = autoPtr_compressible_turbulenceModel
   
   pass


#---------------------------------------------------------------------------
if FOAM_VERSION( "==", "010500" ) or FOAM_BRANCH_VERSION( "dev", ">=", "010500" ):
   RASModel = compressible_RASModel
   autoPtr_RASModel = autoPtr_compressible_RASModel
   
   pass


#----------------------------------------------------------------------------
if FOAM_VERSION(  ">=", "010600" ):
   turbulenceModel = compressible_turbulenceModel
   autoPtr_turbulenceModel = autoPtr_compressible_turbulenceModel

   RASModel = compressible_RASModel
   autoPtr_RASModel = autoPtr_compressible_RASModel
   pass


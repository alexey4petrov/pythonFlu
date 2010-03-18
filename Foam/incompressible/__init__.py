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
from Foam import get_module_initializtion_command
exec get_module_initializtion_command( "incompressible_" ) 


#---------------------------------------------------------------------------
from Foam import WM_PROJECT_VERSION
if WM_PROJECT_VERSION() <= "1.4.1-dev":
   turbulenceModel = incompressible_turbulenceModel
   autoPtr_turbulenceModel = autoPtr_incompressible_turbulenceModel
   pass


#---------------------------------------------------------------------------
if WM_PROJECT_VERSION() == "1.5":
   RASModel = incompressible_RASModel
   autoPtr_RASModel = autoPtr_incompressible_RASModel

   LESModel = incompressible_LESModel
   autoPtr_LESModel = autoPtr_incompressible_LESModel
   pass


#----------------------------------------------------------------------------
if WM_PROJECT_VERSION() >= "1.6":
   RASModel = incompressible_RASModel
   autoPtr_RASModel = autoPtr_incompressible_RASModel

   LESModel = incompressible_LESModel
   autoPtr_LESModel = autoPtr_incompressible_LESModel
   
   turbulenceModel = incompressible_turbulenceModel
   autoPtr_turbulenceModel = autoPtr_incompressible_turbulenceModel
   pass


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


#--------------------------------------------------------------------------------------
include $(pyfoam_root_dir)/foam.version.makefile


#--------------------------------------------------------------------------------------
__CPPFLAGS__ := $(__CPPFLAGS__) \
	-I$(WM_PROJECT_DIR)/src/finiteVolume/lnInclude \
	-I$(WM_PROJECT_DIR)/src/thermophysicalModels/basic/lnInclude \
	-I$(WM_PROJECT_DIR)/src/meshTools/lnInclude \
	-I$(WM_PROJECT_DIR)/src/turbulenceModels \
	-I$(WM_PROJECT_DIR)/src/thermophysicalModels/radiation/lnInclude \
	-I$(WM_PROJECT_DIR)/src/transportModels/incompressible/lnInclude \
	-I$(WM_PROJECT_DIR)/src/transportModels/interfaceProperties/lnInclude \
	-I$(WM_PROJECT_DIR)/src/transportModels \
	-I$(WM_PROJECT_DIR)/src/dynamicFvMesh/lnInclude \
	-I$(WM_PROJECT_DIR)/src/dynamicMesh/lnInclude \
	

ifeq "$(shell if [ ${__FOAM_VERSION__} -eq 010500 ]; then echo 'true'; else echo 'false'; fi )" "true" 
	__CPPFLAGS__ += -I$(WM_PROJECT_DIR)/src/turbulenceModels/LES/LESdeltas/lnInclude
endif

ifeq "$(shell if [ ${__FOAM_VERSION__} -ge 010600 ]; then echo 'true'; else echo 'false'; fi )" "true" 
	__CPPFLAGS__ += -I$(WM_PROJECT_DIR)/src/turbulenceModels/LES/LESdeltas/lnInclude
endif	

ifeq "$(shell if [ ${__FOAM_VERSION__} -ge 010700 ]; then echo 'true'; else echo 'false'; fi )" "true" 
	__CPPFLAGS__ += -I$(WM_PROJECT_DIR)/src/turbulenceModels/compressible/RAS/lnInclude
endif	


#--------------------------------------------------------------------------------------
__LDFLAGS__ := $(__LDFLAGS__) \
	-L$(WM_PROJECT_DIR)/lib/$(WM_OPTIONS) -lfiniteVolume \
	-L$(WM_PROJECT_DIR)/lib/$(WM_OPTIONS) -lbasicThermophysicalModels \
	-L$(WM_PROJECT_DIR)/lib/$(WM_OPTIONS) -lspecie \
	-L$(WM_PROJECT_DIR)/lib/$(WM_OPTIONS) -lincompressibleTransportModels \
	-L$(WM_PROJECT_DIR)/lib/$(WM_OPTIONS) -linterfaceProperties \
	-L$(WM_PROJECT_DIR)/lib/$(WM_OPTIONS) -ldynamicFvMesh	

ifeq "$(shell if [ ${__FOAM_VERSION__} -le 010401 ]; then echo 'true'; else echo 'false'; fi )" "true" 
	__LDFLAGS__ += -L$(WM_PROJECT_DIR)/lib/$(WM_OPTIONS) -lcompressibleTurbulenceModels
	__LDFLAGS__ += -L$(WM_PROJECT_DIR)/lib/$(WM_OPTIONS) -lincompressibleTurbulenceModels
endif

ifeq "$(shell if [ ${__FOAM_VERSION__} -eq 010500 ]; then echo 'true'; else echo 'false'; fi )" "true" 
	__LDFLAGS__ += -L$(WM_PROJECT_DIR)/lib/$(WM_OPTIONS) -lcompressibleLESModels
	__LDFLAGS__ += -L$(WM_PROJECT_DIR)/lib/$(WM_OPTIONS) -lincompressibleLESModels	
	__LDFLAGS__ += -L$(WM_PROJECT_DIR)/lib/$(WM_OPTIONS) -lincompressibleRASModels	
	__LDFLAGS__ += -L$(WM_PROJECT_DIR)/lib/$(WM_OPTIONS) -lcompressibleRASModels
	__LDFLAGS__ += -L$(WM_PROJECT_DIR)/lib/$(WM_OPTIONS) -lradiation	
endif


ifeq "$(shell if [ ${__FOAM_VERSION__} -ge 010600 ]; then echo 'true'; else echo 'false'; fi )" "true" 
	__LDFLAGS__ += -L$(WM_PROJECT_DIR)/lib/$(WM_OPTIONS) -lcompressibleTurbulenceModel
	__LDFLAGS__ += -L$(WM_PROJECT_DIR)/lib/$(WM_OPTIONS) -lincompressibleTurbulenceModel
	__LDFLAGS__ += -L$(WM_PROJECT_DIR)/lib/$(WM_OPTIONS) -lradiation
	__LDFLAGS__ += -L$(WM_PROJECT_DIR)/lib/$(WM_OPTIONS) -lcompressibleLESModels
	__LDFLAGS__ += -L$(WM_PROJECT_DIR)/lib/$(WM_OPTIONS) -lcompressibleRASModels	
	__LDFLAGS__ += -L$(WM_PROJECT_DIR)/lib/$(WM_OPTIONS) -lincompressibleLESModels	
	__LDFLAGS__ += -L$(WM_PROJECT_DIR)/lib/$(WM_OPTIONS) -lincompressibleRASModels		
endif

#--------------------------------------------------------------------------------------
include $(pyfoam_root_dir)/include.makefile


#--------------------------------------------------------------------------------------

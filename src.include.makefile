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


#--------------------------------------------------------------------------------------
include $(pyfoam_root_dir)/foam.version.makefile


#--------------------------------------------------------------------------------------
__CXX_INCLUDES__ := $(__CXX_INCLUDES__) \
	-I$(WM_PROJECT_DIR)/src/finiteVolume/lnInclude \
	-I$(WM_PROJECT_DIR)/src/thermophysicalModels/basic/lnInclude \
	-I$(WM_PROJECT_DIR)/src/meshTools/lnInclude \
	-I$(WM_PROJECT_DIR)/src/turbulenceModels \
	-I$(WM_PROJECT_DIR)/src/thermophysicalModels/radiation/lnInclude \
	-I$(WM_PROJECT_DIR)/src/transportModels/incompressible/lnInclude \
	-I$(WM_PROJECT_DIR)/src/transportModels

	
#--------------------------------------------------------------------------------------
__LIB_FLAGS__ := $(__LIB_FLAGS__) \
	-L$(WM_PROJECT_DIR)/lib/$(WM_OPTIONS) -lfiniteVolume \
	-L$(WM_PROJECT_DIR)/lib/$(WM_OPTIONS) -lbasicThermophysicalModels \
	-L$(WM_PROJECT_DIR)/lib/$(WM_OPTIONS) -lspecie \
	-L$(WM_PROJECT_DIR)/lib/$(WM_OPTIONS) -lincompressibleTransportModels

ifeq "$(shell if [ ${__FOAM_VERSION__} -lt 010500 ]; then echo 'true'; else echo 'false'; fi )" "true" 
	__LIB_FLAGS__ += -L$(WM_PROJECT_DIR)/lib/$(WM_OPTIONS) -lcompressibleTurbulenceModels
	__LIB_FLAGS__ += -L$(WM_PROJECT_DIR)/lib/$(WM_OPTIONS) -lincompressibleTurbulenceModels
else
	__LIB_FLAGS__ += -L$(WM_PROJECT_DIR)/lib/$(WM_OPTIONS) -lcompressibleTurbulenceModel
	__LIB_FLAGS__ += -L$(WM_PROJECT_DIR)/lib/$(WM_OPTIONS) -lincompressibleTurbulenceModel
	__LIB_FLAGS__ += -L$(WM_PROJECT_DIR)/lib/$(WM_OPTIONS) -lradiation 
endif


#--------------------------------------------------------------------------------------
include $(pyfoam_root_dir)/include.makefile


#--------------------------------------------------------------------------------------

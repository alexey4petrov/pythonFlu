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
pyfoam_root_dir:=../../../../..

include $(pyfoam_root_dir)/foam.version.makefile


#--------------------------------------------------------------------------------------
ifeq "$(shell if [ ${__FOAM_VERSION__} -ge 010500 ]; then echo 'true'; else echo 'false'; fi )" "true" 
#--------------------------------------------------------------------------------------

obj_dir := $(WM_PROJECT_DIR)/applications/solvers/heatTransfer/chtMultiRegionFoam/Make/$(WM_OPTIONS)

__CPPFLAGS__ := $(__CPPFLAGS__) \
	-I$(WM_PROJECT_DIR)/src/finiteVolume/lnInclude \
	-I$(WM_PROJECT_DIR)/src/meshTools/lnInclude \
	-I$(WM_PROJECT_DIR)/applications/solvers/heatTransfer/chtMultiRegionFoam/regionProperties 	
	

__LDFLAGS__ := $(__LDFLAGS__) \
	-L$(WM_PROJECT_DIR)/lib/$(WM_OPTIONS) -lfiniteVolume \
	-L$(WM_PROJECT_DIR)/lib/$(WM_OPTIONS) -lbasicThermophysicalModels \
	-L$(WM_PROJECT_DIR)/lib/$(WM_OPTIONS) -lspecie \
	-L$(WM_PROJECT_DIR)/lib/$(WM_OPTIONS) -lcompressibleTurbulenceModel \
	-L$(WM_PROJECT_DIR)/lib/$(WM_OPTIONS) -lcompressibleRASModels \
	-L$(WM_PROJECT_DIR)/lib/$(WM_OPTIONS) -lcompressibleLESModels \
	$(obj_dir)/regionProperties.o \

include $(pyfoam_root_dir)/include.makefile

#--------------------------------------------------------------------------------------
else
#--------------------------------------------------------------------------------------

$(warning To use this functionality it is necessary use OpenFOAM-1.5 or higher)

all:
clean:

#--------------------------------------------------------------------------------------
endif
#--------------------------------------------------------------------------------------

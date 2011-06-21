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


#--------------------------------------------------------------------------------------
include $(pythonflu_root_dir)/Foam/foam.version.makefile


#--------------------------------------------------------------------------------------
#define src_complition_flag to ignore last step in "%.so" target
src_compilation_flag=yes


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
	-I$(WM_PROJECT_DIR)/src/randomProcesses/lnInclude \
	

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
	-L$(WM_PROJECT_DIR)/lib/$(WM_OPTIONS) -ldynamicFvMesh \
	-L$(WM_PROJECT_DIR)/lib/$(WM_OPTIONS) -lrandomProcesses


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

ifeq "$(shell if [ ${__FOAM_VERSION__} -ge 010701 ]; then echo 'true'; else echo 'false'; fi )" "true" 
	__LDFLAGS__ += -L$(WM_PROJECT_DIR)/lib/$(WM_OPTIONS) -ltwoPhaseInterfaceProperties
endif



#--------------------------------------------------------------------------------------
sources = $(filter-out emb_%.cxx,$(wildcard *.cxx))

subdirs := $(shell find -maxdepth 1 -type d)
subdirs := $(subst ./,,$(subdirs))
subdirs := $(subst CVS,,$(subdirs))
subdirs := $(subst cvs,,$(subdirs))
subdirs := $(subst .svn,,$(subdirs))
subdirs := $(subst .,,$(subdirs))

SUBDIRS = $(subdirs)

apps = $(patsubst %.cxx, %.exe, $(sources))
libs = $(patsubst %.cxx, _%.so, $(sources))
objs = $(patsubst %.cxx, %.o, $(sources))
stubs = $(patsubst %.cxx, %.cc, $(sources))
pyths = $(patsubst %.cxx, %.py, $(sources))
tests = $(patsubst %.py, %.pyc, $(wildcard test_*.py))


#--------------------------------------------------------------------------------------
RECURSIVE_TARGETS = all-recursive test-recursive

all: $(libs) $(apps) $(objs) $(stubs) $(tests) all-recursive
	@echo output : $(sources) $(pyths) $(tests)

test: $(pyths) test-recursive

$(RECURSIVE_TARGETS):
	@failcom='exit 1'; \
	for f in x $$MAKEFLAGS; do \
	  case $$f in \
	    *=* | --[!k]*);; \
	    *k*) failcom='fail=yes';; \
	  esac; \
	done; \
	target=`echo $@ | sed s/-recursive//`; \
	list='$(SUBDIRS)'; for subdir in $$list; do \
	  echo "Making $$target in $$subdir"; \
	  if test "$$subdir" = "."; then \
	    break; \
	  fi; \
	  if ! test -f "$$subdir/Makefile"; then \
	    break; \
	  fi; \
	  echo "(cd $$subdir && $(MAKE) $$target)"; \
	  (cd $$subdir && $(MAKE) $$target) \
	  || eval $$failcom; \
	done; \


#--------------------------------------------------------------------------------------
RECURSIVE_CLEAN_TARGETS = clean-recursive

clean: clean-recursive
	rm -fr $(apps) $(libs) $(objs) $(stubs) $(pyths) *.h *.pyc *.d *~

$(RECURSIVE_CLEAN_TARGETS):
	@failcom='exit 1'; \
	for f in x $$MAKEFLAGS; do \
	  case $$f in \
	    *=* | --[!k]*);; \
	    *k*) failcom='fail=yes';; \
	  esac; \
	done; \
	dot_seen=no; \
	case "$@" in \
	  distclean-* | maintainer-clean-*) list='$(DIST_SUBDIRS)' ;; \
	  *) list='$(SUBDIRS)' ;; \
	esac; \
	rev=''; for subdir in $$list; do \
	  if test "$$subdir" = "."; then :; else \
	    rev="$$subdir $$rev"; \
	  fi; \
	done; \
	rev="$$rev ."; \
	target=`echo $@ | sed s/-recursive//`; \
	for subdir in $$rev; do \
	  if test "$$subdir" = "."; then \
	    break; \
	  fi; \
	  if ! test -f "$$subdir/Makefile"; then \
	    break; \
	  fi; \
	  echo "(cd $$subdir && $(MAKE) $$target)"; \
	  (cd $$subdir && $(MAKE) $$target) \
	  || eval $$failcom; \
	done && test -z "$$fail"


#--------------------------------------------------------------------------------------
include $(pythonflu_root_dir)/Foam/include.base.makefile


#--------------------------------------------------------------------------------------

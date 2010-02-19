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
__FOAM_VERSION__ := $(subst -dev,,$(WM_PROJECT_VERSION))
__FOAM_VERSION__ := $(subst 1.4.1,010401,$(__FOAM_VERSION__))
__FOAM_VERSION__ := $(subst 1.5,010500,$(__FOAM_VERSION__))
__FOAM_VERSION__ := $(subst 1.6,010600,$(__FOAM_VERSION__))

__FOAM_PATCH__:=$(WM_PROJECT_VERSION)
__FOAM_PATCH__:=$(subst 1.4.1-dev,1.4.1,$(WM_PROJECT_VERSION))


#------------------------------------------------------------------------------
# set compilation and dependency building rules
#------------------------------------------------------------------------------
GENERAL_RULES = $(WM_DIR)/rules/General
RULES         = $(WM_DIR)/rules/$(WM_ARCH)$(WM_COMPILER)
BIN           = $(WM_DIR)/bin/$(WM_ARCH)$(WM_COMPILER)

include $(GENERAL_RULES)/general
include $(RULES)/general
include $(RULES)/$(WM_LINK_LANGUAGE)

c++FLAGS:=$(shell echo $(c++FLAGS) | sed -e"s%-Wold-style-cast %%g")


#------------------------------------------------------------------------------
# declare default paths
#------------------------------------------------------------------------------
LIB_SRC            = $(WM_PROJECT_DIR)/src
LIB_DIR            = $(WM_PROJECT_DIR)/lib
LIB_WM_OPTIONS_DIR = $(LIB_DIR)/$(WM_OPTIONS)
OBJECTS_DIR        = $(MAKE_DIR)/$(WM_OPTIONS)
CLASSES_DIR        = $(MAKE_DIR)/classes

SYS_INC            =
SYS_LIBS           =

PROJECT_INC        = -I$(LIB_SRC)/$(WM_PROJECT)/lnInclude -I$(LIB_SRC)/OSspecific/$(WM_OSTYPE)/lnInclude
PROJECT_LIBS       = -l$(WM_PROJECT)


#--------------------------------------------------------------------------------------
PYTHON_VERSION := $(shell python -c "import sys; print sys.version[:3]")

ifndef PYTHON_INCLUDE
	PYTHON_INCLUDE := /usr/include/python$(PYTHON_VERSION)
endif

__CXX_INCLUDES__:=$(__CXX_INCLUDES__) $(PROJECT_INC) -I$(PYTHON_INCLUDE) -I$(pyfoam_root_dir)


#--------------------------------------------------------------------------------------
__LIB_FLAGS__:=$(__LIB_FLAGS__) -lstdc++

ifdef WM_PROJECT_VERSION
	__LIB_FLAGS__:=-L$(LIB_WM_OPTIONS_DIR) $(PROJECT_LIBS) $(__LIB_FLAGS__) -lpthread -ldl -lm
endif

PYTHON_LIB := -lpython$(PYTHON_VERSION)
ifdef PYTHONHOME
	PYTHON_LIB := $(PYTHONHOME)/lib/libpython$(PYTHON_VERSION).so
endif

__LIB_FLAGS__ := $(__LIB_FLAGS__) $(PYTHON_LIB)


#--------------------------------------------------------------------------------------
subdirs := $(shell find -maxdepth 1 -type d)
subdirs := $(subst ./,,$(subdirs))
subdirs := $(subst CVS,,$(subdirs))
subdirs := $(subst cvs,,$(subdirs))
subdirs := $(subst .svn,,$(subdirs))
subdirs := $(subst .,,$(subdirs))

SUBDIRS = $(subdirs)

apps = $(patsubst %.cxx, %, $(wildcard *.cxx))
libs = $(patsubst %.cxx, _%.so, $(wildcard *.cxx))
objs = $(patsubst %.cxx, %.o, $(wildcard *.cxx))
stubs = $(patsubst %.cxx, %.cpp, $(wildcard *.cxx))
pyths = $(patsubst %.cxx, %.py, $(wildcard *.cxx))
tests = $(patsubst %.py, %.pyc, $(wildcard test_*.py))


#--------------------------------------------------------------------------------------
RECURSIVE_TARGETS = all-recursive test-recursive

all: $(libs) $(apps) $(objs) $(stubs) $(tests) all-recursive
	@echo output : $(pyths) $(tests)

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
__SWIG_INCLUDES__=-I$(pyfoam_root_dir)/patch-$(__FOAM_PATCH__) $(__CXX_INCLUDES__)

__SWIG_FLAGS__ = -python -c++ -MD -D__restrict__ -D__CINT__ $(GFLAGS) $(__SWIG_INCLUDES__)

__SWIG_FLAGS__+=-w508 # Declaration of 'XXX' shadows declaration accessible via 'YYY"
__SWIG_FLAGS__+=-w317 # Specialization of non-template 'XXX'
__SWIG_FLAGS__+=-w312 # Nested class not currently supported (ignored)
__SWIG_FLAGS__+=-w509 # Overloaded method 'XXX' is shadowed by 'YYY'
__SWIG_FLAGS__+=-w503 # Can't wrap 'XXX' unless renamed to a valid identifier
__SWIG_FLAGS__+=-w462 # Unable to set dimensionless array variable
__SWIG_FLAGS__+=-w473 # Returning a pointer or reference in a director method is not recommended

ifdef WM_PROJECT_VERSION
	__SWIG_FLAGS__+=-D__FOAM_VERSION__=$(__FOAM_VERSION__)
	__SWIG_FLAGS__+=$(shell if [ ${__FOAM_VERSION__} -lt 010600 ]; then echo -DINT_MAX=2147483647; fi )
endif

#-debug-top 4 -directors -dirprot


#--------------------------------------------------------------------------------------
%.cpp : %.cxx
	swig $(__SWIG_FLAGS__) -module $(patsubst %.cxx,%,$<) -o $@ $<

__OBJ_FLAGS__ := $(__OBJ_FLAGS__) $(c++FLAGS) -D__FOAM_VERSION__=$(__FOAM_VERSION__) $(__CXX_INCLUDES__)

%.o : %.cpp
	gcc $(__OBJ_FLAGS__)  "-I." "-D DIRECTOR_INCLUDE=<$(patsubst %.cpp,%.h,$<)>" -c $< -o $@


PACKAGE_DEPENDENCIES = $(wildcard *.d)
ifneq "$(PACKAGE_DEPENDENCIES)" "" # To avoid "include's" warning in case of empty folder
	include $(PACKAGE_DEPENDENCIES)
endif


_%.so : %.o
	$(LINKLIBSO) $< $(__LIB_FLAGS__) -o $@

__APP_FLAGS__ = $(__LIB_FLAGS__)

% : %.o
	gcc $< $(__APP_FLAGS__) -o $@
	python $@.py

%.pyc : %.py
	@python -c "import py_compile; py_compile.compile('$<')"
	@python ./$@


#--------------------------------------------------------------------------------------


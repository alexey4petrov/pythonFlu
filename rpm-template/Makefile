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
DESTDIR=
PYTHON_FLU_BIN=$(DESTDIR)/usr/local/bin
PYTHON_FLU_LIB=$(DESTDIR)/usr/local/lib/python2.6/site-packages/

BUILD_DIR=/usr/src/packages/BUILD
solvers_preparation_dir=$(BUILD_DIR)/solvers
libs_preparation_dir=$(BUILD_DIR)

files_list="list_installed_files"

dirs := $(shell ls Foam/applications/solvers -F | grep / | sed 's/\///g')

solvers_template :=  $(addsuffix /*Foam.py, $(addprefix Foam/applications/solvers/, $(dirs)))

solvers := $(wildcard $(solvers_template) )

solvers_in_lib := $(addprefix $(solvers_preparation_dir), $(solvers))

preparation:$(libs_preparation_dir)/Foam

$(libs_preparation_dir)/Foam:
	@ cp -rf Foam $(libs_preparation_dir)/
	@ install -d $(solvers_preparation_dir)
	@ install -m 755 $(solvers) $(solvers_preparation_dir)
	@ rm -f $(solvers_in_lib)
	@ solvers_=`ls $(solvers_preparation_dir)/*Foam.py`; \
	  for solver in $$solvers_; do \
	      solver_file=`basename $$solver `; \
	      solver_name=`basename $$solver .py `; \
	      new_solver_name=`echo $$solver_name | sed 's/Foam/Flux/g'`;  \
	      ( cd $(solvers_preparation_dir) && mv $$solver_file $$new_solver_name ); \
	  done;

install: $(PYTHON_FLU_LIB)/Foam

$(PYTHON_FLU_LIB)/Foam: 
	@ install -d $(PYTHON_FLU_LIB) $(PYTHON_FLU_BIN)
	@ cp -rf $(libs_preparation_dir)/Foam $(PYTHON_FLU_LIB)/
	@ cp $(solvers_preparation_dir)/* $(PYTHON_FLU_BIN)



#--------------------------------------------------------------------------------------     	

#!/bin/bash

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
#Prepare variables for substition in  control,changelog etc files
export DEBEMAIL='alexey.petrov.nnov@gmail.com'
export DEBFULLNAME="Alexey Petrov"


#--------------------------------------------------------------------------------------
# Prepare folder for deb-packaging and copy folder "Foam" to it 
package_name="pythonflu-dev"
package_version="1.5-1726-1ppa2"
curr_folder=`pwd`
package_folder=${curr_folder}/${package_name}-${package_version}
template_folder=${curr_folder}/deb-template
key_id="7533E278"


install -d ${package_folder}
echo "Copying \"Foam\" to ${package_folder}"
cp -rf Foam ${package_folder}


#--------------------------------------------------------------------------------------
#remove all unnecessary from the ${package_folder}
cd ${package_folder}
echo "cleaning cxx, h, o, etc..."
find \( -name "*.cxx" -o -name "*.h" -o -name "*.d" -o -name "pyfoam" \) -delete
find \( -name "*.h" -o -name "*_" -o -name "*.o" -o -name "*.in" -o -name "Makefile" -o -name "*.pyc" \) -delete
find ./ -name ".svn" -exec rm -rf {} \; 2>/dev/null


#--------------------------------------------------------------------------------------
#create folder debian with control,changelog, etc files
echo "create debian folder and all necessary files( control, changelog etc ) in it "
cp ${template_folder}/Makefile ${package_folder}
dh_make -s -c gpl -createorig --templates ${template_folder} -p ${package_name}


#---------------------------------------------------------------------------------------
#create package
echo "create package"
dpkg-buildpackage -rfakeroot -k${key_id}

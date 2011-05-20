//  VulaSHAKA (Simultaneous Neutronic, Fuel Performance, Heat And Kinetics Analysis)
//  Copyright (C) 2009-2010 Pebble Bed Modular Reactor (Pty) Limited (PBMR)
//  
//  This program is free software: you can redistribute it and/or modify
//  it under the terms of the GNU General Public License as published by
//  the Free Software Foundation, either version 3 of the License, or
//  (at your option) any later version.
//  
//  This program is distributed in the hope that it will be useful,
//  but WITHOUT ANY WARRANTY; without even the implied warranty of
//  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//  GNU General Public License for more details.
//  
//  You should have received a copy of the GNU General Public License
//  along with this program.  If not, see <http://www.gnu.org/licenses/>.
//
//  See http://sourceforge.net/projects/pythonflu
//
//  Author : Alexey PETROV


//---------------------------------------------------------------------------
#ifndef coordinateSystem_cxx
#define coordinateSystem_cxx


//---------------------------------------------------------------------------
%module "Foam.src.meshTools.coordinateSystems.coordinateSystem";
%{
  #include "src/meshTools/coordinateSystems/coordinateSystem.hh"
%}


//---------------------------------------------------------------------------
%import "src/OpenFOAM/primitives/vector.cxx"

%import "src/OpenFOAM/meshes/primitiveShapes/point/point.cxx"

%import "src/OpenFOAM/primitives/tensor.cxx"

%import "src/OpenFOAM/fields/Fields/primitiveFields.cxx"

%import "src/OpenFOAM/meshes/primitiveShapes/point/pointField.cxx"

%import "src/OpenFOAM/fields/tmp/tmp.cxx"

%import "src/meshTools/coordinateSystems/coordinateRotation/coordinateRotation.cxx"

%import "src/OpenFOAM/db/objectRegistry.cxx"

%include <coordinateSystem.H>


//---------------------------------------------------------------------------
#endif

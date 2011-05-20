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
#ifndef porousZone_cxx
#define porousZone_cxx


//---------------------------------------------------------------------------
%module "Foam.src.finiteVolume.cfdTools.general.porousMedia.porousZone";
%{
  #include "src/finiteVolume/cfdTools/general/porousMedia/porousZone.hh"
%}


//---------------------------------------------------------------------------
%import "src/OpenFOAM/db/dictionary/dictionary.cxx"

%import "src/meshTools/coordinateSystems/coordinateSystem.cxx"

%import "src/meshTools/coordinateSystems/coordinateSystems.cxx"

%import "src/OpenFOAM/primitives/Lists/wordList.cxx"

%import "src/OpenFOAM/primitives/Lists/labelList.cxx"

%import "src/OpenFOAM/dimensionedTypes/dimensionedScalar.cxx"

%import "src/OpenFOAM/dimensionedTypes/dimensionedTensor.cxx"

%import "src/OpenFOAM/fields/Fields/primitiveFieldsFwd.cxx"

%import "src/finiteVolume/fvMatrices/fvMatrices.cxx"

%import "src/finiteVolume/fvMesh/fvMeshes.cxx"

%include <porousZone.H>


//---------------------------------------------------------------------------
#endif

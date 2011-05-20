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
#ifndef Random_cxx
#define Random_cxx


//---------------------------------------------------------------------------
%module "Foam.src.OpenFOAM.primitives.Random";
%{
  #include "src/OpenFOAM/primitives/Random.hh"
%}


//---------------------------------------------------------------------------
%import "src/common.hxx"

%import "src/OpenFOAM/primitives/label.cxx"

%import "src/OpenFOAM/primitives/scalar.cxx"

%import "src/OpenFOAM/primitives/vector.cxx"

%import "src/OpenFOAM/primitives/tensor.cxx"

%import "src/OpenFOAM/primitives/symmTensor.cxx"

%import "src/OpenFOAM/primitives/sphericalTensor.cxx"

%include <Random.H>


//---------------------------------------------------------------------------
#endif

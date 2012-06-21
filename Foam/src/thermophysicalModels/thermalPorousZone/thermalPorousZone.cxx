//  pythonFlu - Python wrapping for OpenFOAM C++ API
//  Copyright (C) 2010- Alexey Petrov
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
//  Author : Alexey PETROV, Andrey SIMURZIN


//---------------------------------------------------------------------------
%module "Foam.src.thermophysicalModels.thermalPorousZone.thermalPorousZone";

%{
  #include "Foam/src/thermophysicalModels/thermalPorousZone/thermalPorousZone.hh"
%}


//---------------------------------------------------------------------------
%import "Foam/src/common.hxx"

#if FOAM_VERSION( <, 020000 )
#define thermalPorousZone_cxx
#endif


//-----------------------------------------------------------------------------
#ifndef thermalPorousZone_cxx
#define thermalPorousZone_cxx


//---------------------------------------------------------------------------
%import "Foam/src/finiteVolume/fvMesh/fvMeshes.cxx"

%import "Foam/src/finiteVolume/cfdTools/general/porousMedia/porousZone.cxx"

%import "Foam/src/OpenFOAM/fields/tmp/autoPtr_basicThermo.cxx"

%include <thermalPorousZone.H>


//---------------------------------------------------------------------------
#endif

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
//  See https://vulashaka.svn.sourceforge.net/svnroot/vulashaka
//
//  Author : Alexey PETROV


//---------------------------------------------------------------------------
#ifndef fvcReconstruct_hh
#define fvcReconstruct_hh


//----------------------------------------------------------------------------
#include "src/finiteVolume/fields/volFields/volFields.hh"
#include "src/finiteVolume/fields/surfaceFields/surfaceFields.hh"

#include <fvcSurfaceIntegrate.H>
#include <fvcReconstruct.H>


//---------------------------------------------------------------------------
#include "src/OpenFOAM/fields/tmp/tmp_surfaceVectorField.hh"

#include "src/OpenFOAM/fields/tmp/tmp_surfaceScalarField.hh"

#include "src/finiteVolume/fvMesh/fvMesh.hh"
#include "src/finiteVolume/fields/fvPatchFields/zeroGradient/zeroGradientFvPatchFields.hh"


//---------------------------------------------------------------------------
#endif

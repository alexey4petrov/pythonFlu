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
//  Author : Alexey PETROV


//---------------------------------------------------------------------------
#ifndef no_tmp_typemap_GeometricFields_hh
#define no_tmp_typemap_GeometricFields_hh


//---------------------------------------------------------------------------
#include "src/OpenFOAM/fields/GeometricFields/GeometricField.hh"

#include "src/OpenFOAM/fields/tmp/tmp.hh"

#include "ext/common/ext_tmp.hh"


//---------------------------------------------------------------------------
#include "src/OpenFOAM/primitives/scalar.hh"
#include "src/finiteVolume/volMesh.hh"
#include "src/finiteVolume/fields/fvPatchFields/fvPatchField.hh"


//----------------------------------------------------------------------------
#include "src/OpenFOAM/primitives/vector.hh"
#include "src/finiteVolume/volMesh.hh"
#include "src/finiteVolume/fields/fvPatchFields/fvPatchField.hh"


//----------------------------------------------------------------------------
#include "src/OpenFOAM/primitives/tensor.hh"
#include "src/finiteVolume/volMesh.hh"
#include "src/finiteVolume/fields/fvPatchFields/fvPatchField.hh"


//-----------------------------------------------------------------------------
#include "src/OpenFOAM/primitives/symmTensor.hh"
#include "src/finiteVolume/volMesh.hh"
#include "src/finiteVolume/fields/fvPatchFields/fvPatchField.hh"


//------------------------------------------------------------------------------
#include "src/OpenFOAM/primitives/sphericalTensor.hh"
#include "src/finiteVolume/volMesh.hh"
#include "src/finiteVolume/fields/fvPatchFields/fvPatchField.hh"


//------------------------------------------------------------------------------
#include "src/OpenFOAM/primitives/scalar.hh"
#include "src/finiteVolume/surfaceMesh.hh"
#include "src/finiteVolume/fields/fvsPatchFields/fvsPatchField.hh"


//-------------------------------------------------------------------------------
#include "src/OpenFOAM/primitives/vector.hh"
#include "src/finiteVolume/surfaceMesh.hh"
#include "src/finiteVolume/fields/fvsPatchFields/fvsPatchField.hh"


//-------------------------------------------------------------------------------
#include "src/OpenFOAM/primitives/tensor.hh"
#include "src/finiteVolume/surfaceMesh.hh"
#include "src/finiteVolume/fields/fvsPatchFields/fvsPatchField.hh"


//-------------------------------------------------------------------------------
#endif

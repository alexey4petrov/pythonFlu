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
#ifndef fvmDdt_hh
#define fvmDdt_hh


//---------------------------------------------------------------------------
#include "Foam/src/finiteVolume/fields/fvPatchFields/fvPatchField.hh"

#include <fvmDdt.H>


//---------------------------------------------------------------------------
#include "Foam/src/OpenFOAM/dimensionedTypes/dimensionedScalar.hh"
#include "Foam/src/finiteVolume/fields/volFields/volScalarField.hh"


//---------------------------------------------------------------------------
#include "Foam/src/OpenFOAM/fields/tmp/tmp_fvScalarMatrix.hh"
#include "Foam/ext/common/finiteVolume/managedFlu/fvScalarMatrixHolder.hh"
#include "Foam/src/OpenFOAM/fields/GeometricFields/GeometricField_scalar_fvPatchField_volMesh.hh"


//---------------------------------------------------------------------------
#include "Foam/src/OpenFOAM/fields/tmp/tmp_fvVectorMatrix.hh"
#include "Foam/ext/common/finiteVolume/managedFlu/fvVectorMatrixHolder.hh"
#include "Foam/src/OpenFOAM/fields/GeometricFields/GeometricField_vector_fvPatchField_volMesh.hh"


//---------------------------------------------------------------------------
#include "Foam/src/finiteVolume/volMesh.hh"


//---------------------------------------------------------------------------
#endif

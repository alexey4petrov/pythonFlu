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
#ifndef PrimitivePatch_cxx
#define PrimitivePatch_cxx


//---------------------------------------------------------------------------
%module "Foam.src.OpenFOAM.meshes.PrimitivePatch.PrimitivePatch"
%{
  #include "src/OpenFOAM/meshes/PrimitivePatch/PrimitivePatch.hh"
%}


//---------------------------------------------------------------------------
%import "src/OpenFOAM/primitives/Lists/boolList.cxx"

%import "src/OpenFOAM/primitives/Lists/labelList.cxx"

// #include <edgeList.H>

%import "src/OpenFOAM/meshes/primitiveShapes/point/pointField.cxx"

%import "src/OpenFOAM/fields/Fields/primitiveFields.cxx"

// #include <intersection.H>

// #include <labelHashSet.H>

#if FOAM_NOT_BRANCH( free )
%include <PrimitivePatch.H>
#else
%include <PrimitivePatch_.H>
#endif


//---------------------------------------------------------------------------
#endif

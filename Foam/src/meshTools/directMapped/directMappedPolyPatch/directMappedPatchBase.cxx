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
%module "Foam.src.meshTools.directMapped.directMappedPolyPatch.directMappedPatchBase";
%{
  #include "Foam/src/meshTools/directMapped/directMappedPolyPatch/directMappedPatchBase.hh"
%}


//---------------------------------------------------------------------------
%import "Foam/src/common.hxx"

#if FOAM_VERSION( <, 010600 ) || FOAM_VERSION( >=, 020100 )
#define directMappedPatchBase_cxx
#endif


//---------------------------------------------------------------------------
#ifndef directMappedPatchBase_cxx
#define directMappedPatchBase_cxx


//---------------------------------------------------------------------------
%import "Foam/src/OpenFOAM/meshes/primitiveShapes/point/pointField.cxx"

%import "Foam/src/OpenFOAM/fields/tmp/autoPtr_polyPatch.cxx"

// #include "Tuple2.H"
// #include "pointIndexHit.H"

%import "Foam/src/OpenFOAM/meshes/polyMesh/mapPolyMesh/mapDistribute/mapDistribute.cxx"

%include <directMappedPatchBase.H>

%extend Foam::directMappedPatchBase
{
  TYPEINFO_EXTENDS( polyPatch, directMappedPatchBase );
}


//---------------------------------------------------------------------------
#endif

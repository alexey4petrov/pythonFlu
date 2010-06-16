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
#ifndef DimensionedField_tensor_surfaceMesh_cxx
#define DimensionedField_tensor_surfaceMesh_cxx


//---------------------------------------------------------------------------
// Keep on corresponding "director" includes at the top of SWIG defintion file

%include "src/OpenFOAM/directors.hxx"

%include "src/finiteVolume/directors.hxx"


//---------------------------------------------------------------------------
%include "src/OpenFOAM/fields/DimensionedFields/DimensionedField.cxx"

%include "src/OpenFOAM/fields/Fields/tensorField.cxx"

%include "src/finiteVolume/surfaceMesh.hxx"

%ignore Foam::DimensionedField< Foam::tensor, Foam::surfaceMesh >::typeName;
%ignore Foam::DimensionedField< Foam::tensor, Foam::surfaceMesh >::debug;
%ignore Foam::DimensionedField< Foam::tensor, Foam::surfaceMesh >::T;

DIMENSIONED_FIELD_TEMPLATE_FUNC( tensor, surfaceMesh )


//---------------------------------------------------------------------------
%template( DimensionedField_tensor_surfaceMesh ) Foam::DimensionedField< Foam::tensor, Foam::surfaceMesh >;


//---------------------------------------------------------------------------

#endif

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
#ifndef DimensionedField_vector_surfaceMesh_cpp
#define DimensionedField_vector_surfaceMesh_cpp


//---------------------------------------------------------------------------
%module "Foam.src.OpenFOAM.fields.DimensionedFields.DimensionedField_vector_surfaceMesh";
%{
  #include "src/OpenFOAM/fields/DimensionedFields/DimensionedField_vector_surfaceMesh.hh"
%}


//---------------------------------------------------------------------------
%include "src/OpenFOAM/fields/DimensionedFields/DimensionedField.cpp"

%import "src/OpenFOAM/fields/Fields/vectorField.cxx"
%import "src/finiteVolume/surfaceMesh.hpp"

%ignore Foam::DimensionedField< Foam::vector, Foam::surfaceMesh >::typeName;
%ignore Foam::DimensionedField< Foam::vector, Foam::surfaceMesh >::debug;
%ignore Foam::DimensionedField< Foam::vector, Foam::surfaceMesh >::T;

VECTOR_DIMENSIONED_FIELD_TEMPLATE_FUNC( surfaceMesh )

%template( DimensionedField_vector_surfaceMesh ) Foam::DimensionedField< Foam::vector, Foam::surfaceMesh >;


//---------------------------------------------------------------------------

#endif

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
#ifndef GeometricField_vector_fvsPatchField_surfaceMesh_cxx
#define GeometricField_vector_fvsPatchField_surfaceMesh_cxx


//---------------------------------------------------------------------------
// Keep on corresponding "director" includes at the top of SWIG defintion file

%include "src/OpenFOAM/directors.hxx"

%include "src/finiteVolume/directors.hxx"


//---------------------------------------------------------------------------
%include "src/OpenFOAM/fields/GeometricFields/GeometricField.cxx"
%include "src/finiteVolume/fields/fvsPatchFields/fvsPatchField.cxx"
%include "src/OpenFOAM/fields/DimensionedFields/DimensionedField_vector_surfaceMesh.cxx"


//----------------------------------------------------------------------------
%template ( TGeometricBoundaryField_vector_fvsPatchField_surfaceMesh ) Foam::TGeometricBoundaryField< Foam::vector, Foam::fvsPatchField, Foam::surfaceMesh >;

%feature( "pythonappend" ) Foam::TGeometricBoundaryField< Foam::vector, Foam::fvsPatchField, Foam::surfaceMesh >::NESTEDCLASS_PYAPPEND_GETATTR( TGeometricBoundaryField_vector_fvsPatchField_surfaceMesh );

%extend Foam::TGeometricBoundaryField< Foam::vector, Foam::fvsPatchField, Foam::surfaceMesh >
{
    NESTEDCLASS_EXTEND_ATTR( TGeometricBoundaryField_vector_fvsPatchField_surfaceMesh )
    TGEOM_BOUND_FIELD_GETITEM_EXTEND( Foam::fvsPatchField_vector )
}


//-------------------------------------------------------------------------------
%ignore Foam::GeometricField< Foam::vector, Foam::fvsPatchField, Foam::surfaceMesh >::debug;
%ignore Foam::GeometricField< Foam::vector, Foam::fvsPatchField, Foam::surfaceMesh >::typeName;
%ignore Foam::GeometricField< Foam::vector, Foam::fvsPatchField, Foam::surfaceMesh >::boundaryField;
%ignore Foam::GeometricField< Foam::vector, Foam::fvsPatchField, Foam::surfaceMesh >::T;
%ignore Foam::GeometricField< Foam::vector, Foam::fvsPatchField, Foam::surfaceMesh >::correctBoundaryConditions;
%ignore Foam::GeometricField< Foam::vector, Foam::fvsPatchField, Foam::surfaceMesh >::scale;
%ignore Foam::GeometricField< Foam::vector, Foam::fvsPatchField, Foam::surfaceMesh >::min;
%ignore Foam::GeometricField< Foam::vector, Foam::fvsPatchField, Foam::surfaceMesh >::max;

%include "src/OpenFOAM/dimensionedTypes/dimensionedVector.cxx"

VECTOR_GEOMETRIC_FIELD_TEMPLATE_FUNC( Foam::fvsPatchField, Foam::surfaceMesh );


//---------------------------------------------------------------------------
%template( GeometricField_vector_fvsPatchField_surfaceMesh ) Foam::GeometricField< Foam::vector, Foam::fvsPatchField, Foam::surfaceMesh >;

%inline
{
    namespace Foam
    {
        typedef GeometricField< vector, fvsPatchField, surfaceMesh > surfaceVectorField;
    }
}

//---------------------------------------------------------------------------
#endif

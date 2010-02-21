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
//  See https://csrcs.pbmr.co.za/svn/nea/prototypes/reaktor/pyfoam
//
//  Author : Alexey PETROV


//---------------------------------------------------------------------------
#ifndef GeometricField_scalar_fvPatchField_volMesh_cxx
#define GeometricField_scalar_fvPatchField_volMesh_cxx


//---------------------------------------------------------------------------
%include "src/OpenFOAM/fields/FieldFields/FieldField.cxx"

%include "src/OpenFOAM/fields/tmp/refCount.cxx"

%include "src/OpenFOAM/containers/Lists/PtrList/PtrList_scalarField.cxx"

%include "src/OpenFOAM/fields/FieldFields/FieldField_fvPatchField_scalar.cxx"


//---------------------------------------------------------------------------
%include "src/OpenFOAM/fields/GeometricFields/GeometricField.cxx"

%include "src/OpenFOAM/fields/DimensionedFields/DimensionedField_scalar_volMesh.cxx"

%template ( TGeometricBoundaryField_scalar_fvPatchField_volMesh ) Foam::TGeometricBoundaryField< Foam::scalar, Foam::fvPatchField, Foam::volMesh >;

%ignore Foam::GeometricField< Foam::scalar, Foam::fvPatchField, Foam::volMesh >::debug;
%ignore Foam::GeometricField< Foam::scalar, Foam::fvPatchField, Foam::volMesh >::typeName;
%ignore Foam::GeometricField< Foam::scalar, Foam::fvPatchField, Foam::volMesh >::boundaryField;
%ignore Foam::GeometricField< Foam::scalar, Foam::fvPatchField, Foam::volMesh >::scale;
%ignore Foam::GeometricField< Foam::scalar, Foam::fvPatchField, Foam::volMesh >::min;
%ignore Foam::GeometricField< Foam::scalar, Foam::fvPatchField, Foam::volMesh >::max;
%ignore Foam::GeometricField< Foam::scalar, Foam::fvPatchField, Foam::volMesh >::T;

%include "src/OpenFOAM/dimensionedTypes/dimensionedScalar.cxx"

//---------------------------------------------------------------------------
%template( GeometricField_scalar_fvPatchField_volMesh ) Foam::GeometricField< Foam::scalar, Foam::fvPatchField, Foam::volMesh >;

SCALAR_GEOMETRIC_FIELD_TEMPLATE_FUNC( Foam::fvPatchField, Foam::volMesh );

%inline
{
    namespace Foam
    {
        typedef GeometricField< scalar, fvPatchField, volMesh > volScalarField;
    }
}




//---------------------------------------------------------------------------
#endif

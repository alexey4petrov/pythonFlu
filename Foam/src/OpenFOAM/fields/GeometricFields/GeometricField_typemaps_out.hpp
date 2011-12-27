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
#ifndef GeometricField_typemaps_out_hpp
#define GeometricField_typemaps_out_hpp


//---------------------------------------------------------------------------
%import "Foam/ext/common/smart_tmp.hxx"


//---------------------------------------------------------------------------
%define GEOMETRIC_FIELD_TYPEMAP_OUT( Type, TPatchField, TMesh )

%typemap( out ) Foam::GeometricField< Type, TPatchField, TMesh >& 
{
 $result = SWIG_NewPointerObj( ( new Foam::smart_tmp< Foam::GeometricField< Type, TPatchField, TMesh > >( *$1 ) ), $descriptor( Foam::smart_tmp< Foam::GeometricField< Type, TPatchField, TMesh > >* ), SWIG_POINTER_OWN |  0 );
}

%enddef


//---------------------------------------------------------------------------
%import "Foam/src/OpenFOAM/primitives/scalar.cxx"
%include "Foam/src/finiteVolume/volMesh.hpp"
%include "Foam/src/finiteVolume/fields/fvPatchFields/fvPatchField.cpp"

GEOMETRIC_FIELD_TYPEMAP_OUT( Foam::scalar, Foam::fvPatchField, Foam::volMesh );


//----------------------------------------------------------------------------
%import "Foam/src/OpenFOAM/primitives/vector.cxx"
%include "Foam/src/finiteVolume/volMesh.hpp"
%include "Foam/src/finiteVolume/fields/fvPatchFields/fvPatchField.cpp"

GEOMETRIC_FIELD_TYPEMAP_OUT( Foam::Vector< Foam::scalar >, Foam::fvPatchField, Foam::volMesh );


//----------------------------------------------------------------------------
%import "Foam/src/OpenFOAM/primitives/tensor.cxx"
%include "Foam/src/finiteVolume/volMesh.hpp"
%include "Foam/src/finiteVolume/fields/fvPatchFields/fvPatchField.cpp"

GEOMETRIC_FIELD_TYPEMAP_OUT( Foam::Tensor< Foam::scalar >, Foam::fvPatchField, Foam::volMesh );


//-----------------------------------------------------------------------------
%import "Foam/src/OpenFOAM/primitives/symmTensor.cxx"
%include "Foam/src/finiteVolume/volMesh.hpp"
%include "Foam/src/finiteVolume/fields/fvPatchFields/fvPatchField.cpp"
GEOMETRIC_FIELD_TYPEMAP_OUT( Foam::SymmTensor< Foam::scalar >, Foam::fvPatchField, Foam::volMesh );


//------------------------------------------------------------------------------
%import "Foam/src/OpenFOAM/primitives/sphericalTensor.cxx"
%include "Foam/src/finiteVolume/volMesh.hpp"
%include "Foam/src/finiteVolume/fields/fvPatchFields/fvPatchField.cpp"

GEOMETRIC_FIELD_TYPEMAP_OUT( Foam::SphericalTensor< Foam::scalar >, Foam::fvPatchField, Foam::volMesh );


//------------------------------------------------------------------------------
%import "Foam/src/OpenFOAM/primitives/scalar.cxx"
%include "Foam/src/finiteVolume/surfaceMesh.hpp"
%include "Foam/src/finiteVolume/fields/fvsPatchFields/fvsPatchField.cpp"

GEOMETRIC_FIELD_TYPEMAP_OUT( Foam::scalar, Foam::fvsPatchField, Foam::surfaceMesh );


//-------------------------------------------------------------------------------
%import "Foam/src/OpenFOAM/primitives/vector.cxx"
%include "Foam/src/finiteVolume/surfaceMesh.hpp"
%include "Foam/src/finiteVolume/fields/fvsPatchFields/fvsPatchField.cpp"

GEOMETRIC_FIELD_TYPEMAP_OUT( Foam::Vector< Foam::scalar >, Foam::fvsPatchField, Foam::surfaceMesh );


//-------------------------------------------------------------------------------
%import "Foam/src/OpenFOAM/primitives/tensor.cxx"
%include "Foam/src/finiteVolume/surfaceMesh.hpp"
%include "Foam/src/finiteVolume/fields/fvsPatchFields/fvsPatchField.cpp"

NO_TMP_TYPEMAP_GEOMETRIC_FIELD( Foam::Tensor< Foam::scalar >, Foam::fvsPatchField, Foam::surfaceMesh );


//-------------------------------------------------------------------------------
#endif

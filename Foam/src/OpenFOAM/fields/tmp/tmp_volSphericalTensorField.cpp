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
//  See https://vulashaka.svn.sourceforge.net/svnroot/vulashaka
//
//  Author : Alexey PETROV


//---------------------------------------------------------------------------
#ifndef tmp_volSphericalTensorField_cpp
#define tmp_volSphericalTensorField_cpp


//---------------------------------------------------------------------------
%{
  #include "src/OpenFOAM/fields/tmp/tmp_volSphericalTensorField.hh"
%}


//---------------------------------------------------------------------------
%import "src/OpenFOAM/fields/Fields/primitiveFields.cxx"

%include "src/OpenFOAM/fields/GeometricFields/GeometricField_sphericalTensor_fvPatchField_volMesh.cpp"


//---------------------------------------------------------------------------
%template( tmp_volSphericalTensorField ) Foam::tmp< Foam::GeometricField< Foam::sphericalTensor, Foam::fvPatchField, Foam::volMesh > >;


//----------------------------------------------------------------------------
%feature( "pythonappend" ) Foam::tmp< Foam::GeometricField< Foam::sphericalTensor, Foam::fvPatchField, Foam::volMesh > >::SMARTPTR_PYAPPEND_GETATTR( tmp_volSphericalTensorField );

%extend Foam::tmp< Foam::GeometricField< Foam::sphericalTensor, Foam::fvPatchField, Foam::volMesh > >
{
  SMARTPTR_EXTEND_ATTR( tmp_volSphericalTensorField );
  SMARTPTR_EXTEND_OPERATOR_EQ( Foam::sphericalTensor );
}


//---------------------------------------------------------------------------
#endif

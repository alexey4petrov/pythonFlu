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
#ifndef FieldField_fvPatchField_sphericalTensor_cpp
#define FieldField_fvPatchField_sphericalTensor_cpp


//---------------------------------------------------------------------------
%{
  #include "src/OpenFOAM/fields/FieldFields/FieldField_fvPatchField_sphericalTensor.hh"
%}


//---------------------------------------------------------------------------
%include "src/OpenFOAM/fields/FieldFields/FieldField.cpp"

%import "src/OpenFOAM/containers/Lists/PtrList/PtrList_sphericalTensorField.cxx"

%include "src/finiteVolume/fields/fvPatchFields/fvPatchField_sphericalTensor.cpp"

%ignore Foam::FieldField< Foam::fvPatchField, Foam::sphericalTensor >::FieldField;

%template( FieldField_fvPatchField_sphericalTensor ) Foam::FieldField< Foam::fvPatchField, Foam::sphericalTensor >;


//---------------------------------------------------------------------------
%feature( "pythonappend" ) Foam::FieldField< Foam::fvPatchField, Foam::sphericalTensor >::REDIRECT2BASE_PYAPPEND_GETATTR( FieldField_fvPatchField_sphericalTensor );

%extend Foam::FieldField< Foam::fvPatchField, Foam::sphericalTensor >
{
  REDIRECT2BASE_EXTEND_ATTR( FieldField_fvPatchField_sphericalTensor )
}

FIELDFIELD_TEMPLATE_FUNC( Foam::fvPatchField, Foam::sphericalTensor );


//---------------------------------------------------------------------------
#endif
    

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
#ifndef FieldField_fvPatchField_scalar_cxx
#define FieldField_fvPatchField_scalar_cxx


//---------------------------------------------------------------------------
// Keep on corresponding "director" includes at the top of SWIG defintion file

%include "src/OpenFOAM/directors.hxx"

%include "src/finiteVolume/directors.hxx"


//---------------------------------------------------------------------------
%include "src/OpenFOAM/fields/FieldFields/FieldField.cxx"

%include "src/finiteVolume/fields/fvPatchFields/fvPatchField_scalar.cxx"

%include "src/OpenFOAM/containers/Lists/PtrList/PtrList_fvPatchField_scalar.cxx"

NO_TMP_TYPEMAP_FIELDFIELD(  Foam::fvPatchField, Foam::scalar )

%ignore Foam::FieldField< Foam::fvPatchField, Foam::scalar >::FieldField;
%ignore Foam::FieldField< Foam::fvPatchField, Foam::scalar >::T;

%inline
%{
    typedef Foam::FieldField< Foam::fvPatchField, Foam::scalar > FieldField_fvPatchField_scalar;
%}

%template( FieldField_fvPatchField_scalar ) Foam::FieldField< Foam::fvPatchField, Foam::scalar >;


//---------------------------------------------------------------------------
%feature( "pythonappend" ) Foam::FieldField< Foam::fvPatchField, Foam::scalar >::REDIRECT2BASE_PYAPPEND_GETATTR( FieldField_fvPatchField_scalar );

%extend Foam::FieldField< Foam::fvPatchField, Foam::scalar >
{
    REDIRECT2BASE_EXTEND_ATTR( FieldField_fvPatchField_scalar )
}
FIELDFIELD_TEMPLATE_FUNC( Foam::fvPatchField, Foam::scalar );


//---------------------------------------------------------------------------
#endif
    

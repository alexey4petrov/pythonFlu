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
#ifndef FieldField_fvPatchField_vector_cxx
#define FieldField_fvPatchField_vector_cxx


//---------------------------------------------------------------------------
// Keep on corresponding "director" includes at the top of SWIG defintion file

%include "src/OpenFOAM/directors.hxx"

%include "src/finiteVolume/directors.hxx"


//---------------------------------------------------------------------------
%include "src/OpenFOAM/fields/FieldFields/FieldField.cxx"

%include "src/finiteVolume/fields/fvPatchFields/fvPatchField_vector.cxx"

%include "src/OpenFOAM/containers/Lists/PtrList/PtrList_fvPatchField_vector.cxx"

NO_TMP_TYPEMAP_FIELDFIELD( Foam::fvPatchField, Foam::Vector<Foam::scalar> )

%ignore Foam::FieldField< Foam::fvPatchField, Foam::vector >::FieldField;
%ignore Foam::FieldField< Foam::fvPatchField, Foam::vector >::T;
%ignore Foam::FieldField< Foam::fvPatchField, Foam::vector >::replace;

%template( FieldField_fvPatchField_vector ) Foam::FieldField< Foam::fvPatchField, Foam::vector >;

%inline
%{
    typedef Foam::FieldField< Foam::fvPatchField, Foam::vector > FieldField_fvPatchField_vector;
%}


//---------------------------------------------------------------------------
%feature( "pythonappend" ) Foam::FieldField< Foam::fvPatchField, Foam::vector >::REDIRECT2BASE_PYAPPEND_GETATTR( FieldField_fvPatchField_vector );

%extend Foam::FieldField< Foam::fvPatchField, Foam::vector >
{
    REDIRECT2BASE_EXTEND_ATTR( FieldField_fvPatchField_vector )
}

FIELDFIELD_TEMPLATE_FUNC( Foam::fvPatchField, Foam::vector );


//---------------------------------------------------------------------------
#endif

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
#ifndef fvPatchField_vector_cxx
#define fvPatchField_vector_cxx

//---------------------------------------------------------------------------
// Keep on corresponding "director" includes at the top of SWIG defintion file

%include "src/OpenFOAM/directors.hxx"

%include "src/finiteVolume/directors.hxx"


//---------------------------------------------------------------------------
%include "src/OpenFOAM/fields/Fields/vectorField.cxx"

%include "src/finiteVolume/fields/fvPatchFields/fvPatchField.cxx"

%ignore Foam::fvPatchField< Foam::vector >::typeName;
%ignore Foam::fvPatchField< Foam::vector >::debug;
%ignore Foam::fvPatchField< Foam::vector >::snGrad;


//--------------------------------------------------------------------------
#if ( __FOAM_VERSION__ >= 010500 )

%ignore Foam::fvPatchField< Foam::vector >::disallowGenericFvPatchField;

#else

%ignore Foam::fvPatchField< Foam::vector >::disallowDefaultFvPatchField;

#endif


//---------------------------------------------------------------------------
FVPATCHFIELD_ADDONS( vector );

%template( fvPatchField_vector ) Foam::fvPatchField< Foam::vector >;

%inline
{
  namespace Foam 
  {
    typedef fvPatchField< vector > fvPatchVectorField;
  }
}



//---------------------------------------------------------------------------
#endif

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
#ifndef fixedGradientFvPatchField_vector_cxx
#define fixedGradientFvPatchField_vector_cxx


//---------------------------------------------------------------------------
// Keep on corresponding "director" includes at the top of SWIG defintion file

%include "src/OpenFOAM/directors.hxx"

%include "src/finiteVolume/directors.hxx"


//---------------------------------------------------------------------------
%include "src/OpenFOAM/fields/Fields/scalarField.cxx"

%include "src/finiteVolume/fields/fvPatchFields/fvPatchField_vector.cxx"


%include "src/finiteVolume/fields/fvPatchFields/basic/fixedGradient/fixedGradientFvPatchField.cxx"


%feature( "director" ) fixedGradientFvPatchVectorField;

%inline
{
  namespace Foam 
  {
    typedef fixedGradientFvPatchField< vector > fixedGradientFvPatchVectorField;
  }
}


//---------------------------------------------------------------------------
%ignore Foam::fixedGradientFvPatchField< Foam::vector >::snGrad;

DIRECTOR_PRE_EXTENDS( fixedGradientFvPatchVectorField );


//---------------------------------------------------------------------------
%template( fixedGradientFvPatchVectorField ) Foam::fixedGradientFvPatchField< Foam::vector >;


//---------------------------------------------------------------------------
%include "src/OpenFOAM/db/objectRegistry.cxx"

%extend Foam::fixedGradientFvPatchField< Foam::vector >
{
  DIRECTOR_EXTENDS( fixedGradientFvPatchVectorField );
  TYPEINFO_DIRECTOR_EXTENDS( fvPatchVectorField, fixedGradientFvPatchVectorField );
  COMMON_FIXEDGRADIENT_FVPATCHFIELD_TEMPLATE_FUNC_EXTENDS( Foam::vector );
}


//---------------------------------------------------------------------------
#endif

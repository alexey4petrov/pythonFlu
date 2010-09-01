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
#ifndef fixedGradientFvPatchField_scalar_cxx
#define fixedGradientFvPatchField_scalar_cxx


//---------------------------------------------------------------------------
// Keep on corresponding "director" includes at the top of SWIG defintion file

%include "src/OpenFOAM/directors.hxx"

%include "src/finiteVolume/directors.hxx"


//---------------------------------------------------------------------------
%include "src/OpenFOAM/fields/Fields/scalarField.cxx"

%include "src/finiteVolume/fields/fvPatchFields/fvPatchField_scalar.cxx"

%include "src/finiteVolume/fields/fvPatchFields/basic/fixedGradient/fixedGradientFvPatchField.cxx"

%feature( "director" ) fixedGradientFvPatchScalarField;

%inline
{
  namespace Foam 
  {
    typedef fixedGradientFvPatchField< scalar > fixedGradientFvPatchScalarField;
  }
}


//---------------------------------------------------------------------------
%ignore Foam::fixedGradientFvPatchField< Foam::scalar >::snGrad;
%ignore Foam::fixedGradientFvPatchField< Foam::scalar >::gradientBoundaryCoeffs;

DIRECTOR_PRE_EXTENDS( fixedGradientFvPatchScalarField );


//---------------------------------------------------------------------------
%template( fixedGradientFvPatchScalarField ) Foam::fixedGradientFvPatchField< Foam::scalar >;


//---------------------------------------------------------------------------
%include "src/OpenFOAM/db/objectRegistry.cxx"

%extend Foam::fixedGradientFvPatchField< Foam::scalar >
{
  DIRECTOR_EXTENDS( fixedGradientFvPatchScalarField );
  TYPEINFO_DIRECTOR_EXTENDS( fvPatchScalarField, fixedGradientFvPatchScalarField );
  COMMON_FIXEDGRADIENT_FVPATCHFIELD_TEMPLATE_FUNC_EXTENDS( Foam::scalar );
}


//---------------------------------------------------------------------------
#endif

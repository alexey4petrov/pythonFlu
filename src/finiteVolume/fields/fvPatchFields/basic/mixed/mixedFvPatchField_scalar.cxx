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
#ifndef mixedfvPatchScalarField_cxx
#define mixedfvPatchScalarField_cxx


//---------------------------------------------------------------------------
%include "src/finiteVolume/fields/fvPatchFields/fvPatchField_scalar.cxx"

%include "src/finiteVolume/fields/fvPatchFields/basic/mixed/mixedFvPatchField.cxx"


%feature( "director" ) mixedFvPatchScalarField;

%inline
{
  namespace Foam 
  {
    typedef mixedFvPatchField< scalar > mixedFvPatchScalarField;
  }
}


//---------------------------------------------------------------------------
DIRECTOR_PRE_EXTENDS( mixedFvPatchScalarField );


//---------------------------------------------------------------------------
%template( mixedFvPatchScalarField ) Foam::mixedFvPatchField< Foam::scalar >;


//---------------------------------------------------------------------------
%include "src/OpenFOAM/db/objectRegistry.cxx"

%extend Foam::mixedFvPatchField< Foam::scalar >
{
  DIRECTOR_EXTENDS( mixedFvPatchScalarField );
  TYPEINFO_DIRECTOR_EXTENDS( fvPatchScalarField, mixedFvPatchScalarField );
  MIXEDFVPATCHFIELD_TEMPLATE_Func( scalar );
}


//---------------------------------------------------------------------------
#endif

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
#ifndef autoPtr_volScalarField_cxx
#define autoPtr_volScalarField_cxx


//---------------------------------------------------------------------------
//It is necessary to include "director's" classes above first's DIRECTOR_INCLUDE
%include "src/finiteVolume/directors.hxx"


//---------------------------------------------------------------------------
%include "src/OpenFOAM/fields/tmp/autoPtr.cxx"

%include "src/OpenFOAM/fields/GeometricFields/GeometricField_scalar_fvPatchField_volMesh.cxx"

AUTOPTR_TYPEMAP( Foam::volScalarField )

%template( autoPtr_volScalarField ) Foam::autoPtr< Foam::volScalarField >;

%extend Foam::autoPtr< Foam::volScalarField >
{
    bool operator==( const Foam::UList< Foam::scalar >& theArg )
    {
        Foam::UList< Foam::scalar >* aSelf = static_cast< Foam::UList< Foam::scalar >* >( self->ptr() );
        return *aSelf == theArg;
    }
}

%inline
{
    namespace Foam
    {
        typedef autoPtr< volScalarField > autoPtr_volScalarField;
    }
}


//---------------------------------------------------------------------------
#endif

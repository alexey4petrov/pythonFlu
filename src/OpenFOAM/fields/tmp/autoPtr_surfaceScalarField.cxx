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
#ifndef autoPtr_surfaceScalarField_cxx
#define autoPtr_surfaceScalarField_cxx


//---------------------------------------------------------------------------
%include "src/OpenFOAM/fields/tmp/autoPtr.cxx"

%include "src/OpenFOAM/fields/GeometricFields/GeometricField_scalar_fvsPatchField_surfaceMesh.cxx"

AUTOPTR_TYPEMAP( Foam::surfaceScalarField )

%extend Foam::autoPtr< Foam::surfaceScalarField >
{
    bool operator==( const Foam::UList< Foam::scalar >& theArg )
    {
        Foam::UList< Foam::scalar >* aSelf = static_cast< Foam::UList< Foam::scalar >* >( self->ptr() );
        return *aSelf == theArg;
    }
}

%template( autoPtr_surfaceScalarField ) Foam::autoPtr< Foam::surfaceScalarField >;

%inline
{
    namespace Foam
    {
        typedef autoPtr< surfaceScalarField > autoPtr_surfaceScalarField;
    }
}


//---------------------------------------------------------------------------
#endif

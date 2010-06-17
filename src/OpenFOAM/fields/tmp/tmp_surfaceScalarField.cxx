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
#ifndef tmp_surfaceScalarField_cxx
#define tmp_surfaceScalarField_cxx


//---------------------------------------------------------------------------
// Keep on corresponding "director" includes at the top of SWIG defintion file

%include "src/OpenFOAM/directors.hxx"

%include "src/finiteVolume/directors.hxx"


//---------------------------------------------------------------------------
%include "src/OpenFOAM/fields/tmp/tmp_scalarField.cxx"

%include "src/OpenFOAM/fields/GeometricFields/GeometricField_scalar_fvsPatchField_surfaceMesh.cxx"


//---------------------------------------------------------------------------
%template( tmp_surfaceScalarField ) Foam::tmp< Foam::GeometricField< Foam::scalar, Foam::fvsPatchField, Foam::surfaceMesh > >;

%inline
{
    namespace Foam
    {
        typedef tmp< GeometricField< scalar, fvsPatchField, surfaceMesh > > tmp_surfaceScalarField;
    }
}


//----------------------------------------------------------------------------
%feature( "pythonappend" ) Foam::tmp< Foam::GeometricField< Foam::scalar, Foam::fvsPatchField, Foam::surfaceMesh > >::SMARTPTR_PYAPPEND_GETATTR( tmp_surfaceScalarField );

%extend Foam::tmp< Foam::GeometricField< Foam::scalar, Foam::fvsPatchField, Foam::surfaceMesh > >
{
    SMARTPTR_EXTEND_ATTR( tmp_surfaceScalarField )
    
    bool operator==( const Foam::UList< Foam::scalar >& theArg )
    {
        Foam::UList< Foam::scalar >* aSelf = static_cast< Foam::UList< Foam::scalar >* >( self->ptr() );
        return *aSelf == theArg;
    }
}

//---------------------------------------------------------------------------
#endif

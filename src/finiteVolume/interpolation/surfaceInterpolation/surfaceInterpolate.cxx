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
#ifndef surfaceInterpolate_cxx
#define surfaceInterpolate_cxx


//---------------------------------------------------------------------------
// Keep on corresponding "director" includes at the top of SWIG defintion file

%include "src/OpenFOAM/directors.hxx"

%include "src/finiteVolume/directors.hxx"


//---------------------------------------------------------------------------
%include "src/finiteVolume/fields/volFields/volFields.cxx"

%include "src/finiteVolume/fields/surfaceFields/surfaceFields.cxx"



%{
    #include "surfaceInterpolate.H"
%}

%include "surfaceInterpolate.H"


//---------------------------------------------------------------------------
%define FVC_INTERPOLATE_TEMPLATE_FUNC( Type )
%{
    Foam::tmp< Foam::GeometricField< Type, Foam::fvsPatchField, Foam::surfaceMesh > > interpolate
    (
        const Foam::GeometricField< Type, Foam::fvPatchField, Foam::volMesh >& vf
    )
    {
        return Foam::fvc::interpolate( vf );
    }

    Foam::tmp< GeometricField< Type, Foam::fvsPatchField, Foam::surfaceMesh> > interpolate
    (
        const Foam::GeometricField<Type, Foam::fvPatchField, Foam::volMesh>& tvf,
        const Foam::word& name
    )
    {
        return Foam::fvc::interpolate( tvf, name );
    }

    Foam::tmp< GeometricField< Type, Foam::fvsPatchField, Foam::surfaceMesh> > interpolate
    (
        const Foam::GeometricField<Type, Foam::fvPatchField, Foam::volMesh>& tvf,
        const Foam::surfaceScalarField& faceFlux,
        const Foam::word& name
    )
    {
        return Foam::fvc::interpolate( tvf, faceFlux, name );
    }
    
%}
%enddef


//---------------------------------------------------------------------------
%inline FVC_INTERPOLATE_TEMPLATE_FUNC( Foam::vector )

%inline FVC_INTERPOLATE_TEMPLATE_FUNC( Foam::scalar )

%inline FVC_INTERPOLATE_TEMPLATE_FUNC( Foam::tensor )


//---------------------------------------------------------------------------
#endif

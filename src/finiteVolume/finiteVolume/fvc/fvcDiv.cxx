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
#ifndef fvcDiv_cxx
#define fvcDiv_cxx


//---------------------------------------------------------------------------
// Keep on corresponding "director" includes at the top of SWIG defintion file

%include "src/OpenFOAM/directors.hxx"

%include "src/finiteVolume/directors.hxx"


//---------------------------------------------------------------------------
%include "src/finiteVolume/fields/volFields/volFields.cxx"

%include "src/finiteVolume/fields/surfaceFields/surfaceFields.cxx"

%{
    #include "fvcDiv.H"
%}


//---------------------------------------------------------------------------
%include "src/OpenFOAM/fields/tmp/tmp_volScalarField.cxx"
%include "src/OpenFOAM/fields/tmp/tmp_volVectorField.cxx"
%include "src/OpenFOAM/fields/tmp/tmp_volTensorField.cxx"

%include "src/OpenFOAM/fields/tmp/tmp_surfaceScalarField.cxx"
%include "src/OpenFOAM/fields/tmp/tmp_surfaceVectorField.cxx"


//---------------------------------------------------------------------------
%define FVC_DIV_TEMPLATE_FUNC( Type )
%{
    Foam::tmp< Foam::GeometricField< Type, Foam::fvPatchField, Foam::volMesh > > fvc_div
    (
     const Foam::GeometricField< Type, Foam::fvsPatchField, Foam::surfaceMesh >& ssf
    )
    {
        return Foam::fvc::div( ssf );
    }
    
    Foam::tmp< Foam::GeometricField< Type, Foam::fvPatchField, Foam::volMesh > > fvc_div
    (
     const Foam::surfaceScalarField& flux,
     const Foam::GeometricField< Type, Foam::fvPatchField, Foam::volMesh >& vf
    )
    {
        return Foam::fvc::div( flux, vf );
    }
    
    Foam::tmp< Foam::GeometricField< Type, Foam::fvPatchField, Foam::volMesh > > fvc_div
    (
     const Foam::surfaceScalarField& flux,
     const Foam::GeometricField< Type, Foam::fvPatchField, Foam::volMesh >& vf,
     const Foam::word& name
    )
    {
        return Foam::fvc::div( flux, vf, name );
    }
%}
%enddef


//---------------------------------------------------------------------------
%inline FVC_DIV_TEMPLATE_FUNC( Foam::scalar )

%inline FVC_DIV_TEMPLATE_FUNC( Foam::vector )

%inline FVC_DIV_TEMPLATE_FUNC( Foam::tensor )


//---------------------------------------------------------------------------
%inline 
%{
  Foam::tmp< Foam::GeometricField< Foam::vector, Foam::fvPatchField, Foam::volMesh > > fvc_div
    (
     const Foam::GeometricField< Foam::tensor, Foam::fvPatchField, Foam::volMesh >& ssf,
     const Foam::word& name
    )
    {
        return Foam::fvc::div( ssf, name );
    }
    Foam::tmp< Foam::GeometricField< Foam::vector, Foam::fvPatchField, Foam::volMesh > > fvc_div
    (
     const Foam::GeometricField< Foam::tensor, Foam::fvPatchField, Foam::volMesh >& vf
    )
    {
        return Foam::fvc::div( vf );
    }
  
%}


//---------------------------------------------------------------------------
%include "fvcDiv.H"


//---------------------------------------------------------------------------
#endif

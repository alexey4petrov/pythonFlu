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
#ifndef fvcGrad_cxx
#define fvcGrad_cxx


//---------------------------------------------------------------------------
// Keep on corresponding "director" includes at the top of SWIG defintion file

%include "src/OpenFOAM/directors.hxx"

%include "src/finiteVolume/directors.hxx"


//---------------------------------------------------------------------------
%{
    #include "Field.H"

    #include "fvcGrad.H"
%}


//---------------------------------------------------------------------------
%include "src/OpenFOAM/fields/tmp/tmp_volVectorField.cxx"
%include "src/finiteVolume/fields/surfaceFields/surfaceScalarField.cxx"

%inline
{
    Foam::tmp< Foam::GeometricField< Foam::vector, Foam::fvPatchField, Foam::volMesh > > fvc_grad
    ( 
        const Foam::GeometricField< Foam::scalar, Foam::fvsPatchField, Foam::surfaceMesh >& vf 
    )
    {
        return Foam::fvc::grad( vf );
    }
}


//---------------------------------------------------------------------------
%include "src/OpenFOAM/fields/tmp/tmp_volScalarField.cxx"
%include "src/finiteVolume/fields/volFields/volScalarField.cxx"
%include "src/OpenFOAM/fields/tmp/tmp_volTensorField.cxx"

%inline
%{
    Foam::tmp< Foam::GeometricField< Foam::vector, Foam::fvPatchField, Foam::volMesh > > fvc_grad
    ( 
        const Foam::GeometricField< Foam::scalar, Foam::fvPatchField, Foam::volMesh >& vf 
    )
    {
        return Foam::fvc::grad( vf );
    }
    Foam::tmp< Foam::GeometricField< Foam::tensor, Foam::fvPatchField, Foam::volMesh > > fvc_grad
    ( 
        const Foam::GeometricField< Foam::vector, Foam::fvPatchField, Foam::volMesh >& vf 
    )
    {
        return Foam::fvc::grad( vf );
    }
%}


//---------------------------------------------------------------------------
%include "src/finiteVolume/surfaceMesh.cxx"

%include "src/finiteVolume/volMesh.cxx"


//---------------------------------------------------------------------------
%include "fvcGrad.H"


//---------------------------------------------------------------------------
#endif

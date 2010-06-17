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
#ifndef fvmLaplacian_cxx
#define fvmLaplacian_cxx


//---------------------------------------------------------------------------
// Keep on corresponding "director" includes at the top of SWIG defintion file

%include "src/OpenFOAM/directors.hxx"

%include "src/finiteVolume/directors.hxx"


//---------------------------------------------------------------------------
%include "src/finiteVolume/fields/fvPatchFields/fvPatchField.cxx"

%{
    #include "fvmLaplacian.H"
%}


//---------------------------------------------------------------------------
%include "src/finiteVolume/fields/volFields/volScalarField.cxx"
%include "src/finiteVolume/fields/volFields/volTensorField.cxx"
%include "src/OpenFOAM/dimensionedTypes/dimensionedScalar.cxx"

%include "src/finiteVolume/fields/surfaceFields/surfaceScalarField.cxx"
%include "src/OpenFOAM/fields/tmp/tmp_surfaceScalarField.cxx"


//---------------------------------------------------------------------------
%define FVM_LAPLACIAN_TEMPLATE_FUNC( Type )
%{
    Foam::tmp< Foam::fvMatrix< Type > > fvm_laplacian
    (
        Foam::GeometricField<Type, Foam::fvPatchField, Foam::volMesh>& vf,
        const Foam::word& name
    )
    {
        return Foam::fvm::laplacian( vf, name );
    }

    Foam::tmp< Foam::fvMatrix< Type > > fvm_laplacian
    (
        Foam::GeometricField<Type, Foam::fvPatchField, Foam::volMesh>& vf
    )
    {
        return Foam::fvm::laplacian( vf );
    }

    Foam::tmp< Foam::fvMatrix< Type > > fvm_laplacian
    (
        const Foam::dimensionedScalar& gamma,
        Foam::GeometricField<Type, Foam::fvPatchField, Foam::volMesh>& vf,
        const Foam::word& name
    )
    {
        return Foam::fvm::laplacian( gamma, vf, name );
    }

    Foam::tmp< Foam::fvMatrix< Type > > fvm_laplacian
    (
        const Foam::dimensionedScalar& gamma,
        Foam::GeometricField<Type, Foam::fvPatchField, Foam::volMesh>& vf
    )
    {
        return Foam::fvm::laplacian( gamma, vf );
    }

    Foam::tmp< Foam::fvMatrix< Type > > fvm_laplacian
    (
        const Foam::volScalarField& gamma,
        Foam::GeometricField<Type, Foam::fvPatchField, Foam::volMesh>& vf,
        const Foam::word& name
    )
    {
        return Foam::fvm::laplacian( gamma, vf, name );
    }

    Foam::tmp< Foam::fvMatrix< Type > > fvm_laplacian
    (
        const Foam::volScalarField& gamma,
        Foam::GeometricField<Type, Foam::fvPatchField, Foam::volMesh>& vf
    )
    {
        return Foam::fvm::laplacian( gamma, vf );
    }

    Foam::tmp< Foam::fvMatrix< Type > > fvm_laplacian
    (
        const Foam::volTensorField& tgamma,
        Foam::GeometricField<Type, Foam::fvPatchField, Foam::volMesh>& vf
    )
    {
        return Foam::fvm::laplacian( tgamma, vf );
    }

    Foam::tmp< Foam::fvMatrix< Type > > fvm_laplacian
    (
        const Foam::surfaceScalarField& gamma,
        Foam::GeometricField<Type, Foam::fvPatchField, Foam::volMesh>& vf,
        const Foam::word& name
    )
    {
        return Foam::fvm::laplacian( gamma, vf, name );
    }

    Foam::tmp< Foam::fvMatrix< Type > > fvm_laplacian
    (
        const Foam::surfaceScalarField& gamma,
        Foam::GeometricField<Type, Foam::fvPatchField, Foam::volMesh>& vf
    )
    {
        return Foam::fvm::laplacian( gamma, vf );
    }

%}
%enddef


//---------------------------------------------------------------------------
%include "src/OpenFOAM/fields/GeometricFields/GeometricField_scalar_fvPatchField_volMesh.cxx"
%include "src/OpenFOAM/fields/tmp/tmp_fvScalarMatrix.cxx"

%inline FVM_LAPLACIAN_TEMPLATE_FUNC( Foam::scalar )


//---------------------------------------------------------------------------
%include "src/OpenFOAM/fields/tmp/tmp_fvVectorMatrix.cxx"
%include "src/OpenFOAM/fields/GeometricFields/GeometricField_vector_fvPatchField_volMesh.cxx"

%inline FVM_LAPLACIAN_TEMPLATE_FUNC( Foam::vector )


//---------------------------------------------------------------------------
%include "src/finiteVolume/volMesh.cxx"


//---------------------------------------------------------------------------
%include "fvmLaplacian.H"


//---------------------------------------------------------------------------
#endif

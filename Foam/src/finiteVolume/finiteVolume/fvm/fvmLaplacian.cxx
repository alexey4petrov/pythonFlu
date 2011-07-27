//  pythonFlu - Python wrapping for OpenFOAM C++ API
//  Copyright (C) 2010- Alexey Petrov
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
//  See http://sourceforge.net/projects/pythonflu
//
//  Author : Alexey PETROV


//---------------------------------------------------------------------------
#ifndef fvmLaplacian_cxx
#define fvmLaplacian_cxx


//---------------------------------------------------------------------------
%module "Foam.src.finiteVolume.finiteVolume.fvm.fvmLaplacian";
%{
  #include "Foam/src/finiteVolume/finiteVolume/fvm/fvmLaplacian.hh"
%}


//---------------------------------------------------------------------------
%import "Foam/src/finiteVolume/fvMesh/fvMeshes.cxx"

%import "Foam/src/finiteVolume/fvMatrices/fvMatrices.cxx"

%import "Foam/src/OpenFOAM/dimensionedTypes/dimensionedScalar.cxx"

%import "Foam/src/OpenFOAM/fields/GeometricFields/geometricOneField.cxx"


//---------------------------------------------------------------------------
%define FVM_LAPLACIAN_TEMPLATE_1_FUNC( Type )
%{
  Foam::tmp< Foam::fvMatrix< Type > > fvm_laplacian( Foam::GeometricField< Type, Foam::fvPatchField, Foam::volMesh >& vf,
                                                     const Foam::word& name )
  {
    return Foam::fvm::laplacian( vf, name );
  }

  Foam::tmp< Foam::fvMatrix< Type > > fvm_laplacian( Foam::GeometricField< Type, Foam::fvPatchField, Foam::volMesh >& vf )
  {
    return Foam::fvm::laplacian( vf );
  }
#if FOAM_REF_VERSION( >, 010600 ) || FOAM_BRANCH_VERSION( __OPENFOAM_EXT__, >, 010500 )
  Foam::tmp< Foam::fvMatrix< Type > > fvm_laplacian( const geometricOneField &,
                                                     Foam::GeometricField< Type, Foam::fvPatchField, Foam::volMesh >& vf,
                                                     const Foam::word& name )
  {
    return Foam::fvm::laplacian( vf, name );
  }
  
  Foam::tmp< Foam::fvMatrix< Type > > fvm_laplacian( const geometricOneField &,
                                                     Foam::GeometricField< Type, Foam::fvPatchField, Foam::volMesh >& vf )
  {
    return Foam::fvm::laplacian( vf );
  }
#endif
%}
%enddef


//---------------------------------------------------------------------------
%inline FVM_LAPLACIAN_TEMPLATE_1_FUNC( Foam::scalar );
%inline FVM_LAPLACIAN_TEMPLATE_1_FUNC( Foam::vector );


//---------------------------------------------------------------------------
%define FVM_LAPLACIAN_TEMPLATE_2_FUNC( Type, GType )
%{
  Foam::tmp< Foam::fvMatrix< Type > > fvm_laplacian( const Foam::dimensioned< GType >& gamma,
                                                     Foam::GeometricField< Type, Foam::fvPatchField, Foam::volMesh >& vf,
                                                     const Foam::word& name )
  {
    return Foam::fvm::laplacian( gamma, vf, name );
  }

  Foam::tmp< Foam::fvMatrix< Type > > fvm_laplacian( const Foam::dimensioned< GType >& gamma,
                                                     Foam::GeometricField< Type, Foam::fvPatchField, Foam::volMesh >& vf )
  {
    return Foam::fvm::laplacian( gamma, vf );
  }

  Foam::tmp< Foam::fvMatrix< Type > > fvm_laplacian( const Foam::GeometricField< GType, Foam::fvPatchField, Foam::volMesh >& gamma,
                                                     Foam::GeometricField< Type, Foam::fvPatchField, Foam::volMesh >& vf,
                                                     const Foam::word& name )
  {
    return Foam::fvm::laplacian( gamma, vf, name );
  }

  Foam::tmp< Foam::fvMatrix< Type > > fvm_laplacian( const Foam::GeometricField< GType, Foam::fvPatchField, Foam::volMesh >& gamma,
                                                     Foam::GeometricField< Type, Foam::fvPatchField, Foam::volMesh >& vf )
  {
    return Foam::fvm::laplacian( gamma, vf );
  }

  Foam::tmp< Foam::fvMatrix< Type > > fvm_laplacian( const Foam::GeometricField< GType, Foam::fvsPatchField, Foam::surfaceMesh >& gamma,
                                                     Foam::GeometricField< Type, Foam::fvPatchField, Foam::volMesh >& vf,
                                                     const Foam::word& name )
  {
    return Foam::fvm::laplacian( gamma, vf, name );
  }

  Foam::tmp< Foam::fvMatrix< Type > > fvm_laplacian( const Foam::GeometricField< GType, Foam::fvsPatchField, Foam::surfaceMesh >& gamma,
                                                     Foam::GeometricField< Type, Foam::fvPatchField, Foam::volMesh >& vf )
  {
    return Foam::fvm::laplacian( gamma, vf );
  }
%}
%enddef

//---------------------------------------------------------------------------
%inline FVM_LAPLACIAN_TEMPLATE_2_FUNC( Foam::scalar, Foam::scalar );

%inline FVM_LAPLACIAN_TEMPLATE_2_FUNC( Foam::vector, Foam::scalar );

#if FOAM_VERSION( >=, 010500 )
%inline FVM_LAPLACIAN_TEMPLATE_2_FUNC( Foam::scalar, Foam::tensor );
%inline FVM_LAPLACIAN_TEMPLATE_2_FUNC( Foam::scalar, Foam::symmTensor );
%inline FVM_LAPLACIAN_TEMPLATE_2_FUNC( Foam::vector, Foam::tensor );
%inline FVM_LAPLACIAN_TEMPLATE_2_FUNC( Foam::vector, Foam::symmTensor );
#endif


//---------------------------------------------------------------------------
%include <fvmLaplacian.H>


//---------------------------------------------------------------------------
#endif

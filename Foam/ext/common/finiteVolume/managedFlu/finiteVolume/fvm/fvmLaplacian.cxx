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
//  Author : Alexey PETROV, Andrey SIMURZIN


//---------------------------------------------------------------------------
#ifndef fvmLaplacian_cxx
#define fvmLaplacian_cxx


//---------------------------------------------------------------------------
%module "Foam.ext.common.finiteVolume.managedFlu.fvch"

%{
  #include "Foam/ext/common/finiteVolume/managedFlu/finiteVolume/fvm/fvmLaplacian.hh"
%}


//---------------------------------------------------------------------------
%import "Foam/src/finiteVolume/fvMesh/fvMeshes.cxx"


//---------------------------------------------------------------------------
INCLUDE_FILENAME(fvmLaplacian,hpp)


//---------------------------------------------------------------------------
%define FVM_LAPLACIAN_TEMPLATE_2_FUNC( Type, GType )
%{
  Foam::fvMatrixHolder< Type > fvm_laplacian( const Foam::dimensioned< GType >& gamma,
                                              const Foam::GeometricFieldHolder< Type, Foam::fvPatchField, Foam::volMesh >& vf,
                                              const Foam::word& name )
  {
    return Foam::fvm::laplacian( gamma, vf, name );
  }

  Foam::fvMatrixHolder< Type > fvm_laplacian( const Foam::dimensioned< GType >& gamma,
                                              const Foam::GeometricFieldHolder< Type, Foam::fvPatchField, Foam::volMesh >& vf )
  {
    return Foam::fvm::laplacian( gamma, vf );
  }

  Foam::fvMatrixHolder< Type > fvm_laplacian( const Foam::GeometricFieldHolder< GType, Foam::fvPatchField, Foam::volMesh >& gamma,
                                              const Foam::GeometricFieldHolder< Type, Foam::fvPatchField, Foam::volMesh >& vf,
                                              const Foam::word& name )
  {
    return Foam::fvm::laplacian( gamma, vf, name );
  }

  Foam::fvMatrixHolder< Type > fvm_laplacian( const Foam::GeometricFieldHolder< GType, Foam::fvPatchField, Foam::volMesh >& gamma,
                                              const Foam::GeometricFieldHolder< Type, Foam::fvPatchField, Foam::volMesh >& vf )
  {
    return Foam::fvm::laplacian( gamma, vf );
  }

  Foam::fvMatrixHolder< Type > fvm_laplacian( const Foam::GeometricFieldHolder< GType, Foam::fvsPatchField, Foam::surfaceMesh >& gamma,
                                              const Foam::GeometricFieldHolder< Type, Foam::fvPatchField, Foam::volMesh >& vf,
                                              const Foam::word& name )
  {
    return Foam::fvm::laplacian( gamma, vf, name );
  }

  Foam::fvMatrixHolder< Type > fvm_laplacian( const Foam::GeometricFieldHolder< GType, Foam::fvsPatchField, Foam::surfaceMesh >& gamma,
                                              const Foam::GeometricFieldHolder< Type, Foam::fvPatchField, Foam::volMesh >& vf )
  {
    return Foam::fvm::laplacian( gamma, vf );
  }
%}
%enddef


//--------------------------------------------------------------------------------------
%inline FVM_LAPLACIAN_TEMPLATE_2_FUNC( Foam::scalar, Foam::scalar );

%inline FVM_LAPLACIAN_TEMPLATE_2_FUNC( Foam::vector, Foam::scalar );


//--------------------------------------------------------------------------------------
#endif

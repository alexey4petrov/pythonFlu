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
#ifndef fvmDdt_cxx
#define fvmDdt_cxx


//---------------------------------------------------------------------------
%module "Foam.ext.common.finiteVolume.managedFlu.finiteVolume.fvm.fvmDdt"

%{
  #include "Foam/ext/common/finiteVolume/managedFlu/finiteVolume/fvm/fvmDdt.hh"
%}


//---------------------------------------------------------------------------
%import "Foam/src/finiteVolume/fvMesh/fvMeshes.cxx"

%import "Foam/src/finiteVolume/fvMatrices/fvMatrices.cxx"


//---------------------------------------------------------------------------
INCLUDE_FILENAME(fvmDdt,hpp)


//---------------------------------------------------------------------------
%define FVMHOLDER_DDT_TEMPLATE_FUNC_020000( Type )
%{

  Foam::fvMatrixHolder< Type > fvm_ddt( const Foam::volScalarFieldHolder& field1,
                                        const Foam::GeometricFieldHolder< Type, Foam::fvPatchField, Foam::volMesh >& field2 )
  {
    return Foam::fvm::ddt( field1, field2 );
  }

  Foam::fvMatrixHolder< Type > fvm_ddt( const Foam::GeometricFieldHolder< Type, Foam::fvPatchField, Foam::volMesh >& field )
  {
    return Foam::fvm::ddt( field );
  }

%}
%enddef


//--------------------------------------------------------------------------------------
#if FOAM_VERSION( >=, 020000 )
%inline FVMHOLDER_DDT_TEMPLATE_FUNC_020000( Foam::scalar );

%inline FVMHOLDER_DDT_TEMPLATE_FUNC_020000( Foam::vector );
#endif


//--------------------------------------------------------------------------------------
%define FVMHOLDER_DDT_TEMPLATE_FUNC_010600( Type )
%{

  Foam::fvMatrixHolder< Type > fvm_ddt( const Foam::volScalarFieldHolder& field1,
                                        Foam::GeometricFieldHolder< Type, Foam::fvPatchField, Foam::volMesh >& field2 )
  {
    return Foam::fvm::ddt( field1, field2 );
  }

  Foam::fvMatrixHolder< Type > fvm_ddt( Foam::GeometricFieldHolder< Type, Foam::fvPatchField, Foam::volMesh >& field )
  {
    return Foam::fvm::ddt( field );
  }

%}
%enddef


//--------------------------------------------------------------------------------------
#if FOAM_VERSION( <, 020000 )
%inline FVMHOLDER_DDT_TEMPLATE_FUNC_010600( Foam::scalar );

%inline FVMHOLDER_DDT_TEMPLATE_FUNC_010600( Foam::vector );
#endif

//--------------------------------------------------------------------------------------
#endif

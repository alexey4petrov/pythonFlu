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
//  See http://sourceforge.net/projects/pythonflu
//
//  Author : Alexey PETROV


//---------------------------------------------------------------------------
#ifndef fvmDiv_cxx
#define fvmDiv_cxx


//---------------------------------------------------------------------------
%module "Foam.src.finiteVolume.finiteVolume.fvm.fvmDiv";
%{
  #include "src/finiteVolume/finiteVolume/fvm/fvmDiv.hh"
%}


//---------------------------------------------------------------------------
%import "src/finiteVolume/fvMesh/fvMeshes.cxx"

%import "src/finiteVolume/fvMatrices/fvMatrices.cxx"


//---------------------------------------------------------------------------
%define FVM_DIV_TEMPLATE_FUNC( Type )
%{
  Foam::tmp< Foam::fvMatrix< Type > > 
  fvm_div( const Foam::surfaceScalarField& flux,
           Foam::GeometricField< Type, Foam::fvPatchField, Foam::volMesh >& vf,
           const Foam::word& name )
  {
    return Foam::fvm::div( flux, vf, name );
  }

  Foam::tmp< Foam::fvMatrix< Type > > 
  fvm_div( const Foam::surfaceScalarField& flux,
           Foam::GeometricField< Type, Foam::fvPatchField, Foam::volMesh >& vf )
  {
    return Foam::fvm::div( flux, vf );
  }
%}
%enddef


//---------------------------------------------------------------------------
%inline FVM_DIV_TEMPLATE_FUNC( Foam::scalar );

%inline FVM_DIV_TEMPLATE_FUNC( Foam::vector );


//---------------------------------------------------------------------------
%include <fvmDiv.H>


//---------------------------------------------------------------------------
#endif

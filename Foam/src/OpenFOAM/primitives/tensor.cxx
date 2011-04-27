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
#ifndef tensor_cxx
#define tensor_cxx


//---------------------------------------------------------------------------
%module "Foam.src.OpenFOAM.primitives.tensor";
%{
  #include "src/OpenFOAM/primitives/tensor.hh"
%}


//---------------------------------------------------------------------------
%import "src/OpenFOAM/primitives/scalar.cxx"

%import "src/OpenFOAM/primitives/direction.cxx"

%include <VectorSpace.H>

%template( VectorSpace_Tensor ) Foam::VectorSpace< Foam::Tensor< Foam::scalar >, Foam::scalar, 9 >;


//---------------------------------------------------------------------------
%extend Foam::VectorSpace< Foam::Tensor< Foam::scalar >, Foam::scalar, 9 >
{
  int __len__()
  {
    return self->size();
  }
  
  Foam::scalar __getitem__( const Foam::direction theIndex )
  {
    return self->operator[]( theIndex );
  }
  
  void __setitem__( const Foam::direction theIndex, const Foam::scalar& theValue )
  {
    self->operator[]( theIndex ) = theValue;
  }
}


//---------------------------------------------------------------------------
%import "src/OpenFOAM/primitives/sphericalTensor.cxx"

%import "src/OpenFOAM/primitives/symmTensor.cxx"

%include <Tensor.H>

%include <tensor.H>

%template( tensor ) Foam::Tensor< Foam::scalar >;


//---------------------------------------------------------------------------
#endif

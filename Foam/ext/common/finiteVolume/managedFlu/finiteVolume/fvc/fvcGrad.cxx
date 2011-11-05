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
#ifndef fvcGrad_cxx
#define fvcGrad_cxx


//---------------------------------------------------------------------------
%module "Foam.ext.common.finiteVolume.managedFlu.fvch"

%{
  #include "Foam/ext/common/finiteVolume/managedFlu/finiteVolume/fvc/fvcGrad.hh"
%}


//---------------------------------------------------------------------------
%import "Foam/src/finiteVolume/fvMesh/fvMeshes.cxx"


//---------------------------------------------------------------------------
%include <fvcGrad.hpp>


%inline
{
  Foam::GeometricFieldHolder< Foam::vector, Foam::fvPatchField, Foam::volMesh >
  fvc_grad( const Foam::GeometricFieldHolder< Foam::scalar, Foam::fvsPatchField, Foam::surfaceMesh >& vf )
  {
    return Foam::fvc::grad( vf );
  }
  
  Foam::GeometricFieldHolder< Foam::vector, Foam::fvPatchField, Foam::volMesh >
  fvc_grad( const Foam::GeometricFieldHolder< Foam::scalar, Foam::fvPatchField, Foam::volMesh >& vf )
  {
    return Foam::fvc::grad( vf );
  }
  
  Foam::GeometricFieldHolder< Foam::tensor, Foam::fvPatchField, Foam::volMesh >
  fvc_grad( const Foam::GeometricFieldHolder< Foam::vector, Foam::fvPatchField, Foam::volMesh >& vf )
  {
    return Foam::fvc::grad( vf );
  }
}


//--------------------------------------------------------------------------------------
#endif

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
#ifndef linear_cxx
#define linear_cxx


//---------------------------------------------------------------------------
%module "Foam.src.finiteVolume.interpolation.surfaceInterpolation.schemes.linear";
%{
  #include "src/finiteVolume/interpolation/surfaceInterpolation/schemes/linear.hh"
%}


//---------------------------------------------------------------------------
%import "src/OpenFOAM/fields/tmp/tmp.cxx"

%import "src/finiteVolume/fvMesh/fvMeshes.cxx"

%include <linear.H>


//---------------------------------------------------------------------------
%define FOAM_LINEAR_INTERPOLATE_TEMPLATE_FUNC( Type )
%{
  inline
  Foam::tmp< Foam::GeometricField< Type, Foam::fvsPatchField, Foam::surfaceMesh > > linearInterpolate
  ( const Foam::GeometricField< Type, Foam::fvPatchField, Foam::volMesh >& vf )
  {
    return Foam::linearInterpolate( vf );
  }
%}
%enddef


//---------------------------------------------------------------------------
%inline FOAM_LINEAR_INTERPOLATE_TEMPLATE_FUNC( Foam::vector );
%inline FOAM_LINEAR_INTERPOLATE_TEMPLATE_FUNC( Foam::scalar );


//---------------------------------------------------------------------------
#endif

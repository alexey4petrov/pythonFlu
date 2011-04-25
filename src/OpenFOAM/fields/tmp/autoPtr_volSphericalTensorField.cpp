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
#ifndef autoPtr_volSphericalTensorField_cpp
#define autoPtr_volSphericalTensorField_cpp


//---------------------------------------------------------------------------
%{
  #include "src/OpenFOAM/fields/tmp/autoPtr_volSphericalTensorField.hh"
%}


//---------------------------------------------------------------------------
%import "src/OpenFOAM/fields/tmp/autoPtr.cxx"

%include "src/OpenFOAM/fields/GeometricFields/GeometricField_SphericalTensor_fvPatchField_volMesh.cpp"

AUTOPTR_TYPEMAP( Foam::volSphericalTensorField )

%template( autoPtr_volSphericalTensorField ) Foam::autoPtr< Foam::volSphericalTensorField >;

%extend Foam::autoPtr< Foam::volSphericalTensorField >
{
  SMARTPTR_EXTEND_OPERATOR_EQ( Foam::sphericalTensor );
}


//---------------------------------------------------------------------------
#endif

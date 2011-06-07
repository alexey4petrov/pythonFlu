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
#ifndef tmp_surfaceVectorField_cpp
#define tmp_surfaceVectorField_cpp


//---------------------------------------------------------------------------
%{
  #include "src/OpenFOAM/fields/tmp/tmp_surfaceVectorField.hh"
%}


//---------------------------------------------------------------------------
%import "src/OpenFOAM/fields/Fields/primitiveFields.cxx"

%include "src/OpenFOAM/fields/GeometricFields/GeometricField_vector_fvsPatchField_surfaceMesh.cpp"


//----------------------------------------------------------------------------
%template( tmp_surfaceVectorField ) Foam::tmp< Foam::GeometricField< Foam::vector, Foam::fvsPatchField, Foam::surfaceMesh > >;


//-----------------------------------------------------------------------------
%feature( "pythonappend" ) Foam::tmp< Foam::GeometricField< Foam::vector, Foam::fvsPatchField, Foam::surfaceMesh > >::SMARTPTR_PYAPPEND_GETATTR( tmp_surfaceVectorField );

%extend Foam::tmp< Foam::GeometricField< Foam::vector, Foam::fvsPatchField, Foam::surfaceMesh > >
{
  SMARTPTR_EXTEND_ATTR( tmp_surfaceVectorField );
}


//---------------------------------------------------------------------------
#endif

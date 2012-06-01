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
#ifndef autoPtr_volVectorField_cpp
#define autoPtr_volVectorField_cpp


//---------------------------------------------------------------------------
%{
  #include "Foam/src/OpenFOAM/fields/tmp/autoPtr_volVectorField.hh"
%}


//---------------------------------------------------------------------------
%import "Foam/src/OpenFOAM/fields/tmp/autoPtr.cxx"

%include "Foam/src/OpenFOAM/fields/GeometricFields/GeometricField_vector_fvPatchField_volMesh.cpp"

AUTOPTR_TYPEMAP( Foam::volVectorField );

%ignore Foam::autoPtr< Foam::volVectorField >::operator->;

%template( autoPtr_volVectorField ) Foam::autoPtr< Foam::volVectorField >;

%feature( "pythonappend" ) Foam::autoPtr< Foam::volVectorField >::SMARTPTR_PYAPPEND_GETATTR( autoPtr_volVectorField );

%extend Foam::autoPtr< Foam::volVectorField >
{
  SMARTPTR_EXTEND_ATTR( autoPtr_volVectorField );
}


//---------------------------------------------------------------------------
#endif

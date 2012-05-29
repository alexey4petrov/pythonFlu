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
#ifndef symmTensorField_cpp
#define symmTensorField_cpp


//---------------------------------------------------------------------------
%{
  #include "Foam/src/OpenFOAM/fields/Fields/symmTensorField.hh"
%}


//---------------------------------------------------------------------------
%include "Foam/src/OpenFOAM/fields/Fields/Field.cpp"

%import "Foam/src/OpenFOAM/primitives/symmTensor.cxx"

%import "Foam/src/OpenFOAM/primitives/pTraits_symmTensor.cxx"

%import "Foam/src/OpenFOAM/primitives/Lists/symmTensorList.cxx"

%include "Foam/src/OpenFOAM/fields/Fields/sphericalTensorField.cpp"


//---------------------------------------------------------------------------
%ignore Foam::Field< Foam::symmTensor >::Field;
%ignore Foam::Field< Foam::symmTensor >::typeName;
%ignore Foam::sqr;

#if SWIG_VERSION >= 0x020000 && SWIG_VERSION < 0x020003
%ignore Foam::Field< Foam::symmTensor >::null;
#endif

%template( symmTensorField ) Foam::Field< Foam::symmTensor >; 

%typedef Foam::Field< Foam::symmTensor > symmTensorField;

FIELD_TEMPLATE_FUNC( symmTensor )


//---------------------------------------------------------------------------
#endif

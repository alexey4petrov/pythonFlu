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
#ifndef complexFields_cxx
#define complexFields_cxx


//---------------------------------------------------------------------------
%module "Foam.src.OpenFOAM.fields.Fields.complexFields";
%{
  #include "Foam/src/OpenFOAM/fields/Fields/complexFields.hh"
%}


//---------------------------------------------------------------------------
%import "Foam/src/OpenFOAM/fields/Fields/primitiveFields.cxx"


//---------------------------------------------------------------------------
%import "Foam/src/OpenFOAM/primitives/complex.cxx"

%import "Foam/src/OpenFOAM/containers/Lists/UList/UList_complex.cxx"

%import "Foam/src/OpenFOAM/containers/Lists/List/List_complex.cxx"

%ignore Foam::Field< Foam::complex >::Field;
%ignore Foam::Field< Foam::complex >::typeName;
%ignore Foam::Field< Foam::complex >::replace;
%ignore Foam::Field< Foam::complex >::component;
%ignore Foam::Field< Foam::complex >::T;

#if SWIG_VERSION >= 0x020000 && SWIG_VERSION < 0x020003
%ignore Foam::Field< Foam::complex >::null;
#endif

COMPLEX_FIELD_TEMPLATE_FUNC( complex );

%template( complexField ) Foam::Field< Foam::complex >;


//---------------------------------------------------------------------------
%import "Foam/src/OpenFOAM/primitives/complexVector.cxx"

%include "Foam/src/OpenFOAM/containers/Lists/List/List_complexVector.cpp"

%ignore Foam::Field< Foam::complexVector >::Field;
%ignore Foam::Field< Foam::complexVector >::typeName;
%ignore Foam::Field< Foam::complexVector >::T;

#if SWIG_VERSION >= 0x020000 && SWIG_VERSION < 0x020003
%ignore Foam::Field< Foam::complexVector >::null;
#endif

COMPLEX_FIELD_TEMPLATE_FUNC( complexVector );

%template( complexVectorField ) Foam::Field< Foam::complexVector >;

%include <complexFields.H>


//---------------------------------------------------------------------------
#endif

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
#ifndef ext_tmp_scalarField_cpp
#define ext_tmp_scalarField_cpp


//---------------------------------------------------------------------------
%{
  #include "Foam/ext/common/OpenFOAM/ext_tmp/ext_tmp_scalarField.hh"
%}


//---------------------------------------------------------------------------
%import "Foam/src/common.hxx"

%import "Foam/ext/common/ext_tmp.hxx"

%include "Foam/src/OpenFOAM/fields/Fields/scalarField.cpp"

%ignore Foam::ext_tmp< Foam::Field< Foam::scalar > >::operator=;

%template ( ext_tmp_scalarField ) Foam::ext_tmp< Foam::Field< Foam::scalar > >;


//---------------------------------------------------------------------------
#endif


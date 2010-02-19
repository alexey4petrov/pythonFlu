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
//  See https://csrcs.pbmr.co.za/svn/nea/prototypes/reaktor/pyfoam
//
//  Author : Alexey PETROV


//---------------------------------------------------------------------------
#if ( __FOAM_VERSION__ < 010600 )
%include "src/common.hxx"
#define uniformDimensionedField_cxx
#endif


//---------------------------------------------------------------------------
#ifndef uniformDimensionedField_cxx
#define uniformDimensionedField_cxx


//---------------------------------------------------------------------------
%include "src/OpenFOAM/db/regIOobject.cxx"

%include "src/OpenFOAM/fields/Fields/Field.cxx"

%include "src/OpenFOAM/dimensionedTypes/dimensionedType.cxx"

%{
    #include "UniformDimensionedField.H"
%}

%ignore Foam::UniformDimensionedField::UniformDimensionedField;

%include "UniformDimensionedField.H"


//---------------------------------------------------------------------------
#endif


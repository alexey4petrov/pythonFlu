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
//  Author : Andrey Simurzin


//---------------------------------------------------------------------------
%module "Foam.src.OpenFOAM.db.IOstreams.Pstreams.UPstream";
%{
   #include "Foam/src/OpenFOAM/db/IOstreams/Pstreams/UPstream.hh"
%}

%import "Foam/src/common.hxx"


//---------------------------------------------------------------------------
#if FOAM_VERSION( <, 020000 )
#define UPstream_cxx
#endif


//---------------------------------------------------------------------------
#ifndef UPstream_cxx
#define UPstream_cxx


//---------------------------------------------------------------------------
%import "Foam/src/OpenFOAM/db/typeInfo/className.hxx"

%import "Foam/src/OpenFOAM/primitives/label.cxx"

%import "Foam/src/OpenFOAM/primitives/Lists/labelList.cxx"

%import "Foam/src/OpenFOAM/containers/Lists/DynamicList/DynamicList.cxx"

%import "Foam/src/OpenFOAM/containers/HashTables/HashTable/HashTable.cxx"

%import "Foam/src/OpenFOAM/primitives/strings/string.cxx"

%import "Foam/src/OpenFOAM/containers/NamedEnum/NamedEnum.cxx"

%import "Foam/src/OpenFOAM/primitives/ops/ops_label.cxx"

%include <UPstream.H>


//---------------------------------------------------------------------------
#endif

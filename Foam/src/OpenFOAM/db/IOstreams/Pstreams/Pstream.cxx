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
#ifndef Pstream_cxx
#define Pstream_cxx


//---------------------------------------------------------------------------
%module "Foam.src.OpenFOAM.db.IOstreams.Pstreams.Pstream";
%{
   #include "Foam/src/OpenFOAM/db/IOstreams/Pstreams/Pstream.hh"
%}


//---------------------------------------------------------------------------
%import "Foam/src/common.hxx"

%import "Foam/src/OpenFOAM/db/typeInfo/className.hxx"

%import "Foam/src/OpenFOAM/primitives/label.cxx"

%import "Foam/src/OpenFOAM/primitives/Lists/labelList.cxx"

// #include <DynamicList.H>
// #include <HashTable.H>

%import "Foam/src/OpenFOAM/primitives/strings/string.cxx"

// #include <NamedEnum.H>

%import "Foam/src/OpenFOAM/primitives/ops/ops_label.cxx"

%import "Foam/src/OpenFOAM/db/IOstreams/Pstreams/UPstream.cxx"

#if FOAM_NOT_BRANCH( __FREEFOAM__ )
%include <Pstream.H>
#else
%nodefaultctor;
%include <Pstream.H>
%clearnodefaultctor;
#endif


//---------------------------------------------------------------------------
%inline
{
  int ext_reduce( int theValue, const Foam::sumOp<Foam::label>& theBop )
  {
    Foam::reduce( theValue, theBop );
    return theValue;
  }

  Foam::label returnReduce( const Foam::label& theValue, 
                            const Foam::sumOp< Foam::label >& theBop )
  {
    return Foam::returnReduce( theValue, theBop );
  }
}


//---------------------------------------------------------------------------
#endif

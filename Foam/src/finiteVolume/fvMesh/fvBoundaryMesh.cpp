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
#ifndef fvBoundaryMesh_cpp
#define fvBoundaryMesh_cpp


//---------------------------------------------------------------------------
%module "Foam.src.finiteVolume.fvMesh.fvBoundaryMesh";
%{
  #include "Foam/src/finiteVolume/fvMesh/fvBoundaryMesh.hh"
%}


//---------------------------------------------------------------------------
%include "Foam/src/finiteVolume/fvMesh/fvPatches/fvPatchList.cpp"

%include <fvBoundaryMesh.H>

%define FVBOUNDARYMESH_EXTENDS()
  __PTRLISTBASED_ADDONS__( Foam::fvPatch );
  const Foam::fvPatch& __getitem__( const Foam::word& the_word ) const
  {
    return get_ref( self )[ the_word ];
  }
%enddef


//---------------------------------------------------------------------------
%extend Foam::fvBoundaryMesh
{ 
#if FOAM_VERSION(>=,020000)
  FVBOUNDARYMESH_EXTENDS();
#endif
}



//---------------------------------------------------------------------------
#endif

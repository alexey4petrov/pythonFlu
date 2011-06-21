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
#ifndef primitivePatch_cxx
#define primitivePatch_cxx


//---------------------------------------------------------------------------
%module "Foam.src.OpenFOAM.meshes.PrimitivePatch.p_rimitivePatch"
%{
  #include "Foam/src/OpenFOAM/meshes/PrimitivePatch/p_rimitivePatch.hh"
%}


//---------------------------------------------------------------------------
%import "Foam/src/OpenFOAM/containers/Lists/SubList/SubList_face.cxx"

%import "Foam/src/OpenFOAM/meshes/PrimitivePatch/PrimitivePatch.cxx"

%ignore Foam::PrimitivePatch< Foam::face, Foam::SubList, const Foam::pointField& >::PrimitivePatch;
%ignore Foam::PrimitivePatch< Foam::face, Foam::SubList, const Foam::pointField& >::faceCentres;

#if FOAM_BRANCH_VERSION( dev, >=, 010500 )
  %ignore Foam::PrimitivePatch< Foam::face, Foam::SubList, const Foam::pointField& >::writeVTK;
  %ignore Foam::PrimitivePatch< Foam::face, Foam::SubList, const Foam::pointField& >::writeVTKNormals;
#endif

%include <primitivePatch.H>

%template( primitivePatch ) Foam::PrimitivePatch< Foam::face, Foam::SubList, const Foam::pointField& >;

%extend Foam::PrimitivePatch< Foam::face, Foam::SubList, const Foam::pointField& >
{ 
  Foam::label ext_size()
  {
    return self->size();
  }
}


//---------------------------------------------------------------------------
#endif

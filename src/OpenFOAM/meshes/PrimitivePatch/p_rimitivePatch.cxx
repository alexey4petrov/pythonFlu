//  VulaSHAKA (Simultaneous Neutronic, Fuel Performance, Heat And Kinetics Analysis)
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
//  See https://vulashaka.svn.sourceforge.net/svnroot/vulashaka
//
//  Author : Alexey PETROV


//---------------------------------------------------------------------------
#ifndef primitivePatch_cxx
#define primitivePatch_cxx


//---------------------------------------------------------------------------
%include "src/OpenFOAM/containers/Lists/SubList/SubList_face.cxx"
%include "src/OpenFOAM/meshes/PrimitivePatch/PrimitivePatch.cxx"


%ignore Foam::PrimitivePatch< face, SubList, const pointField& >::PrimitivePatch;

#if FOAM_BRANCH_VERSION( dev, ==, 010500 )
%ignore Foam::PrimitivePatch< face, SubList, const pointField& >::writeVTK;
%ignore Foam::PrimitivePatch< face, SubList, const pointField& >::writeVTKNormals;
#endif

%{
  #include "primitivePatch.H"
%}

%template ( primitivePatch ) Foam::PrimitivePatch< face, SubList, const pointField& >;

%include "primitivePatch.H"

%extend Foam::PrimitivePatch< face, SubList, const pointField& >
{ 
   Foam::label ext_size()
   {
    return self->size();
   }
  
}


//---------------------------------------------------------------------------
#endif

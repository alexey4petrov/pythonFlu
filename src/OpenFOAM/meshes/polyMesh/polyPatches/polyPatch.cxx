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
#ifndef polyPatch_cxx
#define polyPatch_cxx


//---------------------------------------------------------------------------
%include "src/OpenFOAM/db/typeInfo/typeInfo.hxx"

%include "src/OpenFOAM/meshes/PrimitivePatch/p_rimitivePatch.cxx"

%include "src/OpenFOAM/meshes/patchIdentifier.cxx"

%{
    #include "polyPatch.H"
    #include "polyBoundaryMesh.H"
%}

%ignore Foam::polyPatch::faceCentres() const;
%ignore Foam::polyPatch::faceAreas() const;
%ignore Foam::polyPatch::faceCellCentres() const;

%include "polyPatch.H"

%extend Foam::polyPatch COMMON_EXTENDS;

%extend Foam::polyPatch
{
  static Foam::polyPatch* nullPtr()
  {
    return (Foam::polyPatch*) NULL;
  }
}


//---------------------------------------------------------------------------
#endif

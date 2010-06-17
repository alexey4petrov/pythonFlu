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
#ifndef PtrList_coordinateSystem_cxx
#define PtrList_coordinateSystem_cxx


//---------------------------------------------------------------------------
%include "src/meshTools/coordinateSystems/coordinateSystem.cxx"

%include "src/OpenFOAM/containers/Lists/PtrList/PtrList.cxx"

%ignore Foam::PtrList< Foam::coordinateSystem >::begin;
%ignore Foam::PtrList< Foam::coordinateSystem >::end;
%ignore Foam::PtrList< Foam::coordinateSystem >::set;

%template( PtrList_coordinateSystem ) Foam::PtrList< Foam::coordinateSystem >;


//---------------------------------------------------------------------------
%extend Foam::PtrList< Foam::coordinateSystem > PTRLISTBASED_ADDONS( Foam::coordinateSystem )


//---------------------------------------------------------------------------
#endif

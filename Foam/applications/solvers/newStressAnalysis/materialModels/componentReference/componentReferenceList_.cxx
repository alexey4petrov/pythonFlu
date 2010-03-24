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
//  See https://vulashaka.svn.sourceforge.net/svnroot/vulashaka/pyfoam
//
//  Author : Alexey PETROV


//---------------------------------------------------------------------------
#if ( __FOAM_VERSION__ > 010401 )
%include "src/common.hxx"
#define componentReferenceList_cxx
#endif


//---------------------------------------------------------------------------
#ifndef componentReferenceList_cxx
#define componentReferenceList_cxx


//---------------------------------------------------------------------------
%include "Foam/applications/solvers/newStressAnalysis/materialModels/componentReference/componentReference_.cxx"

%include "Foam/applications/solvers/newStressAnalysis/materialModels/componentReference/autoPtr_componentReference.cxx"

%include "src/OpenFOAM/containers/Lists/PtrList/PtrList.cxx"


%ignore Foam::PtrList< Foam::componentReference >::PtrList;
%ignore Foam::PtrList< Foam::componentReference >::begin;
%ignore Foam::PtrList< Foam::componentReference >::end;
%ignore Foam::PtrList< Foam::componentReference >::set;

%template( PtrList_componentReference ) Foam::PtrList< Foam::componentReference >;


//---------------------------------------------------------------------------
%extend Foam::PtrList< Foam::componentReference >
{
  Foam::PtrList< Foam::componentReference >( Foam::Istream& is, const Foam::iNew& inewt )
  {
    return new Foam::PtrList< Foam::componentReference >( is, inewt );
  }
}

%extend Foam::PtrList< Foam::componentReference > PTRLISTBASED_ADDONS( Foam::componentReference )

//---------------------------------------------------------------------------
#endif

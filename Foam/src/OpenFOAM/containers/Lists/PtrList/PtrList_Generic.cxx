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
//  See http://sourceforge.net/projects/pythonflu
//
//  Author : Alexey PETROV


//---------------------------------------------------------------------------
#ifndef PtrList_generic_cxx
#define PtrList_generic_cxx


//---------------------------------------------------------------------------
%module "Foam.src.OpenFOAM.containers.Lists.PtrList.PtrList_Generic";
%{
   #include "src/OpenFOAM/containers/Lists/PtrList/PtrList_Generic.hh"
%}


//---------------------------------------------------------------------------
%import "src/OpenFOAM/containers/Lists/PtrList/PtrList.cxx"

%import "src/OpenFOAM/containers/Lists/PtrList/PtrList_GenericType.cxx"

%import "src/OpenFOAM/containers/Lists/PtrList/PtrList_GenericINew.cxx"

%ignore Foam::PtrList< Foam::PtrList_TypeHolder >::begin;
%ignore Foam::PtrList< Foam::PtrList_TypeHolder >::end;
%ignore Foam::PtrList< Foam::PtrList_TypeHolder >::PtrList;
%ignore Foam::PtrList< Foam::PtrList_TypeHolder >::set;
%ignore Foam::PtrList< Foam::PtrList_TypeHolder >::xfer;


%template( PtrList_Generic ) Foam::PtrList< Foam::PtrList_TypeHolder >;

%template ( TContainer_PtrList_TypeHolder ) Foam::TContainer_iterator< Foam::PtrList< Foam::PtrList_TypeHolder > >;


//---------------------------------------------------------------------------
%extend Foam::PtrList< Foam::PtrList_TypeHolder >
{
  Foam::PtrList< Foam::PtrList_TypeHolder >( const Foam::label s )
  {
    return new Foam::PtrList< Foam::PtrList_TypeHolder >( s );
  }
  
  Foam::PtrList< Foam::PtrList_TypeHolder >( Istream& is, const Foam::PtrList_INewHolder& inewt )
  {
    return new Foam::PtrList< Foam::PtrList_TypeHolder >( is, inewt );
  }
  
  Foam::TContainer_iterator< Foam::PtrList< Foam::PtrList_TypeHolder > >* __iter__()
  {
    return new Foam::TContainer_iterator< Foam::PtrList< Foam::PtrList_TypeHolder > >( *self );
  }
}

%extend Foam::PtrList< Foam::PtrList_TypeHolder > PTRLISTBASED_ADDONS( Foam::PtrList_TypeHolder )


//---------------------------------------------------------------------------
#endif

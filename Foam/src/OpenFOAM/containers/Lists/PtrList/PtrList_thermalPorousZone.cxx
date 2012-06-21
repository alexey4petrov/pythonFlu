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
//  Author : Alexey PETROV, Andrey SIMURZIN


//---------------------------------------------------------------------------
%module "Foam.src.OpenFOAM.containers.Lists.PtrList.PtrList_thermalPorousZone";
%{
  #include "Foam/src/OpenFOAM/containers/Lists/PtrList/PtrList_thermalPorousZone.hh"
%}


//---------------------------------------------------------------------------
%import "Foam/src/common.hxx"

#if FOAM_VERSION( <, 020000 )
#define PtrList_thermalPorousZone_cxx
#endif


//-----------------------------------------------------------------------------
#ifndef PtrList_thermalPorousZone_cxx
#define PtrList_thermalPorousZone_cxx


//---------------------------------------------------------------------------
%import "Foam/src/thermophysicalModels/thermalPorousZone/thermalPorousZone.cxx"

%import "Foam/src/OpenFOAM/containers/Lists/PtrList/PtrList.cxx"

%ignore Foam::PtrList< Foam::thermalPorousZone >::PtrList;
%ignore Foam::PtrList< Foam::thermalPorousZone >::begin;
%ignore Foam::PtrList< Foam::thermalPorousZone >::end;
%ignore Foam::PtrList< Foam::thermalPorousZone >::set;
%ignore Foam::PtrList< Foam::thermalPorousZone >::xfer;

%template( PtrList_thermalPorousZone ) Foam::PtrList< Foam::thermalPorousZone >;


//---------------------------------------------------------------------------
%extend Foam::PtrList< Foam::thermalPorousZone >
{
  Foam::PtrList< Foam::thermalPorousZone >( const Foam::label s )
  {
    return new Foam::PtrList< Foam::thermalPorousZone >( s );
  }
}

%extend Foam::PtrList< Foam::thermalPorousZone > PTRLISTBASED_ADDONS( Foam::thermalPorousZone )


//---------------------------------------------------------------------------
#endif

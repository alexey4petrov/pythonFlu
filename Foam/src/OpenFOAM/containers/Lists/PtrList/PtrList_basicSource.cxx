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
%module "Foam.src.OpenFOAM.containers.Lists.PtrList.PtrList_basicSource";
%{
   #include "Foam/src/OpenFOAM/containers/Lists/PtrList/PtrList_basicSource.hh"
%}


//---------------------------------------------------------------------------
%import "Foam/src/common.hxx"

#if FOAM_VERSION( <, 010701 )
#define PtrList_basicSource_cxx
#endif


//---------------------------------------------------------------------------
#ifndef PtrList_basicSource_cxx
#define PtrList_basicSource_cxx


//---------------------------------------------------------------------------
%import "Foam/src/OpenFOAM/fields/tmp/autoPtr_basicSource.cxx"

%import "Foam/src/OpenFOAM/containers/Lists/PtrList/PtrList.cxx"

%ignore Foam::PtrList< Foam::basicSource >::PtrList;
%ignore Foam::PtrList< Foam::basicSource >::begin;
%ignore Foam::PtrList< Foam::basicSource >::end;
%ignore Foam::PtrList< Foam::basicSource >::set;
%ignore Foam::PtrList< Foam::basicSource >::xfer;


%template( PtrList_basicSource ) Foam::PtrList< Foam::basicSource >;


//---------------------------------------------------------------------------
%extend Foam::PtrList< Foam::basicSource >
{
  Foam::PtrList< Foam::basicSource >( const Foam::label s )
  {
    return new Foam::PtrList< Foam::basicSource >( s );
  }
}

%extend Foam::PtrList< Foam::basicSource > PTRLISTBASED_ADDONS( Foam::basicSource );


//---------------------------------------------------------------------------
#endif

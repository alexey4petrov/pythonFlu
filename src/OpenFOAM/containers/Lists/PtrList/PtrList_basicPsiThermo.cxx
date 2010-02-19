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
//  See https://csrcs.pbmr.co.za/svn/nea/prototypes/reaktor/pyfoam
//
//  Author : Alexey PETROV


//---------------------------------------------------------------------------
#if ( __FOAM_VERSION__ < 010600 )
%include "src/common.hxx"
#define PtrList_basicPsiThermo_cxx
#endif


//---------------------------------------------------------------------------
#ifndef PtrList_basicPsiThermo_cxx
#define PtrList_basicPsiThermo_cxx


//---------------------------------------------------------------------------
%include "src/thermophysicalModels/basic/psiThermo/basicPsiThermo.cxx"

%include "src/OpenFOAM/fields/tmp/autoPtr_basicPsiThermo.cxx"

%include "src/OpenFOAM/containers/Lists/PtrList/PtrList.cxx"

%ignore Foam::PtrList< Foam::basicPsiThermo >::PtrList;
%ignore Foam::PtrList< Foam::basicPsiThermo >::begin;
%ignore Foam::PtrList< Foam::basicPsiThermo >::end;
%ignore Foam::PtrList< Foam::basicPsiThermo >::set;

#if ( __FOAM_VERSION__ >= 010600 )
%ignore Foam::PtrList< Foam::basicPsiThermo >::xfer;
#endif

%template( PtrList_basicPsiThermo ) Foam::PtrList< Foam::basicPsiThermo >;


//---------------------------------------------------------------------------
%extend Foam::PtrList< Foam::basicPsiThermo >
{
  Foam::PtrList< Foam::basicPsiThermo >( const Foam::label s )
  {
    return new Foam::PtrList< Foam::basicPsiThermo >( s );
  }
}

%extend Foam::PtrList< Foam::basicPsiThermo > PTRLISTBASED_ADDONS( Foam::basicPsiThermo )


//---------------------------------------------------------------------------
#endif

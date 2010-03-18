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
#if ( __FOAM_VERSION__ < 010500 )   
%include "src/common.hxx"
#define PtrList_ccompressible_RASModel_cxx
#endif


//---------------------------------------------------------------------------
#ifndef PtrList_ccompressible_RASModel_cxx
#define PtrList_compressible_RASModel_cxx


//---------------------------------------------------------------------------
// Keep on corresponding "director" includes at the top of SWIG defintion file

%include "src/OpenFOAM/directors.hxx"

%include "src/finiteVolume/directors.hxx"


//---------------------------------------------------------------------------
%include "src/turbulenceModels/compressible/RAS/RASModel.cxx"

%include "src/OpenFOAM/fields/tmp/autoPtr_compressible_RASModel.cxx"

%include "src/OpenFOAM/containers/Lists/PtrList/PtrList.cxx"

%ignore Foam::PtrList< Foam::compressible::RASModel >::PtrList;
%ignore Foam::PtrList< Foam::compressible::RASModel >::begin;
%ignore Foam::PtrList< Foam::compressible::RASModel >::end;
%ignore Foam::PtrList< Foam::compressible::RASModel >::set;

#if ( __FOAM_VERSION__ >= 010600 )
%ignore Foam::PtrList< Foam::compressible::RASModel >::xfer;
#endif

%template( PtrList_compressible_RASModel ) Foam::PtrList< Foam::compressible::RASModel >;


//---------------------------------------------------------------------------
%extend Foam::PtrList< Foam::compressible::RASModel >
{
  Foam::PtrList< Foam::compressible::RASModel >( const Foam::label s )
  {
    return new Foam::PtrList< Foam::compressible::RASModel >( s );
  }
}

%extend Foam::PtrList< Foam::compressible::RASModel > PTRLISTBASED_ADDONS( Foam::compressible::RASModel )


//---------------------------------------------------------------------------
#endif

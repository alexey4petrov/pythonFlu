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
#ifndef porousZones_cxx
#define porousZones_cxx


//---------------------------------------------------------------------------
%module "Foam.src.finiteVolume.cfdTools.general.porousMedia.porousZones";
%{
  #include "Foam/src/finiteVolume/cfdTools/general/porousMedia/porousZones.hh"
%}


//---------------------------------------------------------------------------
%import "Foam/src/finiteVolume/cfdTools/general/porousMedia/porousZone.cxx"

%import "Foam/src/OpenFOAM/containers/Lists/PtrList/IOPtrList/IOPtrList_porousZone.cxx"

%import "Foam/src/OpenFOAM/containers/Lists/PtrList/IOPtrList/IOPtrList.hxx"

%import "Foam/src/finiteVolume/fvMatrices/fvMatrices.cxx"

%import "Foam/src/finiteVolume/fvMesh/fvMeshes.cxx"

%include <porousZones.H>

#if FOAM_VERSION( >=, 020000)
%include <PorousZones.H>

%template (porousZones) Foam::PorousZones< Foam::porousZone >;
#endif


//---------------------------------------------------------------------------
%define POROUSZONES_EXTENDS( Type )
   Foam::tmp< Foam::fvMatrix< Foam::Type > > ddt( const Foam::volScalarField& rho, 
                                                  Foam::GeometricField< Foam::Type, Foam::fvPatchField, Foam::volMesh >& vf )
   {
      return self->ddt( rho, vf );
   }
   
   Foam::tmp< Foam::fvMatrix< Foam::Type > > ddt( Foam::GeometricField< Foam::Type, Foam::fvPatchField, Foam::volMesh >& vf )
   {
      return self->ddt( vf );
   }
   
   Foam::tmp<Foam::fvMatrix< Foam::Type > > ddt( const Foam::dimensionedScalar& rho, 
                                                 Foam::GeometricField< Foam::Type, Foam::fvPatchField, Foam::volMesh >& vf )
   {
      return self->ddt( rho,vf );
   }

%enddef


//---------------------------------------------------------------------------
#if FOAM_VERSION( >=, 010500 ) && FOAM_VERSION( <, 020000)
%extend Foam::porousZones
{
   POROUSZONES_EXTENDS( vector );
   POROUSZONES_EXTENDS( scalar );
}
#endif

//---------------------------------------------------------------------------
#if FOAM_VERSION( >=, 020000)
%extend Foam::PorousZones< Foam::porousZone >
{
   POROUSZONES_EXTENDS( vector );
   POROUSZONES_EXTENDS( scalar );
}
#endif


//---------------------------------------------------------------------------
%include "Foam/ext/common/finiteVolume/managedFlu/porousZonesHolder.cpp"

//---------------------------------------------------------------------------
#endif

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
%module "Foam.src.finiteVolume.cfdTools.general.fieldSources.basicSource.basicSource.basicSourceList"

%{
  #include "Foam/src/finiteVolume/cfdTools/general/fieldSources/basicSource/basicSource/basicSourceList.hh"
%}


//---------------------------------------------------------------------------
%import "Foam/src/common.hxx"

#if FOAM_VERSION( <, 010701 )
#define basicSourceList_cxx
#endif


//---------------------------------------------------------------------------
#ifndef basicSourceList_cxx
#define basicSourceList_cxx


//---------------------------------------------------------------------------
%import "Foam/src/OpenFOAM/containers/Lists/PtrList/PtrList_basicSource.cxx"

%include <basicSourceList.H>


%define BASICSOURCELIST_EXTEND( Type )
%extend Foam::basicSourceList
{
  Foam::tmp< Foam::fvMatrix< Type > > operator()( Foam::GeometricField< Type, Foam::fvPatchField, Foam::volMesh >& fld )
  {
    return self->operator()( fld );
  }

  Foam::tmp< Foam::fvMatrix< Type > > operator()( Foam::GeometricField< Type, Foam::fvPatchField, Foam::volMesh >& fld, const Foam::word& fieldName )
  {
    return self->operator()( fld, fieldName );
  }
  
  void constrain( fvMatrix< Type >& eqn )
  {
    self->constrain( eqn );
  }

  void constrain( fvMatrix< Type >& eqn, const word& fieldName )
  {
    self->constrain( eqn, fieldName );
  }

}
%enddef


//---------------------------------------------------------------------------
#if FOAM_VERSION( >=, 020100 )
BASICSOURCELIST_EXTEND( Foam::scalar );
BASICSOURCELIST_EXTEND( Foam::vector );
#endif

//---------------------------------------------------------------------------
%include "Foam/ext/common/finiteVolume/managedFlu/basicSourceListHolder.cpp"


//---------------------------------------------------------------------------
#endif

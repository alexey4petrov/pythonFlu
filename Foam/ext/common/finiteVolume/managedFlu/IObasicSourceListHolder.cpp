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
#ifndef IObasicSourceListHolder_cpp
#define IObasicSourceListHolder_cpp


//---------------------------------------------------------------------------
%{
  #include "Foam/ext/common/finiteVolume/managedFlu/IObasicSourceListHolder.hh"
%}


//---------------------------------------------------------------------------
%import "Foam/ext/common/managedFlu/commonHolder.hxx"

%import "Foam/ext/common/managedFlu/SimpleHolder.cxx"

%import "Foam/src/finiteVolume/fvMesh/fvMeshes.cxx"

%include "Foam/ext/common/finiteVolume/shared_ptr/shared_ptr_IObasicSourceList.hpp"

INCLUDE_FILENAME(IObasicSourceListHolder,hpp)


//---------------------------------------------------------------------------
%feature( "pythonappend" ) Foam::IObasicSourceListHolder::SMARTPTR_PYAPPEND_GETATTR( IObasicSourceListHolder );

%extend Foam::IObasicSourceListHolder
{
  SMARTPTR_EXTEND_ATTR( IObasicSourceListHolder );
  HOLDERS_CALL_SHARED_PTR_EXTENSION( IObasicSourceList );
}


//--------------------------------------------------------------------------------------
%define IOBASICSOURCELISTHOLDER_EXTEND( Type )
%extend Foam::IObasicSourceListHolder
{
  Foam::tmp< Foam::fvMatrix< Type > > operator()( Foam::GeometricField< Type, Foam::fvPatchField, Foam::volMesh >& fld )
  {
    return self->operator->()->operator()( fld );
  }

  Foam::tmp< Foam::fvMatrix< Type > > operator()( Foam::GeometricField< Type, Foam::fvPatchField, Foam::volMesh >& fld, const Foam::word& fieldName )
  {
    return self->operator->()->operator()( fld, fieldName );
  }
}
%enddef


//---------------------------------------------------------------------------
#if FOAM_VERSION( >=, 020100 )
IOBASICSOURCELISTHOLDER_EXTEND( Foam::scalar );
IOBASICSOURCELISTHOLDER_EXTEND( Foam::vector );
#endif


//---------------------------------------------------------------------------
#endif

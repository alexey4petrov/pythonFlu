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
#ifndef PtrList_scalarField_cxx
#define PtrList_scalarField_cxx


//---------------------------------------------------------------------------
%module "Foam.src.OpenFOAM.containers.Lists.PtrList.PtrList_scalarField";
%{
  #include "src/OpenFOAM/containers/Lists/PtrList/PtrList_scalarField.hh"
%}


//---------------------------------------------------------------------------
%import "src/OpenFOAM/fields/Fields/primitiveFields.cxx"

%import "src/OpenFOAM/fields/tmp/autoPtr_scalarField.cxx"

%import "src/OpenFOAM/containers/Lists/PtrList/PtrList.cxx"

%ignore Foam::PtrList< Foam::scalarField >::PtrList;
%ignore Foam::PtrList< Foam::scalarField >::set;
%ignore Foam::PtrList< Foam::scalarField >::begin;
%ignore Foam::PtrList< Foam::scalarField >::end;

%template( PtrList_scalarField ) Foam::PtrList< Foam::scalarField >;


//---------------------------------------------------------------------------
%extend Foam::PtrList< Foam::scalarField >
{
  Foam::PtrList< Foam::scalarField >( const Foam::label s )
  {
    return new Foam::PtrList< Foam::scalarField >( s );
  }
}

%extend Foam::PtrList< Foam::scalarField > PTRLISTBASED_ADDONS( Foam::scalarField )


//---------------------------------------------------------------------------
#endif
    

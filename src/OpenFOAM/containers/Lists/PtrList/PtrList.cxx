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
//  See https://vulashaka.svn.sourceforge.net/svnroot/vulashaka
//
//  Author : Alexey PETROV


//---------------------------------------------------------------------------
#ifndef PtrList_cxx
#define PtrList_cxx


//---------------------------------------------------------------------------
%include "src/OpenFOAM/containers/Lists/List/List.cxx"

%include "PtrList.H"

%{
    #include "PtrList.H"
%}


//---------------------------------------------------------------------------
%define __PTRLISTBASED_AUTOPTR_SET_ADDONS__( TItem )
Foam::autoPtr< TItem > ext_set( const Foam::label i, const Foam::autoPtr< TItem > & ptr )
{
  return self->set( i, ptr );
}
%enddef

%define __PTRLISTBASED_TMP_SET_ADDONS__( TItem )
Foam::autoPtr< TItem > ext_set( const Foam::label i, const Foam::tmp< TItem > & ptr )
{
  return self->set( i, ptr );
}
%enddef

%define PTRLISTBASED_SET_ADDONS( TItem )
{
  __PTRLISTBASED_TMP_SET_ADDONS__( TItem )
}
%enddef


//---------------------------------------------------------------------------
%define __PTRLISTBASED_ADDONS__( TItem )
int __len__()
{
  return self->size();
}
  
TItem& __getitem__( const Foam::label theIndex )
{
  return self->operator[]( theIndex );
}
%enddef

%define PTRLISTBASED_ADDONS( TItem )
{
  __PTRLISTBASED_ADDONS__( TItem )
  __PTRLISTBASED_AUTOPTR_SET_ADDONS__( TItem )
}
%enddef


//---------------------------------------------------------------------------
#endif


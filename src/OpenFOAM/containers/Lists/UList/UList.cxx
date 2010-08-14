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
#ifndef UList_cxx
#define UList_cxx


//---------------------------------------------------------------------------
%include "src/OpenFOAM/primitives/label.cxx"

%{
   #include "UList.H"
   #include "ListOps.H"
%}

%include "UList.H"


//---------------------------------------------------------------------------
%define SEQUENCE_ADDONS( TItem )
{
    int __len__()
    {
      return self->size();
    }
    
    TItem __getitem__( const Foam::label theIndex )
    {
      return self->operator[]( theIndex );
    }

    void __setitem__( const Foam::label theIndex, TItem theValue )
    {
      self->operator[]( theIndex ) = theValue;
    }

    TContainer_iterator< UList< TItem > >* __iter__()
    {
      return new TContainer_iterator< UList< TItem > >( *self );
    }
}
%enddef


//---------------------------------------------------------------------------
%define LISTS_FUNCS( TItem )
{

#if FOAM_VERSION( <, 010600 )
  Foam::label ext_findIndex( TItem& t )
  {
    return Foam::findIndex( *self, t );
  }
#endif

#if FOAM_VERSION( >=, 010600 ) 
  Foam::label ext_findIndex( TItem& t, const label start=0 )
  {
    return Foam::findIndex( *self, t, start );
  }
#endif

}  
%enddef


//----------------------------------------------------------------------------
%define ULISTBASED_ADDONS( TItem )

%extend Foam::UList< TItem > SEQUENCE_ADDONS( TItem )

%extend Foam::UList< TItem > LISTS_FUNCS( TItem )

%enddef


//---------------------------------------------------------------------------
#endif

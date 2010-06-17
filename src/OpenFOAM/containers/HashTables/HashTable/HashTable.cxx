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
#ifndef HashTable_cxx
#define HashTable_cxx


//---------------------------------------------------------------------------
%include "src/OpenFOAM/db/typeInfo/className.hxx"

%include "src/OpenFOAM/primitives/strings/string.cxx"

%include "src/OpenFOAM/primitives/strings/word.cxx"

%{
    #include "HashTable.H"
%}

%include "HashTable.H"


//---------------------------------------------------------------------------
%define __HASHTABLE_ADDONS__( TValue, TKey, THash )
{
    int __len__()
    {
        return self->size();
    }
    
    TValue __getitem__( const TKey& key )
    {
        return self->operator[]( key );
    }

    TContainer_iterator< Foam::HashTable< TValue, TKey, THash > >* __iter__()
    {
      return new TContainer_iterator< Foam::HashTable< TValue, TKey, THash > >( *self );
    }
}
%enddef

%define HASHTABLE_ADDONS( TValue, TKey, THash )
    %extend Foam::HashTable< TValue, TKey, THash > __HASHTABLE_ADDONS__( TValue, TKey, THash )
    %extend Foam::HashTable< TValue, TKey, THash > COMMON_EXTENDS;
%enddef


//---------------------------------------------------------------------------
#endif


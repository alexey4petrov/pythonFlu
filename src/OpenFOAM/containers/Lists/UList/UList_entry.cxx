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
#ifndef UList_entry_cxx
#define UList_entry_cxx


//---------------------------------------------------------------------------
%include "src/OpenFOAM/containers/Lists/UList/UList.cxx"
%include "src/OpenFOAM/db/dictionary/entry.cxx"

%ignore Foam::UList< Foam::entry >::writeEntry;
%ignore Foam::UList< Foam::entry >::swap;
                                      
%ignore Foam::UList< Foam::entry >::operator>;
%ignore Foam::UList< Foam::entry >::operator<;
%ignore Foam::UList< Foam::entry >::operator>=;
%ignore Foam::UList< Foam::entry >::operator<=;

%template( UList_entry ) Foam::UList< Foam::entry >; 

%extend Foam::UList< Foam::entry >
{
    int __len__()
    {
        return self->size();
    }
}


//---------------------------------------------------------------------------
#endif

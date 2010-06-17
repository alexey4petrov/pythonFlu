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
#ifndef UList_word_cxx
#define UList_word_cxx


//---------------------------------------------------------------------------
%ignore Foam::UList< Foam::word >::writeEntry;

%include "src/OpenFOAM/containers/Lists/UList/UList.cxx"
%include "src/OpenFOAM/primitives/strings/word.cxx"

%template( UList_word ) Foam::UList< Foam::word >; 

%template( TContainer_word_iterator ) Foam::TContainer_iterator<  Foam::UList< Foam::word > >;

ULISTBASED_ADDONS( Foam::word );


//---------------------------------------------------------------------------
#endif

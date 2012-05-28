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
#ifndef UList_token_cxx
#define UList_token_cxx


//---------------------------------------------------------------------------
%module "Foam.src.OpenFOAM.containers.Lists.UList.UList_token";
%{
   #include "Foam/src/OpenFOAM/containers/Lists/UList/UList_token.hh"
%}


//---------------------------------------------------------------------------
%import "Foam/src/OpenFOAM/containers/Lists/UList/UList.cxx"

%import "Foam/src/OpenFOAM/db/IOstreams/token.cxx"

%ignore Foam::UList< Foam::token >::operator >;
%ignore Foam::UList< Foam::token >::operator <;

%ignore Foam::UList< Foam::token >::operator >=;
%ignore Foam::UList< Foam::token >::operator <=;

%ignore Foam::UList< Foam::token >::operator ==;
%ignore Foam::UList< Foam::token >::operator !=;

%ignore Foam::UList< Foam::token >::writeEntry;

TEMPLATE_ULIST_ITERATOR( token );

%template( UList_token ) Foam::UList< Foam::token >; 

%extend Foam::UList< Foam::token >
{
  ULISTBASED_ADDONS( Foam::token );
}


//---------------------------------------------------------------------------
#endif

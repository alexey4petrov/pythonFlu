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
#ifndef UList_complexVector_cxx
#define UList_complexVector_cxx


//---------------------------------------------------------------------------
%module "Foam.src.OpenFOAM.containers.Lists.UList.UList_complexVector";
%{
   #include "Foam/src/OpenFOAM/containers/Lists/UList/UList_complexVector.hh"
%}


//---------------------------------------------------------------------------
%import "Foam/src/OpenFOAM/containers/Lists/UList/UList.cxx"

%import "Foam/src/OpenFOAM/containers/Lists/UList/UList_vector.cxx"

%import "Foam/src/OpenFOAM/primitives/complexVector.cxx"

ULIST_TYPEMAP( complexVector );

%ignore Foam::UList< Foam::complexVector >::operator >;
%ignore Foam::UList< Foam::complexVector >::operator <;

%ignore Foam::UList< Foam::complexVector >::operator >=;
%ignore Foam::UList< Foam::complexVector >::operator <=;

%template( UList_complexVector ) Foam::UList< Foam::complexVector >; 

%extend Foam::UList< Foam::complexVector > 
{
  ULISTBASED_ADDONS( Foam::complexVector );
}


//---------------------------------------------------------------------------
%define ULIST_COMPLEX_VECTOR_OPERATORS
  Foam::Field< Foam::complexVector > __rxor__( const Foam::UList< Foam::vector >& theArg ) const
  {
    return theArg ^ get_ref( self );
  }
%enddef


//---------------------------------------------------------------------------
%extend Foam::UList< Foam::complexVector > 
{
  ULIST_COMPLEX_VECTOR_OPERATORS;
}


//---------------------------------------------------------------------------
#endif

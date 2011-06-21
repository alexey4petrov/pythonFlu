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
#ifndef isinstance_hxx
#define isinstance_hxx


//---------------------------------------------------------------------------
%{
  #include "Foam/src/isinstance.hh"
%}


//---------------------------------------------------------------------------
//It is assistant function for check argument's.

%define ISINSTANCE_EXTEND( Type )
  static void ext_isinstance( const Type& theArg ) throw( Python::TypeError ){ }
%enddef


//----------------------------------------------------------------------------
%define ISINSTANCE_TEMPLATE_1_EXTEND( Template, Type1 )
  static void ext_isinstance( const Foam::Template< Type1 >& theArg ) throw( Python::TypeError ) {}
%enddef


//----------------------------------------------------------------------------
%define ISINSTANCE_TEMPLATE_2_EXTEND( Template, Type1, Type2 ) 
  static void ext_isinstance( const Foam::Template< Type1, Type2 >& theArg )  throw( Python::TypeError ) {}
%enddef


//----------------------------------------------------------------------------
%define ISINSTANCE_TEMPLATE_3_EXTEND( Template, Type1, Type2, Type3 )
  static void ext_isinstance( const Foam::Template< Type1, Type2, Type3 >& theArg ) throw( Python::TypeError ) {}
%enddef


//---------------------------------------------------------------------------
#endif


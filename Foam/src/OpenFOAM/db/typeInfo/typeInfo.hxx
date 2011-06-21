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
#ifndef typeInfo_hxx
#define typeInfo_hxx


//---------------------------------------------------------------------------
%import "Foam/src/OpenFOAM/db/typeInfo/className.hxx"

%include <typeInfo.H>


//---------------------------------------------------------------------------
%define _DIRECTOR_EXTENDS( TSource, TTarget )
static Foam::TTarget& ext_refCast( Foam::TSource& theArg )
{
  Foam::TTarget& res = refCast< TTarget >( theArg );

  if ( SwigDirector_##TTarget* director = dynamic_cast< SwigDirector_##TTarget* >( &res ) )
    return *director;
  
  return res;
}
%enddef

//---------------------------------------------------------------------------
%define _TYPEINFO_EXTENDS( TSource, TTarget )
static Foam::TTarget& ext_refCast( Foam::TSource& theArg )
{
  return refCast< TTarget >( theArg );
}
%enddef


//--------------------------------------------------------------------------
%define _IS_EXTENDS( TSource, TTarget ) 
static bool ext_isA(const Foam::TSource& theArg )
{
  return isA< TTarget >( theArg );
}
static bool ext_isType(const Foam::TSource& theArg )
{
  return isType< TTarget >( theArg );
}

%enddef


//---------------------------------------------------------------------------
%define TYPEINFO_EXTENDS( TSource, TTarget )
  _IS_EXTENDS( TSource, TTarget ) 
  _TYPEINFO_EXTENDS( TSource, TTarget )
%enddef


//---------------------------------------------------------------------------
%define TYPEINFO_DIRECTOR_EXTENDS( TSource, TTarget )
  _IS_EXTENDS( TSource, TTarget ) 
  _DIRECTOR_EXTENDS( TSource, TTarget )
%enddef


//---------------------------------------------------------------------------
#endif


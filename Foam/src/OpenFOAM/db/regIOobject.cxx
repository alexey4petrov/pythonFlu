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
#ifndef regIOobject_cxx
#define regIOobject_cxx


//---------------------------------------------------------------------------
%module( directors="1", allprotected="1" ) "Foam.src.OpenFOAM.db.regIOobject";
%{
  #include "Foam/src/OpenFOAM/db/regIOobject.hh"
%}

%import "Foam/src/director.hxx"


//---------------------------------------------------------------------------
%import "Foam/src/OpenFOAM/db/IOobject.cxx"


//---------------------------------------------------------------------------
%feature( "director" ) regIOobject;

DIRECTOR_PRE_EXTENDS( regIOobject );


//---------------------------------------------------------------------------
%ignore Foam::regIOobject::writeObject;

#if FOAM_REF_VERSION( >=, 020000 )
  %ignore Foam::regIOobject::fileCheckTypesNames;
#endif

%include <regIOobject.H>


//---------------------------------------------------------------------------
%extend Foam::regIOobject
{
  DIRECTOR_EXTENDS( regIOobject );
}


//---------------------------------------------------------------------------
#endif

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
%module "Foam.src.OpenFOAM.fields.tmp.autoPtr_basicSource"
%{
  #include "Foam/src/OpenFOAM/fields/tmp/autoPtr_basicSource.hh"
%}


//---------------------------------------------------------------------------
%import "Foam/src/common.hxx"

#if FOAM_VERSION( <, 010701 )
#define autoPtr_basicSource_cxx
#endif


//---------------------------------------------------------------------------
#ifndef autoPtr_basicSource_cxx
#define autoPtr_basicSource_cxx


//---------------------------------------------------------------------------
%import "Foam/src/OpenFOAM/fields/tmp/autoPtr.cxx"

%include "Foam/src/finiteVolume/cfdTools/general/fieldSources/basicSource/basicSource/basicSource.cxx"


//---------------------------------------------------------------------------
AUTOPTR_TYPEMAP( Foam::basicSource )

%ignore Foam::autoPtr< Foam::basicSource >::operator->;

%template( autoPtr_basicSource ) Foam::autoPtr< Foam::basicSource >;


//------------------------------------------------------------------------------
%feature( "pythonappend" ) Foam::autoPtr< Foam::basicSource >::SMARTPTR_PYAPPEND_GETATTR( autoPtr_basicSource );

%extend Foam::autoPtr< Foam::basicSource >
{
  SMARTPTR_EXTEND_ATTR( autoPtr_basicSource );
}


//---------------------------------------------------------------------------
#endif

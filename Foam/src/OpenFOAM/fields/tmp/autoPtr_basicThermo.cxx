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
#ifndef autoPtr_basicThermo_cxx
#define autoPtr_basicThermo_cxx


//---------------------------------------------------------------------------
%module "Foam.src.OpenFOAM.fields.tmp.autoPtr_basicThermo"
%{
  #include "src/OpenFOAM/fields/tmp/autoPtr_basicThermo.hh"
%}


//---------------------------------------------------------------------------
%import "src/OpenFOAM/fields/tmp/autoPtr.cxx"

%include "src/thermophysicalModels/basic/basicThermo.cpp"


//----------------------------------------------------------------------------
%ignore Foam::autoPtr< Foam::basicThermo >::operator->;

%template( autoPtr_basicThermo ) Foam::autoPtr< Foam::basicThermo >;


//------------------------------------------------------------------------------
%feature( "pythonappend" ) Foam::autoPtr< Foam::basicThermo >::SMARTPTR_PYAPPEND_GETATTR( autoPtr_basicThermo );

%extend Foam::autoPtr< Foam::basicThermo >
{
  SMARTPTR_EXTEND_ATTR( autoPtr_basicThermo );
}


//---------------------------------------------------------------------------
#endif

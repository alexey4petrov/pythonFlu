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
%module "Foam.src.OpenFOAM.fields.tmp.autoPtr_basicPsiThermo"
%{
  #include "Foam/src/OpenFOAM/fields/tmp/autoPtr_basicPsiThermo.hh"
%}


//---------------------------------------------------------------------------
%import "Foam/src/common.hxx"

#if FOAM_VERSION( <, 010600 )
#define autoPtr_basicPsiThermo_cxx
#endif


//---------------------------------------------------------------------------
#ifndef autoPtr_basicPsiThermo_cxx
#define autoPtr_basicPsiThermo_cxx


//---------------------------------------------------------------------------
%import "Foam/src/OpenFOAM/fields/tmp/autoPtr.cxx"

%include "Foam/src/thermophysicalModels/basic/psiThermo/basicPsiThermo.cpp"


//---------------------------------------------------------------------------
AUTOPTR_TYPEMAP( Foam::basicPsiThermo )

%ignore Foam::autoPtr< Foam::basicPsiThermo >::operator->;

%template( autoPtr_basicPsiThermo ) Foam::autoPtr< Foam::basicPsiThermo >;


//------------------------------------------------------------------------------
%feature( "pythonappend" ) Foam::autoPtr< Foam::basicPsiThermo >::SMARTPTR_PYAPPEND_GETATTR( autoPtr_basicPsiThermo );

%extend Foam::autoPtr< Foam::basicPsiThermo >
{
  SMARTPTR_EXTEND_ATTR( autoPtr_basicPsiThermo );
}


//---------------------------------------------------------------------------
#endif

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
//  Author : Alexey PETROV, Andrey SIMURZIN


//---------------------------------------------------------------------------
#ifndef incompressible_LESModelHolder_cpp
#define incompressible_LESModelHolder_cpp


//---------------------------------------------------------------------------
%{
  #include "Foam/ext/common/turbulenceModels/managedFlu/incompressible_LESModelHolder.hh"
%}


//---------------------------------------------------------------------------
%include "Foam/ext/common/turbulenceModels/shared_ptr/shared_ptr_incompressible_LESModel.hpp"

%import "Foam/src/OpenFOAM/fields/tmp/autoPtr_incompressible_turbulenceModel.cxx"

%import "Foam/src/transportModels/incompressible/transportModel.cxx"

INCLUDE_FILENAME(LESModelHolder,hpp)


//---------------------------------------------------------------------------
%feature( "pythonappend" ) Foam::incompressible::LESModelHolder::SMARTPTR_PYAPPEND_GETATTR( LESModelHolder );

%extend Foam::incompressible::LESModelHolder
{
  SMARTPTR_EXTEND_ATTR( LESModelHolder );
  HOLDERS_CALL_SHARED_PTR_EXTENSION( incompressible::LESModel );
}


//--------------------------------------------------------------------------------------
#endif

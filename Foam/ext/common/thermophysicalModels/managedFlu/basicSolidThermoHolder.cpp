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
%{
  #include "Foam/ext/common/thermophysicalModels/managedFlu/basicSolidThermoHolder.hh"
%}


//---------------------------------------------------------------------------
%import "Foam/src/common.hxx"

#if FOAM_VERSION( <, 020000 )   
#define basicSolidThermoHolder_cpp
#endif


//---------------------------------------------------------------------------
#ifndef basicSolidThermoHolder_cpp
#define basicSolidThermoHolder_cpp


//---------------------------------------------------------------------------
%import "Foam/ext/common/managedFlu/DependentHolder.cxx"

%import "Foam/src/finiteVolume/fvMesh/fvMeshes.cxx"

%include "Foam/ext/common/thermophysicalModels/shared_ptr/shared_ptr_basicSolidThermo.hpp"

INCLUDE_FILENAME(basicSolidThermoHolder,hpp);

//---------------------------------------------------------------------------
%feature( "pythonappend" ) Foam::basicSolidThermoHolder::SMARTPTR_PYAPPEND_GETATTR( basicSolidThermoHolder );

%extend Foam::basicSolidThermoHolder
{
  HOLDERS_CALL_SHARED_PTR_EXTENSION( basicSolidThermo );
  SMARTPTR_EXTEND_ATTR( basicSolidThermoHolder );
}


//--------------------------------------------------------------------------------------
#endif

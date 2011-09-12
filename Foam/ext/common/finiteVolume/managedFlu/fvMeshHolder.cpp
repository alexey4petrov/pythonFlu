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
#ifndef fvMeshHolder_cpp
#define fvMeshHolder_cpp


//---------------------------------------------------------------------------
%{
  #include "Foam/ext/common/finiteVolume/managedFlu/fvMeshHolder.hh"
%}


//---------------------------------------------------------------------------
%import "Foam/ext/common/managedFlu/commonHolder.hxx"

%include "Foam/ext/common/finiteVolume/shared_ptr/shared_ptr_fvMesh.hpp"

%import "Foam/ext/common/managedFlu/DependentHolder.cxx"

%import "Foam/src/OpenFOAM/db/objectRegistry.cxx"

%include <fvMeshHolder.hpp>


//---------------------------------------------------------------------------
%feature( "pythonappend" ) Foam::fvMeshHolder::SMARTPTR_PYAPPEND_GETATTR( fvMeshHolder );

%extend Foam::fvMeshHolder
{
  SMARTPTR_EXTEND_ATTR( fvMeshHolder );
  HOLDERS_CALL_SHARED_PTR_EXTENSION( fvMesh );
}


//--------------------------------------------------------------------------------------
#endif

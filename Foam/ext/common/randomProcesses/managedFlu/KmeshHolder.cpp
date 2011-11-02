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
#ifndef KmeshHolder_cpp
#define KmeshHolder_cpp


//---------------------------------------------------------------------------
%{
  #include "Foam/ext/common/randomProcesses/managedFlu/KmeshHolder.hh"
%}


//---------------------------------------------------------------------------
%import "Foam/ext/common/managedFlu/commonHolder.hxx"

%include "Foam/ext/common/randomProcesses/smart_tmp/smart_tmp_Kmesh.hpp"

%import "Foam/ext/common/managedFlu/DependentHolder.cxx"

%import "Foam/src/OpenFOAM/fields/Fields/primitiveFields.cxx"

%include <KmeshHolder.hpp>


//---------------------------------------------------------------------------
%feature( "pythonappend" ) Foam::KmeshHolder::SMARTPTR_PYAPPEND_GETATTR( KmeshHolder );

%extend Foam::KmeshHolder
{
  SMARTPTR_EXTEND_ATTR( KmeshHolder );
  HOLDERS_CALL_SMART_TMP_EXTENSION( Kmesh );
}


//--------------------------------------------------------------------------------------
#endif

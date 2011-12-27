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
#ifndef vectorFieldHolder_cpp
#define vectorFieldHolder_cpp


//---------------------------------------------------------------------------
%{
  #include "Foam/ext/common/OpenFOAM/managedFlu/vectorFieldHolder.hh"
%}


//---------------------------------------------------------------------------
%include "Foam/ext/common/OpenFOAM/smart_tmp/smart_tmp_vectorField.hpp"

%include "Foam/ext/common/OpenFOAM/managedFlu/FieldHolder.hxx"

%include <primitiveFields.hpp>

%template ( vectorFieldHolder ) Foam::FieldHolder< Foam::vector >;


//---------------------------------------------------------------------------
%feature( "pythonappend" ) Foam::FieldHolder< Foam::vector >::SMARTPTR_PYAPPEND_GETATTR( vectorFieldHolder );

%extend Foam::FieldHolder< Foam::vector >
{
  SMARTPTR_EXTEND_ATTR( vectorFieldHolder );
}



//--------------------------------------------------------------------------------------
#endif

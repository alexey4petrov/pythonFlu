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
#ifndef twoPhaseMixtureHolder_cpp
#define twoPhaseMixtureHolder_cpp


//---------------------------------------------------------------------------
%{
  #include "Foam/ext/common/transportModels/managedFlu/incompressible/twoPhaseMixtureHolder.hh"
%}


//---------------------------------------------------------------------------
%import "Foam/src/transportModels/incompressible/transportModel.cxx"

%include "Foam/ext/common/transportModels/shared_ptr/shared_ptr_twoPhaseMixture.hpp"

%include <twoPhaseMixtureHolder.hpp>


//--------------------------------------------------------------------------
%feature( "pythonappend" ) Foam::twoPhaseMixtureHolder::SMARTPTR_PYAPPEND_GETATTR( twoPhaseMixtureHolder );

%extend Foam::twoPhaseMixtureHolder
{
  SMARTPTR_EXTEND_ATTR( twoPhaseMixtureHolder );
  HOLDERS_CALL_SHARED_PTR_EXTENSION( twoPhaseMixture );
}

NO_HOLDER_TYPEMAP( Foam::twoPhaseMixture );


//--------------------------------------------------------------------------
#endif

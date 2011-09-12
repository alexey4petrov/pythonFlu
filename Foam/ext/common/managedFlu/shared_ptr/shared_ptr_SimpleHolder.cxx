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
#ifndef shared_ptr_SimpleHolder_cxx
#define shared_ptr_SimpleHolder_cxx


//---------------------------------------------------------------------------
%module "Foam.ext.common.managedFlu.shared_ptr.shared_ptr_SimpleHolder"
%{
  #include "Foam/ext/common/managedFlu/shared_ptr/shared_ptr_SimpleHolder.hh"
%}

%include "Foam/ext/common/shared_ptr.hxx"

%import "Foam/ext/common/managedFlu/SimpleHolder.cxx"

SHAREDPTR_TYPEMAP( Foam::SimpleHolder );

//%ignore boost::shared_ptr< Foam::SimpleHolder >::operator->;

%template( shared_ptr_SimpleHolder ) boost::shared_ptr< Foam::SimpleHolder >;


//---------------------------------------------------------------------------
#endif

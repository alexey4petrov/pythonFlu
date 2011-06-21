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
//


//---------------------------------------------------------------------------
#ifndef autoPtr_motionSolver_cxx
#define autoPtr_motionSolver_cxx


//---------------------------------------------------------------------------
%module "Foam.src.OpenFOAM.fields.tmp.autoPtr_motionSolver"
%{
  #include "Foam/src/OpenFOAM/fields/tmp/autoPtr_motionSolver.hh"
%}


//---------------------------------------------------------------------------
%import "Foam/src/OpenFOAM/fields/tmp/autoPtr.cxx"

%include "Foam/src/dynamicMesh/motionSolver.cpp"


//----------------------------------------------------------------------------
%ignore Foam::autoPtr< Foam::motionSolver >::operator->;

%template( autoPtr_motionSolver ) Foam::autoPtr< Foam::motionSolver >;


//------------------------------------------------------------------------------
%feature( "pythonappend" ) Foam::autoPtr< Foam::motionSolver >::SMARTPTR_PYAPPEND_GETATTR( autoPtr_motionSolver );

%extend Foam::autoPtr< Foam::motionSolver >
{
  SMARTPTR_EXTEND_ATTR( autoPtr_motionSolver );
}


//---------------------------------------------------------------------------
#endif

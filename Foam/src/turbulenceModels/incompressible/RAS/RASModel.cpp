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
%{
  #include "Foam/src/turbulenceModels/incompressible/RAS/RASModel.hh"
%}


//---------------------------------------------------------------------------
%import "Foam/src/common.hxx"

#if FOAM_VERSION( <, 010500 )
#define incompressibleRASModel_cpp
#endif


//-----------------------------------------------------------------------------
#ifndef incompressibleRASModel_cpp
#define incompressibleRASModel_cpp


//----------------------------------------------------------------------------
%import "Foam/src/OpenFOAM/fields/tmp/autoPtr_incompressible_turbulenceModel.cxx"

%import "Foam/src/finiteVolume/fvMesh/fvMeshes.cxx"

%import "Foam/src/finiteVolume/fvMatrices/fvMatrices.cxx"

%import "Foam/src/transportModels/incompressible/transportModel.cxx"

%import "Foam/src/OpenFOAM/db/IOdictionary.cxx"

%import "Foam/src/OpenFOAM/db/Switch.cxx"

%import "Foam/src/finiteVolume/cfdTools/general/bound.cxx"


//----------------------------------------------------------------------------
%ignore Foam::incompressible::RASModel::k;

%ignore Foam::incompressible::RASModel::epsilon;

%ignore Foam::incompressible::RASModel::nut;

%rename( incompressible_RASModel ) Foam::incompressible::RASModel;

#if FOAM_NOT_BRANCH( __FREEFOAM__ )
%include <incompressible/RASModel.H>
#else
%include <incompressibleRASModels/RASModel.H>
#endif


//---------------------------------------------------------------------------
%extend Foam::incompressible::RASModel
{
  Foam::volScalarField& ext_k()
  {
    return self->k()();
  }
  Foam::volScalarField& ext_epsilon()
  {
    return self->epsilon()();
  }
  Foam::volScalarField& ext_nut()
  {
    return self->nut()();
  }
}


//---------------------------------------------------------------------------
%include "Foam/ext/common/turbulenceModels/managedFlu/incompressible_RASModelHolder.cpp"


//---------------------------------------------------------------------------
#endif

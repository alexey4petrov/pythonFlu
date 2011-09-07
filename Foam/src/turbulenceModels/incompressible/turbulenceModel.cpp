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
  #include "Foam/src/turbulenceModels/incompressible/turbulenceModel.hh"
%}


//---------------------------------------------------------------------------
%import "Foam/src/common.hxx"

#if FOAM_VERSION( ==, 010500 )   
#define incompressibleturbulenceModel_cpp
#endif

//---------------------------------------------------------------------------
#ifndef incompressibleturbulenceModel_cpp
#define incompressibleturbulenceModel_cpp


//---------------------------------------------------------------------------
%import "Foam/src/OpenFOAM/fields/Fields/primitiveFields.cxx"

%import "Foam/src/OpenFOAM/fields/tmp/autoPtr.cxx"

%import "Foam/src/finiteVolume/fvMesh/fvMeshes.cxx"

%import "Foam/src/finiteVolume/fvMatrices/fvMatrices.cxx"

%import "Foam/src/OpenFOAM/db/typeInfo/typeInfo.hxx"

%import "Foam/src/transportModels/incompressible/transportModel.cxx"


//------------------------------------------------------------------------
//There is no namespace "incompressible" in OpenFOAM-1.4.1-dev
#if FOAM_VERSION( <, 010500 )   
%rename( incompressible_turbulenceModel ) Foam::turbulenceModel;

%ignore Foam::turbulenceModel::nut;

%include <incompressible/turbulenceModel.H>
    
%extend Foam::turbulenceModel  
{
  Foam::ext_tmp< Foam::volScalarField > ext_nut()
  {
    return self->nut();
  }
}
#endif


//-------------------------------------------------------------------------
#if FOAM_VERSION( >=, 010600 )
%rename( incompressible_turbulenceModel ) Foam::incompressible::turbulenceModel;
    
%ignore Foam::incompressible::turbulenceModel::nut;

#if FOAM_VERSION( >=, 020000 )
%ignore Foam::incompressible::turbulenceModel::nu;
#endif


#if FOAM_NOT_BRANCH( __FREEFOAM__ )
%include <incompressible/turbulenceModel.H>
#else
%include <incompressibleTurbulenceModel/turbulenceModel.H>
#endif 
  
%extend Foam::incompressible::turbulenceModel  
{
  Foam::ext_tmp< Foam::volScalarField > ext_nut()
  {
    return self->nut();
  }
#if FOAM_VERSION( >=, 020000 )
  Foam::ext_tmp< Foam::volScalarField > ext_nu()
  {
    return self->nu()();
  }
#endif

}
#endif


//---------------------------------------------------------------------------
#endif

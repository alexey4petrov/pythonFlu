//  VulaSHAKA (Simultaneous Neutronic, Fuel Performance, Heat And Kinetics Analysis)
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
//  See https://vulashaka.svn.sourceforge.net/svnroot/vulashaka
//
//  Author : Alexey PETROV


//---------------------------------------------------------------------------
%module "Foam.src.turbulenceModels.incompressible.turbulenceModel";
%{
  #include "src/turbulenceModels/incompressible/turbulenceModel.hh"
%}


//---------------------------------------------------------------------------
%import "src/common.hxx"

#if FOAM_VERSION( ==, 010500 )   
#define incompressibleturbulenceModel_cxx
#endif

//---------------------------------------------------------------------------
#ifndef incompressibleturbulenceModel_cxx
#define incompressibleturbulenceModel_cxx


//---------------------------------------------------------------------------
%import "src/OpenFOAM/fields/Fields/primitiveFields.cxx"

%import "src/OpenFOAM/fields/tmp/autoPtr.cxx"

%import "src/finiteVolume/fvMesh/fvMeshes.cxx"

%import "src/finiteVolume/fvMatrices/fvMatrices.cxx"

%import "src/OpenFOAM/db/typeInfo/typeInfo.hxx"

%import "src/transportModels/incompressible/transportModel.cxx"


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

%include <incompressible/turbulenceModel.H>
   
%extend Foam::incompressible::turbulenceModel  
{
  Foam::ext_tmp< Foam::volScalarField > ext_nut()
  {
    return self->nut();
  }
}
#endif


//---------------------------------------------------------------------------
#endif

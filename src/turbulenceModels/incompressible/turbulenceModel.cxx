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
//  See https://csrcs.pbmr.co.za/svn/nea/prototypes/reaktor/pyfoam
//
//  Author : Alexey PETROV


//---------------------------------------------------------------------------
#ifndef incompressibleturbulenceModel_cxx
#define incompressibleturbulenceModel_cxx


//---------------------------------------------------------------------------
%include "src/OpenFOAM/fields/Fields/primitiveFields.cxx"

%include "src/OpenFOAM/fields/tmp/autoPtr.cxx"

%include "src/finiteVolume/fields/volFields/volFields.cxx"

%include "src/finiteVolume/fields/surfaceFields/surfaceFields.cxx"

%include "src/finiteVolume/fvMatrices/fvMatrices.cxx"

%include "src/OpenFOAM/db/typeInfo/typeInfo.hxx"

%include "src/transportModels/incompressible/transportModel.cxx"

%{
    #include "incompressible/turbulenceModel/turbulenceModel.H"
%}


//------------------------------------------------------------------------
//There is no namespace "incompressible" in OpenFOAM-1.4.1-dev

#if ( __FOAM_VERSION__ < 010500 )   
%rename( incompressible_turbulenceModel ) Foam::turbulenceModel;

#endif


//-------------------------------------------------------------------------
#if ( __FOAM_VERSION__ >= 010500 )   

%rename( incompressible_turbulenceModel ) Foam::incompressible::turbulenceModel;


#endif



//--------------------------------------------------------------------------
%include "incompressible/turbulenceModel.H"


//---------------------------------------------------------------------------
#endif

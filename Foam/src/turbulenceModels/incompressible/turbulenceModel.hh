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
#include "Foam/src/common.hh"

#if FOAM_VERSION( ==, 010500 )   
#define incompressibleturbulenceModel_hh
#endif

//---------------------------------------------------------------------------
#ifndef incompressibleturbulenceModel_hh
#define incompressibleturbulenceModel_hh


//---------------------------------------------------------------------------
#include "Foam/src/OpenFOAM/fields/Fields/primitiveFields.hh"

#include "Foam/src/OpenFOAM/fields/tmp/autoPtr.hh"

#include "Foam/src/finiteVolume/fields/volFields/volFields.hh"

#include "Foam/src/finiteVolume/fields/surfaceFields/surfaceFields.hh"

#include "Foam/src/finiteVolume/fvMatrices/fvMatrices.hh"

#include "Foam/src/transportModels/incompressible/transportModel.hh"

#include "Foam/ext/common/finiteVolume/ext_tmp/ext_tmp_volScalarField.hh"


//------------------------------------------------------------------------
#if FOAM_NOT_BRANCH( __FREEFOAM__ )
  #if FOAM_VERSION( <, 010500 )   
    #include <incompressible/turbulenceModel/turbulenceModel.H>
  #endif

  #if FOAM_VERSION( >=, 010600 )
    #include <incompressible/turbulenceModel/turbulenceModel.H>
  #endif
#else
  #include <incompressibleTurbulenceModel/turbulenceModel.H>
#endif 


//---------------------------------------------------------------------------
#endif

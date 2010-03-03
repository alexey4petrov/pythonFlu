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
#if ( __FOAM_VERSION__ < 010600 )
%include "src/common.hxx"
#define compressibleRASModel_cxx
#endif


//-----------------------------------------------------------------------------
#ifndef compressibleRASModel_cxx
#define compressibleRASModel_cxx

//---------------------------------------------------------------------------
//It is necessary to include "director's" classes above first's DIRECTOR_INCLUDE
%include "src/finiteVolume/directors.hxx"


//----------------------------------------------------------------------------
%include "src/turbulenceModels/compressible/turbulenceModel.cxx"

%include "src/finiteVolume/fields/volFields/volFields.cxx"

%include "src/finiteVolume/fields/surfaceFields/surfaceFields.cxx"

%include "src/finiteVolume/fvMatrices/fvMatrices.cxx"

%include "src/thermophysicalModels/basic/basicThermo.cxx"

%{
    #include "compressible/RAS/RASModel/RASModel.H"
%}

%rename( compressible_RASModel ) Foam::compressible::RASModel;

%include "compressible/RASModel.H"


//---------------------------------------------------------------------------
#endif

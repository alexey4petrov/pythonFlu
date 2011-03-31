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
%include "src/common.hxx"
#if FOAM_VERSION( <, 010500 )
#define compressibleRASModel_cxx
#endif


//-----------------------------------------------------------------------------
#ifndef compressibleRASModel_cxx
#define compressibleRASModel_cxx

//---------------------------------------------------------------------------
// Keep on corresponding "director" includes at the top of SWIG defintion file

%include "src/OpenFOAM/directors.hxx"

%include "src/finiteVolume/directors.hxx"


//----------------------------------------------------------------------------
%include "src/turbulenceModels/compressible/turbulenceModel.cxx"

%include "src/finiteVolume/fields/volFields/volFields.cxx"

%include "src/finiteVolume/fields/surfaceFields/surfaceFields.cxx"

%include "src/finiteVolume/fvMatrices/fvMatrices.cxx"

%include "src/thermophysicalModels/basic/basicThermo.cxx"


//----------------------------------------------------------------------------
#if  FOAM_VERSION( ==, 010500 )
%{
    #include "RAS/compressible/RASModel/RASModel.H"
%}
#endif

#if FOAM_VERSION( >=, 010600 )
%{
    #include "compressible/RAS/RASModel/RASModel.H"
%}
#endif


//-----------------------------------------------------------------------------
%rename( compressible_RASModel ) Foam::compressible::RASModel;

%include "compressible/RASModel.H"


//---------------------------------------------------------------------------
#endif

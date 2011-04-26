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
%module "Foam.src.OpenFOAM.fields.tmp.autoPtr_compressible_turbulenceModel"
%{
  #include "src/OpenFOAM/fields/tmp/autoPtr_compressible_turbulenceModel.hh"
%}


//---------------------------------------------------------------------------
%import "src/common.hxx"

#if FOAM_VERSION( ==, 010500 )   
#define autoPtr_compressible_turbulenceModel_cxx
#endif


//---------------------------------------------------------------------------
#ifndef autoPtr_compressible_turbulenceModel_cxx
#define autoPtr_compressible_turbulenceModel_cxx


//---------------------------------------------------------------------------
%import "src/OpenFOAM/fields/tmp/autoPtr.cxx"

%include "src/turbulenceModels/compressible/turbulenceModel.cpp"


//----------------------------------------------------------------------------
AUTOPTR_TYPEMAP( Foam::compressible::turbulenceModel )

%ignore Foam::autoPtr< Foam::compressible::turbulenceModel >::operator->;

%template( autoPtr_compressible_turbulenceModel ) Foam::autoPtr< Foam::compressible::turbulenceModel >;


//------------------------------------------------------------------------------
%feature( "pythonappend" ) Foam::autoPtr< Foam::compressible::turbulenceModel >::SMARTPTR_PYAPPEND_GETATTR( autoPtr_compressible_turbulenceModel );

%extend Foam::autoPtr< Foam::compressible::turbulenceModel >
{
  SMARTPTR_EXTEND_ATTR( autoPtr_compressible_turbulenceModel );
}


//---------------------------------------------------------------------------
#endif

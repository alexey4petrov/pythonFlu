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
%module "Foam.src.OpenFOAM.fields.tmp.autoPtr_incompressible_LESModel"
%{
  #include "src/OpenFOAM/fields/tmp/autoPtr_incompressible_LESModel.hh"
%}


//---------------------------------------------------------------------------
%import "src/common.hxx"

#if FOAM_VERSION( <, 010500 )
#define autoPtr_incompressible_LESModel_cxx
#endif


//-----------------------------------------------------------------------------
#ifndef autoPtr_incompressible_LESModel_cxx
#define autoPtr_incompressible_LESModel_cxx


//---------------------------------------------------------------------------
%import "src/OpenFOAM/fields/tmp/autoPtr.cxx"

%include "src/turbulenceModels/incompressible/LES/LESModel.cpp"


//----------------------------------------------------------------------------
AUTOPTR_TYPEMAP( Foam::incompressible::LESModel )

%ignore Foam::autoPtr< Foam::incompressible::LESModel >::operator->;

%template( autoPtr_incompressible_LESModel ) Foam::autoPtr< Foam::incompressible::LESModel >;


//------------------------------------------------------------------------------
%feature( "pythonappend" ) Foam::autoPtr< Foam::incompressible::LESModel >::SMARTPTR_PYAPPEND_GETATTR( autoPtr_incompressible_LESModel );

%extend Foam::autoPtr< Foam::incompressible::LESModel >
{
  SMARTPTR_EXTEND_ATTR( autoPtr_incompressible_LESModel );
}


//---------------------------------------------------------------------------
#endif

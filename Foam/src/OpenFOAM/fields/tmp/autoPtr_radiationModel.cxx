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
//  See http://sourceforge.net/projects/pythonflu
//
//  Author : Alexey PETROV


//---------------------------------------------------------------------------
%module "Foam.src.OpenFOAM.fields.tmp.autoPtr_radiationModel"
%{
  #include "src/OpenFOAM/fields/tmp/autoPtr_radiationModel.hh"
%}


//---------------------------------------------------------------------------
%import "src/common.hxx"

#if FOAM_VERSION( <, 010500 )
#define autoPtr_radiationModel_cxx
#endif


//-----------------------------------------------------------------------------
#ifndef autoPtr_radiationModel_cxx
#define autoPtr_radiationModel_cxx


//---------------------------------------------------------------------------
%import "src/OpenFOAM/fields/tmp/autoPtr.cxx"

%include "src/thermophysicalModels/radiation/radiationModel/radiationModel.cpp"


//-----------------------------------------------------------------------------
AUTOPTR_TYPEMAP( Foam::radiation::radiationModel )

%ignore Foam::autoPtr< Foam::radiation::radiationModel >::operator->;

%template( autoPtr_radiationModel ) Foam::autoPtr< Foam::radiation::radiationModel >;


//------------------------------------------------------------------------------
%feature( "pythonappend" ) Foam::autoPtr< Foam::radiation::radiationModel >::SMARTPTR_PYAPPEND_GETATTR( autoPtr_radiationModel );

%extend Foam::autoPtr< Foam::radiation::radiationModel >
{
  SMARTPTR_EXTEND_ATTR( autoPtr_radiationModel );
}


//---------------------------------------------------------------------------
#endif

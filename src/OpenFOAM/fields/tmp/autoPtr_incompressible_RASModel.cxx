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

#if ( __FOAM_VERSION__ < 010500 )
%include "src/common.hxx"
#define autoPtr_incompressible_RASModel_cxx
#endif


//-----------------------------------------------------------------------------
#ifndef autoPtr_incompressible_RASModel_cxx
#define autoPtr_incompressible_RASModel_cxx


//---------------------------------------------------------------------------
// Keep on corresponding "director" includes at the top of SWIG defintion file

%include "src/OpenFOAM/directors.hxx"

%include "src/finiteVolume/directors.hxx"


//---------------------------------------------------------------------------
%include "src/OpenFOAM/fields/tmp/autoPtr.cxx"

%include "src/turbulenceModels/incompressible/RAS/RASModel.cxx"


//----------------------------------------------------------------------------
AUTOPTR_TYPEMAP( Foam::incompressible::RASModel )

%ignore Foam::autoPtr< Foam::incompressible::RASModel >::operator->;

%template( autoPtr_incompressible_RASModel ) Foam::autoPtr< Foam::incompressible::RASModel >;

%inline
{
  namespace Foam
  {
    typedef autoPtr< incompressible::RASModel > autoPtr_incompressible_RASModel;
  }
}


//------------------------------------------------------------------------------
%feature( "pythonappend" ) Foam::autoPtr< Foam::incompressible::RASModel >::SMARTPTR_PYAPPEND_GETATTR( autoPtr_incompressible_RASModel );

%extend Foam::autoPtr< Foam::incompressible::RASModel >
{
  SMARTPTR_EXTEND_ATTR( autoPtr_incompressible_RASModel )
}

//---------------------------------------------------------------------------
#endif

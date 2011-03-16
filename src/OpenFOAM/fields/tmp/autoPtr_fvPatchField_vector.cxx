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
#ifndef autoPtr_fvPatchField_vector_cxx
#define autoPtr_fvPatchField_vector_cxx


//---------------------------------------------------------------------------
%module "Foam.src.OpenFOAM.fields.tmp.autoPtr_fvPatchField_vector"
%{
  #include "src/OpenFOAM/fields/tmp/autoPtr_fvPatchField_vector.hpp"
%}


//---------------------------------------------------------------------------
%import "src/OpenFOAM/fields/tmp/autoPtr.cxx"

%import "src/finiteVolume/fields/fvPatchFields/fvPatchField_vector.cxx"

%template( autoPtr_fvPatchField_vector ) Foam::autoPtr< Foam::fvPatchField< Foam::vector > >;


//---------------------------------------------------------------------------
%feature( "pythonappend" ) Foam::autoPtr< Foam::fvPatchField< Foam::vector > >::SMARTPTR_PYAPPEND_GETATTR( autoPtr_fvPatchField_vector );

%extend Foam::autoPtr< Foam::fvPatchField< Foam::vector > >
{
  SMARTPTR_EXTEND_ATTR( autoPtr_fvPatchField_vector )
  
  bool operator==( const Foam::UList< Foam::vector >& theArg )
  {
    Foam::UList< Foam::vector >* aSelf = static_cast< Foam::UList< Foam::vector >* >( self->ptr() );
    return *aSelf == theArg;
  }
}


//---------------------------------------------------------------------------
#endif

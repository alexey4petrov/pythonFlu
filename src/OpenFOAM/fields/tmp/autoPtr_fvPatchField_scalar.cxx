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
#ifndef autoPtr_fvPatchField_scalar_cxx
#define autoPtr_fvPatchField_scalar_cxx


//---------------------------------------------------------------------------
%include "src/OpenFOAM/fields/tmp/autoPtr.cxx"

%include "src/finiteVolume/fields/fvPatchFields/fvPatchField_scalar.cxx"

%template( autoPtr_fvPatchField_scalar ) Foam::autoPtr< Foam::fvPatchField< Foam::scalar > >;

%inline
{
    namespace Foam
    {
        typedef autoPtr< fvPatchField< scalar > > autoPtr_fvPatchField_scalar;
    }
}


//---------------------------------------------------------------------------
%feature( "pythonappend" ) Foam::autoPtr< Foam::fvPatchField< Foam::scalar > >::SMARTPTR_PYAPPEND_GETATTR( autoPtr_fvPatchField_scalar );

%extend Foam::autoPtr< Foam::fvPatchField< Foam::scalar > >
{
  SMARTPTR_EXTEND_ATTR( autoPtr_fvPatchField_scalar )
  
  bool operator==( const Foam::UList< Foam::scalar >& theArg )
  {
    Foam::UList< Foam::scalar >* aSelf = static_cast< Foam::UList< Foam::scalar >* >( self->ptr() );
    return *aSelf == theArg;
  }

}


//---------------------------------------------------------------------------
#endif

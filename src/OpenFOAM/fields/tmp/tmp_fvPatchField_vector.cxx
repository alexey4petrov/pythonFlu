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
#ifndef tmp_fvPatchField_vector_cxx
#define tmp_fvPatchField_vector_cxx


//---------------------------------------------------------------------------
%include "src/OpenFOAM/fields/tmp/tmp.cxx"

%include "src/finiteVolume/fields/fvPatchFields/fvPatchField_vector.cxx"

TMP_TYPEMAP( Foam::fvPatchField< Foam::vector > )


//----------------------------------------------------------------------------
%ignore Foam::tmp< Foam::fvPatchField< Foam::vector > >::tmp;

%template( tmp_fvPatchField_vector ) Foam::tmp< Foam::fvPatchField< Foam::vector > >;

%inline
{
  namespace Foam
  {
    typedef tmp< fvPatchField< vector > > tmp_fvPatchField_vector;
  }
}


//----------------------------------------------------------------------------
%feature( "pythonappend" ) Foam::tmp< Foam::fvPatchField< Foam::vector > >::TMP_PYTHONAPPEND_ATTR( tmp_fvPatchField_vector );

%extend Foam::tmp< Foam::fvPatchField< Foam::vector > >
{
  TMP_EXTEND_ATTR( tmp_fvPatchField_vector )
  
  Foam::tmp< Foam::fvPatchField< Foam::vector > >( const  Foam::tmp< Foam::fvPatchField< Foam::vector > >&  theArg ) 
  {
    return new Foam::tmp< Foam::fvPatchField< Foam::vector > >( theArg );
  }
  
  bool operator==( const Foam::UList< Foam::vector >& theArg )
  {
    Foam::UList< Foam::vector >* aSelf = static_cast< Foam::UList< Foam::vector >* >( self->ptr() );
    return *aSelf == theArg;
  }
}


//---------------------------------------------------------------------------
#endif

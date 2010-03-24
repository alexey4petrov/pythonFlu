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
//  See https://csrcs.pbmr.co.za/svn/nea/prototypes/reaktor/pyfoam
//
//  Author : Alexey PETROV


//---------------------------------------------------------------------------
#ifndef vectorField_cxx
#define vectorField_cxx


//---------------------------------------------------------------------------
%include "src/OpenFOAM/fields/Fields/Field.cxx"

%include "src/OpenFOAM/primitives/vector.cxx"

%include "src/OpenFOAM/primitives/Lists/vectorList.cxx"

%include "src/OpenFOAM/primitives/tensor.cxx"
//---------------------------------------------------------------------------
%{
    #include "vectorField.H"
%}

%ignore Foam::Field< Foam::vector >::typeName;
%ignore Foam::Field< Foam::vector >::Field;
%ignore Foam::Field< Foam::vector >::T;

%template( vectorField ) Foam::Field< Foam::vector >; 

%typedef Foam::Field< Foam::vector > vectorField;

FIELD_TEMPLATE_FUNC( vector )


//---------------------------------------------------------------------------
%extend Foam::Field< Foam::vector >
{
  Foam::tmp< Foam::Field< Foam::scalar > > __rand__( const Foam::vector& theArg)
  {
    return theArg & get_ref( self );
  }
  Foam::tmp< Foam::Field< Foam::vector > > __rand__( const Foam::tensor& theArg)
  {
    return theArg & get_ref( self );
  }
}
//---------------------------------------------------------------------------
#endif

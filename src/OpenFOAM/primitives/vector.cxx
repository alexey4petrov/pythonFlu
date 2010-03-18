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
#ifndef vector_cxx
#define vector_cxx


//---------------------------------------------------------------------------
%include "src/common.hxx"

%include "src/OpenFOAM/primitives/scalar.cxx"

%include "src/OpenFOAM/primitives/direction.cxx"

%{
    #include "VectorSpace.H"
    #include "Vector.H"
%}

%include "VectorSpace.H"

%template( VectorSpace_Vector ) Foam::VectorSpace< Foam::Vector< Foam::scalar >, Foam::scalar, 3 >;


//---------------------------------------------------------------------------
%extend Foam::VectorSpace< Foam::Vector< Foam::scalar >, Foam::scalar, 3 >
{
    int __len__()
    {
        return self->size();
    }
    
    Foam::scalar __getitem__( const Foam::direction theIndex )
    {
            return self->operator[]( theIndex );
    }

    void __setitem__( const Foam::direction theIndex, const Foam::scalar& theValue )
    {
        self->operator[]( theIndex ) = theValue;
    }
}


//---------------------------------------------------------------------------
%{
    #include "Vector.H"
%}

%include "Vector.H"


//---------------------------------------------------------------------------
%{
    #include "vector.H"
    #include "Tensor.H"
%}

%include "vector.H"

%template( vector ) Foam::Vector< Foam::scalar >;

%extend Foam::Vector< Foam::scalar >
{
  Foam::Tensor< Foam::scalar > sqr()
  {
     return Foam::sqr( *self );
  }
}


//---------------------------------------------------------------------------
#endif

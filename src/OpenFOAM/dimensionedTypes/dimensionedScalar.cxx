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
#ifndef dimensionedScalar_cxx
#define dimensionedScalar_cxx


//---------------------------------------------------------------------------
%include "src/OpenFOAM/dimensionedTypes/dimensionedType.cxx"

%include "src/OpenFOAM/primitives/scalar.cxx"

%include "src/OpenFOAM/primitives/vector.cxx"

%{
    #include "dimensionedScalar.H"
%}

%ignore Foam::dimensioned< Foam::scalar >::component;
%ignore Foam::dimensioned< Foam::scalar >::replace;
%ignore Foam::dimensioned< Foam::scalar >::T;

%typedef Foam::dimensioned< Foam::scalar > dimensionedScalar;

%typemap( out ) Foam::dimensioned< Foam::scalar >
{
    $result = SWIG_NewPointerObj( ( new $1_type( *&$1 ) ), $&1_descriptor, SWIG_POINTER_OWN |  0 );
}

%template( dimensionedScalar ) Foam::dimensioned< Foam::scalar >; 

%include "dimensionedScalar.H"


//--------------------------------------------------
DIMENSIONEDTYPE_ADDONS( Foam::scalar )

%extend Foam::dimensioned< Foam::scalar >
{
  Foam::dimensioned< Foam::scalar > sqrt()
  {
     return Foam::sqrt( *self );
  }
  Foam::dimensioned< Foam::vector > __rmul__( const Foam::vector& ds )
  {
      return ds * *self;
  }
}


//---------------------------------------------------------------------------
#endif

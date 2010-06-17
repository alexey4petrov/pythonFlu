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
#ifndef dimensionedVector_cxx
#define dimensionedVector_cxx


//---------------------------------------------------------------------------
%include "src/OpenFOAM/dimensionedTypes/dimensionedType.cxx"

%include "src/OpenFOAM/primitives/vector.cxx"

%include "src/OpenFOAM/primitives/tensor.cxx"

%{
    #include "dimensionedVector.H"
%}

%ignore Foam::dimensioned< Foam::vector >::component;
%ignore Foam::dimensioned< Foam::vector >::replace;
%ignore Foam::dimensioned< Foam::vector >::T;

%typedef Foam::dimensioned< Foam::vector > dimensionedVector;

%typemap( out ) Foam::dimensioned< Foam::vector >
{
    $result = SWIG_NewPointerObj( ( new $1_type( *&$1 ) ), $&1_descriptor, SWIG_POINTER_OWN |  0 );
}


//-----------------------------------------------------------------------
PYAPPEND_RETURN_SELF_COMPOUND_OPERATOR_TEMPLATE_1(Foam::dimensioned, Foam::vector, operator+= )


//-----------------------------------------------------------------------
%template( dimensionedVector ) Foam::dimensioned< Foam::vector >; 

%include "dimensionedVector.H"


//------------------------------------------------------------------------
%include "src/try_reverse_operator.hxx"

%feature ("pythonprepend") Foam::dimensioned< Foam::vector >::TRY_REVERSE_PYPREPEND( and );


//-------------------------------------------------------------------------
DIMENSIONEDTYPE_ADDONS( Foam::vector )

%extend Foam::dimensioned< Foam::vector >
{
  Foam::dimensioned< Foam::scalar > __and__( const Foam::dimensioned< Foam::vector >& ds )
  {
     return *self & ds;
  }
  Foam::dimensioned< Foam::vector > __rand__( const Foam::tensor& ds )
  {
     return *self & ds;
  }
}


//---------------------------------------------------------------------------
CLEAR_PYAPPEND_RETURN_SELF_COMPOUND_OPERATOR_TEMPLATE_1(Foam::dimensioned, Foam::vector, operator+= );


//---------------------------------------------------------------------------
#endif

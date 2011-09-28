//  pythonFlu - Python wrapping for OpenFOAM C++ API
//  Copyright (C) 2010- Alexey Petrov
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
#ifndef GeometricField_cpp
#define GeometricField_cpp


//---------------------------------------------------------------------------
%{
  #include "Foam/src/OpenFOAM/fields/GeometricFields/GeometricField.hh"
%}


//---------------------------------------------------------------------------
%include "Foam/src/OpenFOAM/fields/DimensionedFields/DimensionedField.cpp"

%include <GeometricField.H>


//---------------------------------------------------------------------------
%include "Foam/src/OpenFOAM/fields/GeometricFields/TGeometricBoundaryField.hpp"

%include "Foam/src/OpenFOAM/fields/GeometricFields/no_tmp_typemap_GeometricFields.hpp"


//---------------------------------------------------------------------------
%import "Foam/src/compound_operator.hxx"
%import "Foam/src/OpenFOAM/fields/tmp/tmp.cxx"

%import "Foam/src/OpenFOAM/db/objectRegistry.cxx"
%import "Foam/src/OpenFOAM/primitives/label.cxx"

%define __COMMON_GEOMETRIC_FIELD_TEMPLATE_FUNC__( Type, TPatchField, TMesh )
{
  OBJECTREGISTRY_TEMPLATE_3_EXTENDS( GeometricField, Type, TPatchField, TMesh );
    
  ISINSTANCE_TEMPLATE_3_EXTEND( GeometricField, Type, TPatchField, TMesh );
    
  static const TPatchField< Type >&
  ext_lookupPatchField( const Foam::fvPatch& thePatch, const word& theName ) const
  {
    return thePatch.lookupPatchField< Foam::GeometricField< Type, TPatchField, TMesh >, Type >( theName );
  }

  void ext_assign( const Foam::GeometricField< Type, TPatchField, TMesh >& theArg )
  {
    get_ref( self ) = theArg;
  }
    
  void ext_assign( const Foam::dimensioned< Type >& theArg )
  {
    get_ref( self ) = theArg;
  }
  
  Foam::tmp< Foam::GeometricField< Type, TPatchField, TMesh > > __neg__() const
  {
    return -get_ref( self );
  }
  
  Foam::tmp< Foam::GeometricField< Type, TPatchField, TMesh > > __sub__( const Foam::GeometricField< Type, TPatchField, TMesh >& theArg ) const
  {
    return get_ref( self ) - theArg;
  }
  
  Foam::tmp< Foam::GeometricField< Type, TPatchField, TMesh > > __add__( const Foam::GeometricField< Type, TPatchField, TMesh >& theArg ) const
  {
    return get_ref( self ) + theArg;
  }
  
  Foam::tmp< Foam::GeometricField< Type, TPatchField, TMesh > > __add__( const Foam::dimensioned< Type >& theArg ) const
  {
    return get_ref( self ) + theArg;
  }
  
  Foam::tmp< Foam::GeometricField< Type, TPatchField, TMesh > > __sub__( const Foam::dimensioned< Type >& theArg ) const
  {
    return get_ref( self ) - theArg;
  }

  Foam::tmp< Foam::GeometricField< Type, TPatchField, TMesh > > __rsub__( const Foam::dimensioned< Type >& theArg ) const
  {
    return theArg - get_ref( self ) ;
  }
  
  Foam::tmp< Foam::GeometricField< Type, TPatchField, TMesh > > __radd__( const Foam::dimensioned< Type >& theArg ) const 
  {
    return theArg + get_ref( self ) ;
  }
  
  Foam::tmp< Foam::GeometricField< Type, TPatchField, TMesh > > __mul__( const Foam::GeometricField< Foam::scalar, TPatchField, TMesh >& theArg ) const
  {
    return  get_ref( self ) * theArg;
  }
  
  Foam::tmp< Foam::GeometricField< Type, TPatchField, TMesh > > __rmul__( const Foam::GeometricField< Foam::scalar, TPatchField, TMesh >& theArg ) const
  {
    return  theArg * get_ref( self );
  }
  
  Foam::tmp< Foam::GeometricField< Type, TPatchField, TMesh > > __rmul__( const Foam::label& theArg ) const
  {
    return theArg * get_ref( self );
  }
  
  Foam::tmp< Foam::GeometricField< Foam::scalar, TPatchField, TMesh > > mag() const
  {
    return Foam::mag( get_ref( self ) );
  }
  
  Foam::tmp< Foam::GeometricField< Foam::scalar, TPatchField, TMesh > > magSqr() const
  {
    return Foam::magSqr( get_ref( self ) );
  }
  
  Foam::dimensioned< Type > ext_max() const
  {
    return Foam::max( get_ref( self ) );
  }
  
  Foam::tmp< Foam::GeometricField< Type, TPatchField, TMesh > > ext_max( const Foam::GeometricField< Type, TPatchField, TMesh >& theArg ) const
  {
    return Foam::max( get_ref( self ), theArg );
  }
  
  Foam::tmp< Foam::GeometricField< Type, TPatchField, TMesh > > ext_min( const Foam::GeometricField< Type, TPatchField, TMesh >& theArg ) const
  {
    return Foam::min( get_ref( self ), theArg );
  }
  
  Foam::tmp< Foam::GeometricField< Type, TPatchField, TMesh > > ext_max( const Foam::dimensioned< Type >& theArg ) const
  {
    return Foam::max( get_ref( self ), theArg );
  }

  Foam::tmp< Foam::GeometricField< Type, TPatchField, TMesh > > ext_max( const Type& theArg ) const
  {
    return Foam::max( get_ref( self ), theArg );
  }

  Foam::tmp< Foam::GeometricField< Type, TPatchField, TMesh > > ext_min( const Type& theArg ) const
  {
    return Foam::min( get_ref( self ), theArg );
  }
 
  Foam::tmp< Foam::GeometricField< Type, TPatchField, TMesh > > ext_min( const Foam::dimensioned< Type >& theArg ) const
  {
    return Foam::min( get_ref( self ), theArg );
  }
  
  Foam::dimensioned< Type > ext_min() const
  {
    return Foam::min( get_ref( self ) );
  }

  Foam::dimensioned< Type > sum() const
  {
    return Foam::sum( get_ref( self ) );
  }
    
  Foam::dimensioned< Type > average() const
  {
    return Foam::average( get_ref( self ) );
  }    
  
  Foam::TGeometricBoundaryField< Type, TPatchField, TMesh > ext_boundaryField()
  {
    return Foam::TGeometricBoundaryField< Type, TPatchField, TMesh >( get_ref( self ).boundaryField() );
  }
  
  
}
%enddef


//---------------------------------------------------------------------------
%define __COMMON_TMP_GEOMETRIC_FIELD_TEMPLATE_FUNC__( Type )
{
  const Type& __getitem__( const Foam::label& theIndex ) const
  {
    return get_ref( self )[ theIndex ];
  }

  void __setitem__( const Foam::label& theIndex, const Type& theValue )
  {
    get_ref( self )[ theIndex ] = theValue;
  }
}
%enddef


//---------------------------------------------------------------------------
%import "Foam/ext/common/managedFlu/commonHolder.hxx"

%define GEOMETRIC_FIELD_HOLDER_FUNC_EXTEND( Type, TPatchField, TMesh )
%extend Foam::GeometricField< Type, TPatchField, TMesh > FUNCTION_HOLDER_EXTEND_SMART_PTR_TEMPLATE3( Foam::GeometricField, Type, TPatchField, TMesh )

%extend Foam::tmp< Foam::GeometricField< Type, TPatchField, TMesh > >
{
  Foam::GeometricFieldHolder< Type, TPatchField, TMesh > holder( const Deps& theDeps ) const
  {
    return Foam::GeometricFieldHolder< Type, TPatchField, TMesh >( *self, theDeps );
  }
}
%enddef


//---------------------------------------------------------------------------
%define GEOMETRIC_FIELD_TEMPLATE_FUNC( Type, TPatchField, TMesh )

%extend Foam::GeometricField< Type, TPatchField, TMesh > COMMON_EXTENDS;

%import "Foam/src/OpenFOAM/primitives/scalar.cxx"

%extend Foam::GeometricField< Type, TPatchField, TMesh > COMMON_EXTENDS;

%extend Foam::tmp< Foam::GeometricField< Type, TPatchField, TMesh > > COMMON_EXTENDS;

%import "Foam/src/OpenFOAM/db/IOstreams/IOstreams/Ostream.cxx"

%extend Foam::GeometricField< Type, TPatchField, TMesh > OSTREAM_EXTENDS;

%extend Foam::GeometricField< Type, TPatchField, TMesh > __COMMON_GEOMETRIC_FIELD_TEMPLATE_FUNC__( Type, TPatchField, TMesh );

%extend Foam::tmp< Foam::GeometricField< Type, TPatchField, TMesh > > __COMMON_GEOMETRIC_FIELD_TEMPLATE_FUNC__( Type, TPatchField, TMesh );

%extend Foam::tmp< Foam::GeometricField< Type, TPatchField, TMesh > > __COMMON_TMP_GEOMETRIC_FIELD_TEMPLATE_FUNC__( Type );

%enddef


//---------------------------------------------------------------------------
%import "Foam/src/OpenFOAM/primitives/tensor.cxx"
%import "Foam/src/OpenFOAM/primitives/sphericalTensor.cxx"

%define __SCALAR_GEOMETRIC_FIELD_TEMPLATE_FUNC__( TPatchField, TMesh )
{
  Foam::tmp< Foam::GeometricField< Foam::scalar, TPatchField, TMesh > > sqrt() const
  {
    return Foam::sqrt( get_ref( self ) );
  }
  
  Foam::tmp< Foam::GeometricField< Foam::scalar, TPatchField, TMesh > > sqr() const
  {
    return Foam::sqr( get_ref( self ) );
  }
  
  Foam::tmp< Foam::GeometricField< Foam::scalar, TPatchField, TMesh > > __div__( const Foam::GeometricField< Foam::scalar, TPatchField, TMesh >& theArg ) const
  {
    return get_ref( self ) / theArg;
  }
  
  Foam::tmp< Foam::GeometricField< Foam::scalar, TPatchField, TMesh > > __div__( const Foam::dimensioned< Foam::scalar >& theArg ) const
  {
    return get_ref( self ) / theArg;
  }
  
  Foam::tmp< Foam::GeometricField< Foam::scalar, TPatchField, TMesh > > __rdiv__( const Foam::scalar& theArg ) const
  {
    return theArg / get_ref( self );
  }

  Foam::tmp< Foam::GeometricField< Foam::scalar, TPatchField, TMesh > > __rdiv__( const Foam::dimensioned< Foam::scalar >& theArg ) const
  {
    return theArg / get_ref( self );
  }
  
  Foam::tmp< Foam::GeometricField< Foam::scalar, TPatchField, TMesh > > __rmul__( const Foam::scalar& theArg ) const
  {
    return theArg * get_ref( self );
  }
  
  Foam::tmp< Foam::GeometricField< Foam::vector, TPatchField, TMesh > > __rmul__( const Foam::vector& theArg ) const
  {
    return theArg * get_ref( self );
  }
    
  Foam::tmp< Foam::GeometricField< Foam::scalar, TPatchField, TMesh > > __rmul__( const Foam::dimensioned< Foam::scalar >& theArg ) const
  {
    return theArg * get_ref( self ) ;
  }
    
  Foam::tmp< Foam::GeometricField< Foam::scalar, TPatchField, TMesh > > __mul__( const Foam::dimensioned< Foam::scalar >& theArg ) const
  {
    return get_ref( self ) * theArg ;
  }
  
  void __imul__( const Foam::GeometricField< Foam::scalar, TPatchField, TMesh >& theArg )
  {
    get_ref( self ) *= theArg;
  }    

  Foam::tmp< Foam::GeometricField< Foam::scalar, TPatchField, TMesh > > __radd__( const Foam::scalar& theArg ) const
  {
    return  theArg + get_ref( self );
  }
  
  Foam::tmp< Foam::GeometricField< Foam::scalar, TPatchField, TMesh > > __rsub__( const Foam::scalar& theArg ) const
  {
    return  theArg - get_ref( self );
  }
    
  Foam::tmp< Foam::GeometricField< Foam::scalar, TPatchField, TMesh > > __sub__( const Foam::scalar& theArg ) const
  {
    return  get_ref( self ) - theArg;
  }
    
  Foam::tmp< Foam::GeometricField< Foam::tensor, TPatchField, TMesh > > __rmul__( const Foam::tensor& theArg ) const
  {
    return  theArg * get_ref( self );
  }
  
  Foam::tmp< Foam::GeometricField< Foam::sphericalTensor, TPatchField, TMesh > > __rmul__( const Foam::sphericalTensor& theArg ) const
  {
    return theArg * get_ref( self );
  }
  
  Foam::tmp< Foam::GeometricField< Foam::sphericalTensor, TPatchField, TMesh > > __mul__( const Foam::GeometricField< Foam::sphericalTensor, TPatchField, TMesh >& theArg ) const
  {
    return get_ref( self ) * theArg;
  }
  
  Foam::tmp< Foam::GeometricField< Foam::symmTensor, TPatchField, TMesh > > __mul__( const Foam::GeometricField< Foam::symmTensor, TPatchField, TMesh >& theArg ) const
  {
    return get_ref( self ) * theArg;
  }
  Foam::tmp< Foam::GeometricField< Foam::scalar, TPatchField, TMesh > > pos() const
  {
    return Foam::pos( get_ref( self ) );
  }
}
%enddef


//---------------------------------------------------------------------------
%define SCALAR_SMART_TMP_GEOMETRIC_FIELD_TEMPLATE_FUNC( GeometricFieldType, TPatchField, TMesh )

%extend Foam::smart_tmp< GeometricFieldType > __COMMON_GEOMETRIC_FIELD_TEMPLATE_FUNC__( Foam::scalar, TPatchField, TMesh );
%extend Foam::smart_tmp< GeometricFieldType > __COMMON_TMP_GEOMETRIC_FIELD_TEMPLATE_FUNC__( Foam::scalar );
%extend Foam::smart_tmp< GeometricFieldType > __SCALAR_GEOMETRIC_FIELD_TEMPLATE_FUNC__( TPatchField, TMesh );

%enddef


//---------------------------------------------------------------------------
%define SCALAR_GEOMETRIC_FIELD_TEMPLATE_FUNC( TPatchField, TMesh )

GEOMETRIC_FIELD_TEMPLATE_FUNC( Foam::scalar, TPatchField, TMesh );

PYAPPEND_RETURN_SELF_COMPOUND_OPERATOR_TEMPLATE_3( Foam::GeometricField, Foam::scalar, TPatchField, TMesh, __imul__ );

%extend Foam::GeometricField< Foam::scalar, TPatchField, TMesh > __SCALAR_GEOMETRIC_FIELD_TEMPLATE_FUNC__( TPatchField, TMesh );

CLEAR_PYAPPEND_RETURN_SELF_COMPOUND_OPERATOR_TEMPLATE_3( Foam::GeometricField, Foam::scalar, TPatchField, TMesh, __imul__ );

PYAPPEND_RETURN_SELF_COMPOUND_OPERATOR_TEMPLATE_4( Foam::tmp, Foam::GeometricField, Foam::scalar, TPatchField, TMesh, __imul__ );

%extend Foam::tmp< Foam::GeometricField< Foam::scalar, TPatchField, TMesh > > __SCALAR_GEOMETRIC_FIELD_TEMPLATE_FUNC__( TPatchField, TMesh );

CLEAR_PYAPPEND_RETURN_SELF_COMPOUND_OPERATOR_TEMPLATE_4( Foam::tmp, Foam::GeometricField, Foam::scalar, TPatchField, TMesh, __imul__ );

GEOMETRIC_FIELD_HOLDER_FUNC_EXTEND( Foam::scalar, TPatchField, TMesh );

%enddef


//---------------------------------------------------------------------------
%import "Foam/src/OpenFOAM/dimensionedTypes/dimensionedVector.cxx"
%import "Foam/src/OpenFOAM/fields/UniformDimensionedFields/UniformDimensionedVectorField.cxx"
%define __VECTOR_GEOMETRIC_FIELD_TEMPLATE_FUNC__( Type, TPatchField, TMesh )
{
  Foam::tmp< Foam::GeometricField< Foam::scalar, TPatchField, TMesh > > __and__( const Foam::GeometricField< Foam::vector, TPatchField, TMesh >& theArg ) const
  {
    return get_ref( self ) & theArg;
  }
  Foam::tmp< Foam::GeometricField< Foam::vector, TPatchField, TMesh > > __and__( const Foam::GeometricField< Foam::tensor, TPatchField, TMesh >& theArg ) const
  {
    return get_ref( self ) & theArg;
  }
  Foam::tmp< Foam::GeometricField< Foam::vector, TPatchField, TMesh > > __div__( const Foam::GeometricField< Foam::scalar, TPatchField, TMesh >& theArg ) const
  {
    return get_ref( self ) / theArg;
  }
  Foam::tmp< Foam::GeometricField< Foam::vector, TPatchField, TMesh > > __div__( const Foam::dimensioned< Foam::scalar >& theArg ) const
  {
    return get_ref( self ) / theArg;
  }
  Foam::tmp< Foam::GeometricField< Foam::vector, TPatchField, TMesh > > __mul__( const Foam::dimensioned< Foam::scalar >& theArg ) const
  {
    return get_ref( self ) * theArg;
  }
  Foam::tmp< Foam::GeometricField< Foam::vector, TPatchField, TMesh > >  __rxor__( const Foam::dimensioned< Foam::vector >& theArg ) const
  {
    return theArg ^ get_ref( self );
  }
  
  Foam::tmp<Foam::GeometricField<Foam::scalar, TPatchField, TMesh > > __rand__( const Foam::dimensioned< Foam::vector >& theArg ) const
  {
    return theArg & get_ref( self );
  }
    
  Foam::tmp<Foam::GeometricField<Foam::scalar, TPatchField, TMesh > > __rand__( const Foam::vector& theArg ) const
  {
    return theArg & get_ref( self );
  }
  Foam::tmp< Foam::GeometricField< Foam::vector, TPatchField, TMesh > > __rmul__( const Foam::dimensioned< Foam::scalar >& theArg ) const
  {
    return theArg * get_ref( self ) ;
  }

  Foam::tmp<Foam::GeometricField<Foam::scalar, TPatchField, TMesh > > __and__( const Foam::dimensioned< Foam::vector >& theArg ) const
  {
    return get_ref( self ) & theArg;
  }

  Foam::tmp< Foam::GeometricField< Foam::vector, TPatchField, TMesh > >  __xor__( const Foam::dimensioned< Foam::vector >& theArg ) const
  {
    return get_ref( self ) ^ theArg ;
  }
  
#if FOAM_VERSION( >, 010500 )
  Foam::tmp< Foam::GeometricField< Foam::scalar, TPatchField, TMesh > >__rand__( const Foam::UniformDimensionedField< Foam::vector >& theArg ) const
  {
    return theArg & *self;
  }
#endif    
}
%enddef


//---------------------------------------------------------------------------
%define VECTOR_GEOMETRIC_FIELD_TEMPLATE_FUNC( TPatchField, TMesh )

GEOMETRIC_FIELD_TEMPLATE_FUNC( Foam::vector, TPatchField, TMesh );

%extend Foam::GeometricField< Foam::vector, TPatchField, TMesh > __VECTOR_GEOMETRIC_FIELD_TEMPLATE_FUNC__( Type, TPatchField, TMesh );

%extend Foam::tmp< Foam::GeometricField< Foam::vector, TPatchField, TMesh > > __VECTOR_GEOMETRIC_FIELD_TEMPLATE_FUNC__( Type, TPatchField, TMesh );

GEOMETRIC_FIELD_HOLDER_FUNC_EXTEND( Foam::vector, TPatchField, TMesh );

%enddef


//---------------------------------------------------------------------------
%define __TENSOR_GEOMETRIC_FIELD_TEMPLATE_FUNC__( Type, TPatchField, TMesh )
{
  Foam::tmp< Foam::GeometricField< Foam::tensor, TPatchField, TMesh > > inv() const
  {
    return Foam::inv( get_ref( self ) );
  }
  
  Foam::tmp< Foam::GeometricField< Foam::scalar, TPatchField, TMesh > > tr() const
  {
    return Foam::tr( get_ref( self ) );
  }
  
  Foam::tmp< Foam::GeometricField< Foam::tensor, TPatchField, TMesh > > dev2() const
  {
    return Foam::dev2( get_ref( self ) );
  }
  
  Foam::tmp< Foam::GeometricField< Foam::symmTensor, TPatchField, TMesh > > symm() const
  {
    return Foam::symm( get_ref( self ) );
  }
  
  Foam::GeometricField< Foam::vector, TPatchField, TMesh > __and__( const Foam::tmp<GeometricField< Foam::vector, TPatchField, TMesh > >& theArg ) const
  {
    return  get_ref( self ) & theArg;
  }
  Foam::tmp< Foam::GeometricField< Foam::tensor, TPatchField, TMesh > > __add__( const Foam::GeometricField< Foam::sphericalTensor, TPatchField, TMesh >& theArg ) const
  {
    return  get_ref( self ) + theArg;
  }
}
%enddef


//---------------------------------------------------------------------------
%define TENSOR_GEOMETRIC_FIELD_TEMPLATE_FUNC( TPatchField, TMesh )

GEOMETRIC_FIELD_TEMPLATE_FUNC( Foam::tensor, TPatchField, TMesh );

%extend Foam::GeometricField< Foam::tensor, TPatchField, TMesh > __TENSOR_GEOMETRIC_FIELD_TEMPLATE_FUNC__( Type, TPatchField, TMesh );

%extend Foam::tmp< Foam::GeometricField< Foam::tensor, TPatchField, TMesh > > __TENSOR_GEOMETRIC_FIELD_TEMPLATE_FUNC__( Type, TPatchField, TMesh );

%enddef


//---------------------------------------------------------------------------
%define __SYMMTENSOR_GEOMETRIC_FIELD_TEMPLATE_FUNC__( Type, TPatchField, TMesh )
{
  Foam::tmp< Foam::GeometricField< Foam::symmTensor, TPatchField, TMesh > > dev() const
  {
    return Foam::dev( get_ref( self ) );
  }
  Foam::tmp< Foam::GeometricField< Foam::scalar, TPatchField, TMesh > > magSqr() const
  {
    return Foam::magSqr( get_ref( self )  );
  }
  Foam::tmp< Foam::GeometricField< Foam::symmTensor, TPatchField, TMesh > > __add__( const Foam::GeometricField< Foam::sphericalTensor, TPatchField, TMesh >& theArg ) const
  {
    return  get_ref( self ) + theArg;
  }
}
%enddef


//---------------------------------------------------------------------------
%define SYMMTENSOR_GEOMETRIC_FIELD_TEMPLATE_FUNC( TPatchField, TMesh )

GEOMETRIC_FIELD_TEMPLATE_FUNC( Foam::symmTensor, TPatchField, TMesh );

%extend Foam::GeometricField< Foam::symmTensor, TPatchField, TMesh > __SYMMTENSOR_GEOMETRIC_FIELD_TEMPLATE_FUNC__( Type, TPatchField, TMesh );

%extend Foam::tmp< Foam::GeometricField< Foam::symmTensor, TPatchField, TMesh > >__SYMMTENSOR_GEOMETRIC_FIELD_TEMPLATE_FUNC__( Type, TPatchField, TMesh );

%enddef


//-----------------------------------------------------------------------------
%define SPHERICALTENSOR_GEOMETRIC_FIELD_TEMPLATE_FUNC( TPatchField, TMesh )

GEOMETRIC_FIELD_TEMPLATE_FUNC( Foam::sphericalTensor, TPatchField, TMesh );

%enddef


//-------------------------------------------------------------------------------
#endif

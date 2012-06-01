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
#ifndef Field_cpp
#define Field_cpp


//---------------------------------------------------------------------------
%{
  #include "Foam/src/OpenFOAM/fields/Fields/Field.hh"
%}


//---------------------------------------------------------------------------
%import "Foam/src/OpenFOAM/containers/Lists/List/List.cxx"

%import "Foam/src/OpenFOAM/fields/tmp/refCount.cxx"

%import "Foam/src/OpenFOAM/fields/tmp/tmp.cxx"

%import "Foam/ext/common/smart_tmp.hxx"

%include <Field.H>

%import "Foam/src/OpenFOAM/fields/Fields/primitiveFieldsFwd.cxx"


//---------------------------------------------------------------------------
%include <FieldHolder.hpp>

%define NO_TMP_TYPEMAP_FIELD( Type )

%typecheck( SWIG_TYPECHECK_POINTER ) const Foam::Field< Type >& 
{
  void *ptr;
  int res = SWIG_ConvertPtr( $input, (void **) &ptr, $descriptor( Foam::Field< Type > * ), 0 );
  int res1 = SWIG_ConvertPtr( $input, (void **) &ptr, $descriptor( Foam::tmp< Foam::Field< Type > > * ), 0 );
  int res_smart_tmpT = SWIG_ConvertPtr( $input, (void **) &ptr, $descriptor( Foam::smart_tmp< Foam::Field< Type > > * ), 0 );
  int res_holder = SWIG_ConvertPtr( $input, (void **) &ptr, $descriptor( Foam::FieldHolder< Type > * ), 0 );
  $1 = SWIG_CheckState( res ) || SWIG_CheckState( res1 ) || SWIG_CheckState( res_smart_tmpT ) || SWIG_CheckState( res_holder );
}

%typemap( in ) const Foam::Field< Type >& 
{
  void  *argp = 0;
  int res = 0;
  
  res = SWIG_ConvertPtr( $input, &argp, $descriptor(  Foam::Field< Type > * ), %convertptr_flags );
  if ( SWIG_IsOK( res )&& argp  ){
    Foam::Field< Type > * res =  %reinterpret_cast( argp, Foam::Field< Type >* );
    $1 = res;
  } else {
    res = SWIG_ConvertPtr( $input, &argp, $descriptor( Foam::tmp< Foam::Field< Type > >* ), %convertptr_flags );
    if ( SWIG_IsOK( res ) && argp ) {
      Foam::tmp<Foam::Field< Type > >* tmp_res =%reinterpret_cast( argp, Foam::tmp< Foam::Field< Type > > * );
      $1 = tmp_res->operator->();
      } else {
      res = SWIG_ConvertPtr( $input, &argp, $descriptor( Foam::smart_tmp< Foam::Field< Type > >* ), %convertptr_flags );
      if ( SWIG_IsOK( res ) && argp ) { 
        Foam::smart_tmp< Foam::Field< Type > >* tmp_res =%reinterpret_cast( argp, Foam::smart_tmp< Foam::Field< Type > > * );
        $1 = tmp_res->operator->();
      } else {
        res = SWIG_ConvertPtr( $input, &argp, $descriptor( Foam::FieldHolder< Type >* ), %convertptr_flags );
        if ( SWIG_IsOK( res ) && argp ) {
          Foam::FieldHolder< Type >* tmp_res =%reinterpret_cast( argp, Foam::FieldHolder< Type >* );
          $1 = tmp_res->operator->();
        } else {
          %argument_fail( res, "$type", $symname, $argnum );
        }
    } }
 }
}    
%enddef


//---------------------------------------------------------------------------
%define FIELD_VIRTUAL_EXTENDS( Type )
  void ext_assign( const Foam::Type& theSource )
  {
    Foam::Warning << "The “ext_assign” method is obsolete, use “<<” operator instead" << endl;
    *dynamic_cast< Foam::Field< Foam::Type >* >( get_ptr( self ) ) = theSource;
  }
  
  void ext_assign( const Foam::UList< Foam::Type >& theSource )
  {
    Foam::Warning << "The “ext_assign” method is obsolete, use “<<” operator instead" << endl;
    *dynamic_cast< Foam::Field< Foam::Type >* >( get_ptr( self ) ) = theSource;
  }
  
  void ext_assign( const Foam::Field< Foam::Type >& theSource )
  {
    Foam::Warning << "The “ext_assign” method is obsolete, use “<<” operator instead" << endl;
    *dynamic_cast< Foam::Field< Foam::Type >* >( get_ptr( self ) ) = theSource;
  }
  
  void __lshift__( const Foam::Type& theSource )
  {
    *dynamic_cast< Foam::Field< Foam::Type >* >( get_ptr( self ) ) = theSource;
  }
  
  void __lshift__( const Foam::UList< Foam::Type >& theSource )
  {
    *dynamic_cast< Foam::Field< Foam::Type >* >( get_ptr( self ) ) = theSource;
  }
  
  void __lshift__( const Foam::Field< Foam::Type >& theSource )
  {
    *dynamic_cast< Foam::Field< Foam::Type >* >( get_ptr( self ) ) = theSource;
  }
%enddef


//---------------------------------------------------------------------------
%define FIELD_PYAPPEND_RETURN_SELF_COMPOUND_OPERATOR( Type )

PYAPPEND_RETURN_SELF_COMPOUND_OPERATOR_TEMPLATE_1( Foam::Field, Type, __imul__ );

PYAPPEND_RETURN_SELF_COMPOUND_OPERATOR_TEMPLATE_1( Foam::Field, Type, __iadd__ );

PYAPPEND_RETURN_SELF_COMPOUND_OPERATOR_TEMPLATE_1( Foam::Field, Type, __isub__ );

PYAPPEND_RETURN_SELF_COMPOUND_OPERATOR_TEMPLATE_1( Foam::Field, Type, __idiv__ );

PYAPPEND_RETURN_SELF_COMPOUND_OPERATOR_TEMPLATE_TEMPLATE_1( Foam::tmp, Foam::Field, Type, __imul__ );

PYAPPEND_RETURN_SELF_COMPOUND_OPERATOR_TEMPLATE_TEMPLATE_1( Foam::tmp, Foam::Field, Type, __iadd__ );

PYAPPEND_RETURN_SELF_COMPOUND_OPERATOR_TEMPLATE_TEMPLATE_1( Foam::tmp, Foam::Field, Type, __isub__ );

PYAPPEND_RETURN_SELF_COMPOUND_OPERATOR_TEMPLATE_TEMPLATE_1( Foam::tmp, Foam::Field, Type, __idiv__ );


%enddef


%define FIELD_CLEAR_PYAPPEND_RETURN_SELF_COMPOUND_OPERATOR( Type )

CLEAR_PYAPPEND_RETURN_SELF_COMPOUND_OPERATOR_TEMPLATE_1( Foam::Field, Type, __idiv__ );

CLEAR_PYAPPEND_RETURN_SELF_COMPOUND_OPERATOR_TEMPLATE_1( Foam::Field, Type, __isub__ );

CLEAR_PYAPPEND_RETURN_SELF_COMPOUND_OPERATOR_TEMPLATE_1( Foam::Field, Type, __iadd__ );

CLEAR_PYAPPEND_RETURN_SELF_COMPOUND_OPERATOR_TEMPLATE_1( Foam::Field, Type, __imul__ );

CLEAR_PYAPPEND_RETURN_SELF_COMPOUND_OPERATOR_TEMPLATE_TEMPLATE_1( Foam::tmp, Foam::Field, Type, __idiv__ );

CLEAR_PYAPPEND_RETURN_SELF_COMPOUND_OPERATOR_TEMPLATE_TEMPLATE_1( Foam::tmp, Foam::Field, Type, __isub__ );

CLEAR_PYAPPEND_RETURN_SELF_COMPOUND_OPERATOR_TEMPLATE_TEMPLATE_1( Foam::tmp, Foam::Field, Type, __iadd__ );

CLEAR_PYAPPEND_RETURN_SELF_COMPOUND_OPERATOR_TEMPLATE_TEMPLATE_1( Foam::tmp, Foam::Field, Type, __imul__ );

%enddef

//---------------------------------------------------------------------------
%define __COMMON_FIELD_TEMPLATE_OPERATOR( Type )
  Foam::tmp< Foam::Field< Foam::Type > > __rmul__( const Foam::scalar& theArg)
  {
    return theArg * get_ref( self );
  }
  Foam::tmp< Foam::Field< Foam::Type > > __mul__( const Foam::Field< Foam::scalar >& theArg)
  {
    return get_ref( self ) * theArg;
  }
  Foam::tmp< Foam::Field< Foam::Type > > __rmul__( const Foam::Field< Foam::scalar >& theArg)
  {
    return theArg * get_ref( self );
  }
  Foam::tmp< Foam::Field< Foam::Type > > __add__( const Foam::Field< Foam::Type >& theArg)
  {
    return get_ref( self ) + theArg;
  }
  Foam::tmp< Foam::Field< Foam::Type > > __sub__( const Foam::Field< Foam::Type >& theArg)
  {
    return get_ref( self ) - theArg;
  }
  
  Foam::tmp< Foam::Field< Foam::Type > > __sub__( const Foam::Type& theArg )
  {
    return  get_ref( self ) - theArg; 
  }
  
  Foam::tmp< Foam::Field< Foam::Type > > __div__( const Foam::Field< Foam::scalar >& theArg)
  {
    return get_ref( self ) / theArg;
  }
  Foam::tmp< Foam::Field< Type > > __mul__( const Foam::scalar& theArg )
  {
    return get_ref( self ) * theArg; 
  }
  
  Foam::tmp< Foam::Field< Type > > __div__( const Foam::Field< scalar >& theArg )
  {
    return  get_ref( self ) / theArg; 
  }
  
  Foam::tmp< Foam::Field< Foam::scalar > > mag()
  {
    return Foam::mag( get_ref( self ) );
  }
  Foam::tmp< Foam::Field< Foam::scalar > > magSqr()
  {
    return Foam::magSqr( get_ref( self ) );
  }
  Foam::Type gSum()
  {
    return Foam::gSum( get_ref( self ) );
  }
  Foam::Type gMin()
  {
    return Foam::gMin( get_ref( self ) );
  }
  Foam::Type gMax()
  {
    return Foam::gMax( get_ref( self ) );
  }
  Foam::Type gAverage()
  {
    return Foam::gAverage( get_ref( self ) );
  }
  Foam::Type max()
  {
    return Foam::max( get_ref( self ) );
  }
%enddef


//---------------------------------------------------------------------------
%define __FIELD_TEMPLATE_FUNC__( Type )
  Foam::Field< Foam::Type >()
  {
    return new Foam::Field< Foam::Type >();
  }

  Foam::Field< Foam::Type >( const Foam::label size )
  {
    return new Foam::Field< Foam::Type >( size );
  }

  Foam::Field< Foam::Type >( const Foam::label size, const Foam::Type& t )
  {
    return new Foam::Field< Foam::Type >( size, t );
  }

  Foam::Field< Foam::Type >( const Foam::word& keyword, const Foam::dictionary& dict, const Foam::label size )
  {
    return new Foam::Field< Foam::Type >( keyword, dict, size );
  }
  Foam::Field< Foam::Type >( const Foam::Field< Foam::Type >& theField )
  {
    return new Foam::Field< Foam::Type >( theField );
  }
%enddef


//---------------------------------------------------------------------------
%define __COMMON_TMP_FIELD_TEMPLATE_FUNC__( Type )
  const Type& __getitem__( const Foam::label& theIndex ) const
  {
    return get_ref( self )[ theIndex ];
  }

  void __setitem__( const Foam::label& theIndex, const Type& theValue )
  {
    get_ref( self )[ theIndex ] = theValue;
  }
%enddef


//---------------------------------------------------------------------------
%define FIELD_TEMPLATE_FUNC( Type )

%import "Foam/src/OpenFOAM/fields/tmp/tmp.cxx"

NO_TMP_TYPEMAP_FIELD(  Foam::scalar );
NO_TMP_TYPEMAP_FIELD(  Foam::vector );
NO_TMP_TYPEMAP_FIELD(  Foam::tensor );

%import "Foam/src/OpenFOAM/db/IOstreams/IOstreams/Ostream.cxx"

%extend Foam::Field< Foam::Type >
{
 FIELD_VIRTUAL_EXTENDS( Type );
 __FIELD_TEMPLATE_FUNC__( Type );
 __COMMON_FIELD_TEMPLATE_OPERATOR( Type );
 OSTREAM_EXTENDS;
}

%extend Foam::tmp< Foam::Field< Foam::Type > >
{
  __COMMON_FIELD_TEMPLATE_OPERATOR( Type );
  __COMMON_TMP_FIELD_TEMPLATE_FUNC__( Type );
  SEQUENCE_ADDONS( Foam::Type );
  LISTS_FUNCS( Foam::Type );
}

%extend Foam::smart_tmp< Foam::Field< Foam::Type > >
{
  __COMMON_FIELD_TEMPLATE_OPERATOR( Type );
  __COMMON_TMP_FIELD_TEMPLATE_FUNC__( Type );
  SEQUENCE_ADDONS( Foam::Type );
  LISTS_FUNCS( Foam::Type );
}

%enddef

//--------------------------------------------------------------------------
%define __SCALAR_FIELD_TEMPLATE_OPERATOR
  Foam::tmp< Foam::Field< Foam::scalar > > __add__( const Foam::scalar& theArg )
  {
    return get_ref( self ) + theArg;
  }
%enddef


//--------------------------------------------------------------------------
%define SCALAR_FIELD_TEMPLATE_FUNC

FIELD_PYAPPEND_RETURN_SELF_COMPOUND_OPERATOR( Foam::scalar );

FIELD_TEMPLATE_FUNC( scalar );

%extend Foam::Field< Foam::scalar >
{
  __SCALAR_FIELD_TEMPLATE_OPERATOR;
}

%extend Foam::tmp< Foam::Field< Foam::scalar > >
{
  __SCALAR_FIELD_TEMPLATE_OPERATOR;
}

FIELD_CLEAR_PYAPPEND_RETURN_SELF_COMPOUND_OPERATOR( Foam::scalar );

%enddef


//---------------------------------------------------------------------------
%define __VECTOR_FIELD_TEMPLATE_FUNC
  Foam::tmp< Foam::Field< Foam::tensor > > __mul__( const Foam::Field< Foam::vector >& theArg)
  {
    return get_ref( self ) * theArg;
  }
  Foam::tmp< Foam::Field< Foam::scalar > > __rand__( const Foam::vector& theArg)
  {
    return theArg & get_ref( self );
  }
  Foam::tmp< Foam::Field< Foam::vector > > __rand__( const Foam::tensor& theArg)
  {
    return theArg & get_ref( self );
  }
  Foam::tmp< Foam::Field< Foam::scalar > > __and__( const Foam::Field< Foam::vector >& theArg )
  {
    return  get_ref( self ) & theArg; 
  }
  Foam::tmp< Foam::Field< Foam::vector > > __and__( const Foam::Field< Foam::tensor >& theArg )
  {
    return  get_ref( self ) & theArg; 
  }
%enddef


//---------------------------------------------------------------------------
%define VECTOR_FIELD_TEMPLATE_FUNC

FIELD_PYAPPEND_RETURN_SELF_COMPOUND_OPERATOR( Foam::vector );

FIELD_TEMPLATE_FUNC( vector );

%extend Foam::Field< Foam::vector >
{
  __VECTOR_FIELD_TEMPLATE_FUNC;
}

%extend Foam::tmp< Foam::Field< Foam::vector > >
{
  __VECTOR_FIELD_TEMPLATE_FUNC;
}

FIELD_CLEAR_PYAPPEND_RETURN_SELF_COMPOUND_OPERATOR( Foam::vector );

%enddef


//----------------------------------------------------------------------------
%define __TENSOR_FIELD_TEMPLATE_FUNC
  Foam::tmp< Foam::Field< Foam::tensor > > ext_T()
  {
    return get_ref( self ).T();
  }
  Foam::tmp< Foam::Field< Foam::scalar > > tr()
  {
    return Foam::tr( get_ref( self ) );
  }
%enddef


//-----------------------------------------------------------------------------
%define TENSOR_FIELD_TEMPLATE_FUNC

FIELD_PYAPPEND_RETURN_SELF_COMPOUND_OPERATOR( Foam::tensor );

FIELD_TEMPLATE_FUNC( tensor );

%extend Foam::Field< Foam::tensor >
{
 __TENSOR_FIELD_TEMPLATE_FUNC;
}

FIELD_CLEAR_PYAPPEND_RETURN_SELF_COMPOUND_OPERATOR( Foam::tensor );

%enddef


//----------------------------------------------------------------------------
%define COMPLEX_FIELD_TEMPLATE_FUNC( ComplexType )

NO_TMP_TYPEMAP_FIELD( Field< Foam::ComplexType > );

%extend Foam::Field< Foam::ComplexType >
{
  __FIELD_TEMPLATE_FUNC__( ComplexType );
  FIELD_VIRTUAL_EXTENDS( ComplexType );
}

%enddef


//----------------------------------------------------------------------------
#endif

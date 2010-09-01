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
#ifndef Field_cxx
#define Field_cxx


//---------------------------------------------------------------------------
%include "src/OpenFOAM/containers/Lists/List/List.cxx"

%include "src/OpenFOAM/fields/tmp/refCount.cxx"

%{
    #include "Field.H"
%}

%include "Field.H"

%include "src/OpenFOAM/fields/tmp/tmp.cxx"

%include "ext/common/ext_tmp.hxx"


//---------------------------------------------------------------------------
%define NO_TMP_TYPEMAP_FIELD( Field_Type )

%typecheck( SWIG_TYPECHECK_POINTER ) const Foam::Field_Type& 
{
    void *ptr;
    int res = SWIG_ConvertPtr( $input, (void **) &ptr, $descriptor( Foam::Field_Type * ), 0 );
    int res1 = SWIG_ConvertPtr( $input, (void **) &ptr, $descriptor( Foam::tmp< Foam::Field_Type > * ), 0 );
    int res_ext_tmpT = SWIG_ConvertPtr( $input, (void **) &ptr, $descriptor( Foam::ext_tmp< Foam::Field_Type > * ), 0 );
    $1 = SWIG_CheckState( res ) || SWIG_CheckState( res1 ) || SWIG_CheckState( res_ext_tmpT );
}

%typemap( in ) const Foam::Field_Type& 
{
  void  *argp = 0;
  int res = 0;
  
  res = SWIG_ConvertPtr( $input, &argp, $descriptor(  Foam::Field_Type * ), %convertptr_flags );
  if ( SWIG_IsOK( res )&& argp  ){
    Foam::Field_Type * res =  %reinterpret_cast( argp, Foam::Field_Type* );
    $1 = res;
  } else {
    res = SWIG_ConvertPtr( $input, &argp, $descriptor( Foam::tmp< Foam::Field_Type >* ), %convertptr_flags );
    if ( SWIG_IsOK( res ) && argp ) {
      Foam::tmp<Foam::Field_Type >* tmp_res =%reinterpret_cast( argp, Foam::tmp< Foam::Field_Type > * );
      $1 = tmp_res->operator->();
      } else {
      res = SWIG_ConvertPtr( $input, &argp, $descriptor( Foam::ext_tmp< Foam::Field_Type >* ), %convertptr_flags );
      if ( SWIG_IsOK( res ) && argp ) { Foam::ext_tmp< Foam::Field_Type >* tmp_res =%reinterpret_cast( argp, Foam::ext_tmp< Foam::Field_Type > * );
      $1 = tmp_res->operator->();
      } else {
        %argument_fail( res, "$type", $symname, $argnum );
        }
    }
 }
}    
%enddef


//---------------------------------------------------------------------------
%define FIELD_VIRTUAL_EXTENDS( Type )
{
  void ext_assign( const Foam::Type& theSource )
  {
    *dynamic_cast< Foam::Field< Foam::Type >* >( self ) = theSource;
  }
  
  void ext_assign( const Foam::UList< Foam::Type >& theSource )
  {
    *dynamic_cast< Foam::Field< Foam::Type >* >( self ) = theSource;
  }
  
  void ext_assign( const Foam::Field< Foam::Type >& theSource )
  {
    *dynamic_cast< Foam::Field< Foam::Type >* >( self ) = theSource;
  }
}
%enddef


//---------------------------------------------------------------------------
%define __COMMON_FIELD_TEMPLATE_OPERATOR( Type )
{
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
}
%enddef


//---------------------------------------------------------------------------
%define __FIELD_TEMPLATE_FUNC__( Type )
{
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

}
%enddef


//---------------------------------------------------------------------------
%define FIELD_TEMPLATE_FUNC( Type )

%include "src/OpenFOAM/fields/tmp/tmp.cxx"

NO_TMP_TYPEMAP_FIELD( Field< Foam::scalar > );
NO_TMP_TYPEMAP_FIELD( Field< Foam::vector > );
NO_TMP_TYPEMAP_FIELD( Field< Foam::tensor > );

%extend Foam::Field< Foam::Type > FIELD_VIRTUAL_EXTENDS( Type );
%extend Foam::Field< Foam::Type > __FIELD_TEMPLATE_FUNC__( Type );

%extend Foam::Field< Foam::Type >__COMMON_FIELD_TEMPLATE_OPERATOR( Type );
%extend Foam::tmp< Foam::Field< Foam::Type > >__COMMON_FIELD_TEMPLATE_OPERATOR( Type );
%extend Foam::ext_tmp< Foam::Field< Foam::Type > >__COMMON_FIELD_TEMPLATE_OPERATOR( Type );

%include "src/OpenFOAM/db/IOstreams/IOstreams/Ostream.cxx"

%extend Foam::Field< Foam::Type > OSTREAM_EXTENDS;

%enddef

//--------------------------------------------------------------------------
%define SCALAR_FIELD_TEMPLATE_FUNC
FIELD_TEMPLATE_FUNC( scalar );
%enddef

//---------------------------------------------------------------------------
%define __VECTOR_FIELD_TEMPLATE_FUNC
{
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
}
%enddef


//---------------------------------------------------------------------------
%define VECTOR_FIELD_TEMPLATE_FUNC

FIELD_TEMPLATE_FUNC( vector );

%extend Foam::Field< Foam::vector > __VECTOR_FIELD_TEMPLATE_FUNC;
%extend Foam::tmp< Foam::Field< Foam::vector > >__VECTOR_FIELD_TEMPLATE_FUNC;

%enddef


//----------------------------------------------------------------------------
%define __TENSOR_FIELD_TEMPLATE_FUNC
{
  Foam::tmp< Foam::Field< Foam::tensor > > ext_T()
  {
    return self->T();
  }
  Foam::tmp< Foam::Field< Foam::scalar > > tr()
  {
    return Foam::tr( *self );
  }
} 
%enddef


//-----------------------------------------------------------------------------
%define TENSOR_FIELD_TEMPLATE_FUNC

FIELD_TEMPLATE_FUNC( tensor );

%extend Foam::Field< Foam::tensor > __TENSOR_FIELD_TEMPLATE_FUNC;

%enddef


//----------------------------------------------------------------------------
#endif

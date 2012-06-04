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
#ifndef DimensionedField_cpp
#define DimensionedField_cpp


//---------------------------------------------------------------------------
%module "Foam.src.OpenFOAM.fields.DimensionedFields.DimensionedField";
%{
  #include "Foam/src/OpenFOAM/fields/DimensionedFields/DimensionedField.hh"
%}


//---------------------------------------------------------------------------
%import "Foam/src/OpenFOAM/db/regIOobject.cxx"

%import "Foam/src/OpenFOAM/fields/Fields/primitiveFields.cxx"

%import "Foam/src/OpenFOAM/dimensionedTypes/dimensionedType.cxx"

%include <DimensionedField.H>


//---------------------------------------------------------------------------
%import "Foam/src/OpenFOAM/fields/tmp/tmp.cxx"

%define DIMENSIONED_FIELD_VIRTUAL_EXTENDS( Type, TMesh )
  void ext_assign( const Foam::DimensionedField< Foam::Type, Foam::TMesh >& theSource )
  {
    Foam::Warning << "The “ext_assign” method is obsolete, use “<<” operator instead" << endl;
    *dynamic_cast< Foam::DimensionedField< Foam::Type, Foam::TMesh >* >( &get_ref( self ) ) = theSource;
  }
  
  void __lshift__( const Foam::DimensionedField< Foam::Type, Foam::TMesh >& theSource )
  {
    *dynamic_cast< Foam::DimensionedField< Foam::Type, Foam::TMesh >* >( &get_ref( self ) ) = theSource;
  }
%enddef


//---------------------------------------------------------------------------
%define __COMMON_DIMENSIONEDFIELD_TEMPLATE_OPERATOR( Type, TMesh )
  Foam::tmp< Foam::DimensionedField< Foam::Type, Foam::TMesh > > __rmul__( const Foam::scalar& theArg)
  {
    return theArg * get_ref( self );
  }
  Foam::tmp< Foam::DimensionedField< Foam::Type, Foam::TMesh > > __mul__( const Foam::DimensionedField< Foam::scalar, Foam::TMesh >& theArg)
  {
    return get_ref( self ) * theArg;
  }
  Foam::tmp< Foam::DimensionedField< Foam::Type, Foam::TMesh > > __rmul__( const Foam::DimensionedField< Foam::scalar, Foam::TMesh >& theArg)
  {
    return theArg * get_ref( self );
  }
  Foam::tmp< Foam::DimensionedField< Foam::Type, Foam::TMesh > > __add__( const Foam::DimensionedField< Foam::Type, Foam::TMesh >& theArg)
  {
    return get_ref( self ) + theArg;
  }
  Foam::tmp< Foam::DimensionedField< Foam::Type, Foam::TMesh > > __sub__( const Foam::DimensionedField< Foam::Type, Foam::TMesh >& theArg)
  {
    return get_ref( self ) - theArg;
  }
  
  Foam::tmp< Foam::DimensionedField< Foam::Type, Foam::TMesh > > __sub__( const Foam::Type& theArg )
  {
    return  get_ref( self ) - theArg; 
  }
  
  Foam::tmp< Foam::DimensionedField< Foam::Type, Foam::TMesh > > __div__( const Foam::DimensionedField< Foam::scalar, Foam::TMesh >& theArg)
  {
    return get_ref( self ) / theArg;
  }
  Foam::tmp< Foam::DimensionedField< Foam::Type, Foam::TMesh > > __mul__( const Foam::scalar& theArg )
  {
    return get_ref( self ) * theArg; 
  }
  
  Foam::tmp< Foam::DimensionedField< Foam::Type, Foam::TMesh > > __div__( const Foam::DimensionedField< Foam::scalar, Foam::TMesh >& theArg )
  {
    return  get_ref( self ) / theArg; 
  }
  
  Foam::tmp< Foam::DimensionedField< Foam::scalar, Foam::TMesh > > mag()
  {
    return Foam::mag( get_ref( self ) );
  }
  Foam::tmp< Foam::DimensionedField< Foam::scalar, Foam::TMesh > > magSqr()
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
  Foam::dimensioned< Foam::Type > gMax()
  {
    return Foam::gMax( get_ref( self ) );
  }
  Foam::Type gAverage()
  {
    return Foam::gAverage( get_ref( self ) );
  }
  Foam::dimensioned< Foam::Type > max()
  {
    return Foam::max( get_ref( self ) );
  }
%enddef


//---------------------------------------------------------------------------
%define NO_TMP_TYPEMAP_DIMENSIONED_FIELD( Type, TMesh, TPatchField )

%typecheck( SWIG_TYPECHECK_POINTER ) const Foam::DimensionedField< Type, TMesh >& 
{
  void *ptr;
  int res = SWIG_ConvertPtr( $input, (void **) &ptr, $descriptor( Foam::DimensionedField< Type, TMesh > * ), 0 );
  int res1 = SWIG_ConvertPtr( $input, (void **) &ptr, $descriptor( Foam::tmp< Foam::DimensionedField< Type, TMesh > > * ), 0 );
  int res2 = SWIG_ConvertPtr( $input, (void **) &ptr, $descriptor( Foam::tmp< Foam::GeometricField< Type, TPatchField, TMesh > > * ), 0 );
  $1 = SWIG_CheckState( res ) || SWIG_CheckState( res1 ) || SWIG_CheckState( res2 );
}

%typemap( in ) const Foam::DimensionedField< Type, TMesh >& 
{
  void  *argp = 0;
  int res = 0;
  
  res = SWIG_ConvertPtr( $input, &argp, $descriptor(  Foam::DimensionedField< Type, TMesh > * ), %convertptr_flags );
  if ( SWIG_IsOK( res )&& argp  ){
    Foam::DimensionedField< Type, TMesh > * res = %reinterpret_cast( argp, Foam::DimensionedField< Type, TMesh >* );
    $1 = res;
  } else {
      res = SWIG_ConvertPtr( $input, &argp, $descriptor( Foam::tmp< Foam::DimensionedField< Type, TMesh > >* ), %convertptr_flags );
      if ( SWIG_IsOK( res ) && argp ) {
        Foam::tmp<Foam::DimensionedField< Type, TMesh > >* tmp_res = %reinterpret_cast( argp, Foam::tmp< Foam::DimensionedField< Type, TMesh > > * );
        $1 = tmp_res->operator->();
      } else {
          res = SWIG_ConvertPtr( $input, &argp, $descriptor( Foam::tmp< Foam::GeometricField< Type, TPatchField, TMesh > >* ), %convertptr_flags );
          if ( SWIG_IsOK( res ) && argp ) {
            Foam::tmp< Foam::GeometricField< Type, TPatchField, TMesh > >* tmp_res = %reinterpret_cast( argp, Foam::tmp< Foam::GeometricField< Type, TPatchField, TMesh > > * );
            $1 = tmp_res->operator->();
          } else {    
              %argument_fail( res, "$type", $symname, $argnum );
            }
      }
  }
}    
%enddef


//---------------------------------------------------------------------------
%import "Foam/src/OpenFOAM/db/objectRegistry.cxx"

%import "Foam/src/OpenFOAM/db/IOstreams/IOstreams/Ostream.cxx"

%define DIMENSIONED_FIELD_TEMPLATE_FUNC( Type, TMesh )

%extend Foam::DimensionedField< Foam::Type, Foam::TMesh >
{
  FIELD_VIRTUAL_EXTENDS( Type );
  DIMENSIONED_FIELD_VIRTUAL_EXTENDS( Type, TMesh );
  OBJECTREGISTRY_TEMPLATE_2_EXTENDS( DimensionedField, Foam::Type, Foam::TMesh  );
  OSTREAM_EXTENDS;
  
  void ext_assign( const Foam::DimensionedField< Foam::Type, Foam::TMesh >& theArg )
  {
    Foam::Warning << "The “ext_assign” method is obsolete, use “<<” operator instead" << endl;
    get_ref( self ) = theArg;
  }
  
  void __lshift__( const Foam::DimensionedField< Foam::Type, Foam::TMesh >& theArg )
  {
    get_ref( self ) = theArg;
  }

  Foam::dimensioned< Type > ext_sum()
  {
    return Foam::sum( get_ref( self ) );
  }
  
  ISINSTANCE_TEMPLATE_2_EXTEND( DimensionedField, Foam::Type, Foam::TMesh );
  
  __COMMON_DIMENSIONEDFIELD_TEMPLATE_OPERATOR( Type, TMesh );
}

%extend Foam::tmp< Foam::DimensionedField< Foam::Type, Foam::TMesh > >
{
  __COMMON_DIMENSIONEDFIELD_TEMPLATE_OPERATOR( Type, TMesh );    
  
  void __lshift__( const Foam::DimensionedField< Foam::Type, Foam::TMesh >& theArg )
  {
    get_ref( self ) = theArg;
  }

  ISINSTANCE_TEMPLATE_2_EXTEND( DimensionedField, Foam::Type, Foam::TMesh );
  
  SEQUENCE_ADDONS( Foam::Type );

  LISTS_FUNCS( Foam::Type );
  
  IOOBJECT_FUNCTIONS;
}

%enddef


//--------------------------------------------------------------------------------
%define __VECTOR_DIMENSIONED_FIELD_OPERATORS( TMesh )
  Foam::tmp< Foam::DimensionedField< Foam::vector, TMesh > > __div__( const Foam::DimensionedField< Foam::scalar, TMesh >& theArg )
  {
    return get_ref( self ) / theArg;
  }
  
  Foam::tmp< Foam::DimensionedField< Foam::tensor, TMesh > > __mul__( const Foam::DimensionedField< Foam::vector, TMesh >& theArg)
  {
    return get_ref( self ) * theArg;
  }
  Foam::tmp< Foam::DimensionedField< Foam::scalar, TMesh > > __rand__( const Foam::vector& theArg)
  {
    return theArg & get_ref( self );
  }
  Foam::tmp< Foam::DimensionedField< Foam::vector, TMesh > > __rand__( const Foam::tensor& theArg)
  {
    return theArg & get_ref( self );
  }
  Foam::tmp< Foam::DimensionedField< Foam::scalar, TMesh > > __and__( const Foam::DimensionedField< Foam::vector, TMesh >& theArg )
  {
    return  get_ref( self ) & theArg; 
  }
  Foam::tmp< Foam::DimensionedField< Foam::vector, TMesh > > __and__( const Foam::DimensionedField< Foam::tensor, TMesh >& theArg )
  {
    return  get_ref( self ) & theArg; 
  }

%enddef


//---------------------------------------------------------------------------------
%define VECTOR_DIMENSIONED_FIELD_TEMPLATE_FUNC( TMesh )
   DIMENSIONED_FIELD_TEMPLATE_FUNC( vector, TMesh );
   
   %extend Foam::DimensionedField< Foam::vector, Foam::TMesh >
   {
     __VECTOR_DIMENSIONED_FIELD_OPERATORS( TMesh );
   }
   
   %extend Foam::tmp< Foam::DimensionedField< Foam::vector, TMesh > >
   {
     __VECTOR_DIMENSIONED_FIELD_OPERATORS( TMesh );

   }

%enddef


//---------------------------------------------------------------------------------
%define DIMENSIONED_FIELD_VOLMESH_TYPEMAP( Type )

NO_TMP_TYPEMAP_DIMENSIONED_FIELD( Foam::Type, Foam::volMesh, Foam::fvPatchField );

%enddef


//---------------------------------------------------------------------------------
%define DIMENSIONED_FIELD_SURFACEMESH_TYPEMAP( Type )

NO_TMP_TYPEMAP_DIMENSIONED_FIELD( Foam::Type, Foam::surfaceMesh, Foam::fvsPatchField );

%enddef


//---------------------------------------------------------------------------------
#endif

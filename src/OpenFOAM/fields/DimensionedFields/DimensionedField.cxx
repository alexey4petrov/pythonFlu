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
#ifndef DimensionedField_cxx
#define DimensionedField_cxx


//---------------------------------------------------------------------------
%include "src/OpenFOAM/db/regIOobject.cxx"

%include "src/OpenFOAM/fields/Fields/Field.cxx"

%include "src/OpenFOAM/dimensionedTypes/dimensionedType.cxx"

%{
    #include "DimensionedField.H"
%}

%include "DimensionedField.H"


//---------------------------------------------------------------------------
%define DIMENSIONED_FIELD_VIRTUAL_EXTENDS( Type, TMesh )
{
  void ext_assign( const Foam::DimensionedField< Foam::Type, Foam::TMesh >& theSource )
  {
    *dynamic_cast< Foam::DimensionedField< Foam::Type, Foam::TMesh >* >( self ) = theSource;
  }
  
}
%enddef


//---------------------------------------------------------------------------
%define NO_TMP_TYPEMAP_DIMENSIONED_FIELD( Type, TMesh )

%typecheck( SWIG_TYPECHECK_POINTER ) const Foam::DimensionedField< Type, TMesh >& 
{
    void *ptr;
    int res = SWIG_ConvertPtr( $input, (void **) &ptr, $descriptor( Foam::DimensionedField< Type, TMesh > * ), 0 );
    int res1 = SWIG_ConvertPtr( $input, (void **) &ptr, $descriptor( Foam::tmp< Foam::DimensionedField< Type, TMesh > > * ), 0 );
    $1 = SWIG_CheckState( res ) || SWIG_CheckState( res1 );
}

%typemap( in ) const Foam::DimensionedField< Type, TMesh >& 
{
  void  *argp = 0;
  int res = 0;
  
  res = SWIG_ConvertPtr( $input, &argp, $descriptor(  Foam::DimensionedField< Type, TMesh > * ), %convertptr_flags );
  if ( SWIG_IsOK( res )&& argp  ){
    Foam::DimensionedField< Type, TMesh > * res =  %reinterpret_cast( argp, Foam::DimensionedField< Type, TMesh >* );
    $1 = res;
  } else {
    res = SWIG_ConvertPtr( $input, &argp, $descriptor( Foam::tmp< Foam::DimensionedField< Type, TMesh > >* ), %convertptr_flags );
    if ( SWIG_IsOK( res ) && argp ) {
      Foam::tmp<Foam::DimensionedField< Type, TMesh > >* tmp_res =%reinterpret_cast( argp, Foam::tmp< Foam::DimensionedField< Type, TMesh > > * );
      $1 = tmp_res->operator->();
      } else {
        %argument_fail( res, "$type", $symname, $argnum );
        }
    }
 
}    
%enddef


//---------------------------------------------------------------------------
%include "src/OpenFOAM/db/objectRegistry.cxx"

%define DIMENSIONED_FIELD_TEMPLATE_FUNC( Type, TMesh )

%extend Foam::DimensionedField< Foam::Type, Foam::TMesh > COMMON_EXTENDS;

NO_TMP_TYPEMAP_DIMENSIONED_FIELD( Foam::Type, Foam::TMesh );

%extend Foam::DimensionedField< Foam::Type, Foam::TMesh > FIELD_VIRTUAL_EXTENDS( Type );

%extend Foam::DimensionedField< Foam::Type, Foam::TMesh > DIMENSIONED_FIELD_VIRTUAL_EXTENDS( Type, TMesh );

%extend Foam::DimensionedField< Foam::Type, Foam::TMesh > 
{
  OBJECTREGISTRY_TEMPLATE_2_EXTENDS( DimensionedField, Foam::Type, Foam::TMesh  )
    
  void ext_assign( const Foam::DimensionedField< Foam::Type, Foam::TMesh >& theArg )
  {
    *self = theArg;
  }
  
  ISINSTANCE_TEMPLATE_2_EXTEND( DimensionedField, Foam::Type, Foam::TMesh )
}

%include "src/OpenFOAM/db/IOstreams/IOstreams/Ostream.cxx"

%extend Foam::DimensionedField< Foam::Type, Foam::TMesh > OSTREAM_EXTENDS;

%enddef


//--------------------------------------------------------------------------------
#endif

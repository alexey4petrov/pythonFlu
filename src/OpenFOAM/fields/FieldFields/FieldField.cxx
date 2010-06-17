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
#ifndef FieldField_cxx
#define FieldField_cxx


//---------------------------------------------------------------------------
%include "src/common.hxx"

%include "src/redirect2base.hxx"

%include "FieldField.H"

%include "src/OpenFOAM/fields/Fields/scalarField.cxx"

%{
    #include "FieldField.H"
%}


//---------------------------------------------------------------------------
%define NO_TMP_TYPEMAP_FIELDFIELD(  TPatchField, Type )

%typemap( in ) const Foam::FieldField< TPatchField, Type  >& 
{
  void  *argp = 0;
  int res = 0;
  
  res = SWIG_ConvertPtr( $input, &argp, $descriptor(  Foam::FieldField< TPatchField, Type  > * ), %convertptr_flags );
  if ( SWIG_IsOK( res )&& argp  ){
    Foam::FieldField< TPatchField, Type  > * res =  %reinterpret_cast( argp, Foam::FieldField< TPatchField, Type  >* );
    $1 = res;
  } else {
    res = SWIG_ConvertPtr( $input, &argp, $descriptor( Foam::tmp< Foam::FieldField< TPatchField, Type  > >* ), %convertptr_flags );
    if ( SWIG_IsOK( res ) && argp ) {
      Foam::tmp<Foam::FieldField< TPatchField, Type > >* tmp_res =%reinterpret_cast( argp, Foam::tmp< Foam::FieldField< TPatchField, Type  > > * );
      $1 = tmp_res->operator->();
      } else {
        %argument_fail( res, "$type", $symname, $argnum );
        }
    }
 
}    

%enddef
//------------------------------------------------------------------------------
%define BASECLASS_FUNC( TPatchField, Type )
{
  Foam::PtrList< TPatchField< Type > >& base()
  {
    return *self;
  }
  int __len__()
  {
     return self->size();
  }
    
  TPatchField< Type >& __getitem__( const Foam::label theIndex )
  {
     return self->operator[]( theIndex );
  }

  void __setitem__( const Foam::label theIndex, const TPatchField< Type >& theValue )
  {
     self->operator[]( theIndex ) = theValue;
  }
  
}
%enddef


//------------------------------------------------------------------------------
%define _FIELDFIELD_TEMPLATE_FUNC( TPatchField, Type )
{  
  Foam::tmp< Foam::FieldField< TPatchField, Foam::scalar > > magSqr()
  {
     return Foam::magSqr( *self );
  }
  
  Foam::tmp< Foam::FieldField< TPatchField, Type > > __rmul__( const  Foam::scalar& theArg)
  {
     return theArg * *self;
  }
}
%enddef


//-------------------------------------------------------------------------------
%define FIELDFIELD_TEMPLATE_FUNC( TPatchField, Type )

%extend  Foam::FieldField< TPatchField, Type > _FIELDFIELD_TEMPLATE_FUNC( TPatchField, Type );

%extend  Foam::tmp< Foam::FieldField< TPatchField, Type > > _FIELDFIELD_TEMPLATE_FUNC( TPatchField, Type );

%extend  Foam::FieldField< TPatchField, Type > BASECLASS_FUNC( TPatchField, Type );

%enddef


#endif

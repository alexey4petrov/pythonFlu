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
#ifndef fvMatrix_cxx
#define fvMatrix_cxx


//---------------------------------------------------------------------------
// Keep on corresponding "director" includes at the top of SWIG defintion file

%include "src/OpenFOAM/directors.hxx"

%include "src/finiteVolume/directors.hxx"

//---------------------------------------------------------------------------
%include "src/OpenFOAM/fields/tmp/refCount.cxx"

%include "src/OpenFOAM/matrices/lduMatrix/lduMatrix.cxx"

%include "src/OpenFOAM/db/typeInfo/className.hxx"

%{
    #include "fvMatrix.H"
%}

%include "fvMatrix.H"


//---------------------------------------------------------------------------
%include "src/finiteVolume/fields/volFields/volFieldsFwd.hxx"

%include "src/OpenFOAM/fields/tmp/tmp.cxx"


//---------------------------------------------------------------------------
%define NO_TMP_TYPEMAP_FVMATRIX( Type )

%typecheck( SWIG_TYPECHECK_POINTER ) Foam::fvMatrix< Type >& 
{
    void *ptr;
    int res = SWIG_ConvertPtr( $input, (void **) &ptr, $descriptor( Foam::fvMatrix< Type > * ), 0 );
    int res1 = SWIG_ConvertPtr( $input, (void **) &ptr, $descriptor( Foam::tmp< Foam::fvMatrix< Type > > * ), 0 );
    $1 = SWIG_CheckState( res ) || SWIG_CheckState( res1 );
}

%typemap( in ) Foam::fvMatrix< Type >& 
{
  void  *argp = 0;
  int res = 0;
  
  res = SWIG_ConvertPtr( $input, &argp, $descriptor(  Foam::fvMatrix< Type > * ), %convertptr_flags );
  if ( SWIG_IsOK( res )&& argp  ){
    Foam::fvMatrix< Type > * res =  %reinterpret_cast( argp, Foam::fvMatrix< Type >* );
    $1 = res;
  } else {
    res = SWIG_ConvertPtr( $input, &argp, $descriptor( Foam::tmp< Foam::fvMatrix< Type > >* ), %convertptr_flags );
    if ( SWIG_IsOK( res ) && argp ) {
      Foam::tmp<Foam::fvMatrix< Type > >* tmp_res =%reinterpret_cast( argp, Foam::tmp< Foam::fvMatrix< Type > > * );
      $1 = tmp_res->operator->();
      } else {
        %argument_fail( res, "$type", $symname, $argnum );
        }
    }
 
}    
%enddef

//---------------------------------------------------------------------------

%define __COMMON_FVMATRIX_TEMPLATE_FUNC__( Type )
{
    Foam::tmp< Foam::fvMatrix< Type > > __neg__()
    {
        return -get_ref( self );
    }

    Foam::tmp< Foam::fvMatrix< Type > > __add__( const Foam::fvMatrix< Type >& theArg )
    {
        return get_ref( self ) + theArg;
    }

    Foam::tmp< Foam::fvMatrix< Type > > __add__( const Foam::dimensioned< Type >& theArg )
    {
        return get_ref( self ) + theArg;
    }

    Foam::tmp< Foam::fvMatrix< Type > > __sub__( const Foam::fvMatrix< Type >& theArg )
    {
        return get_ref( self ) - theArg;
    }

    Foam::tmp< Foam::fvMatrix< Type > > __add__( const Foam::GeometricField< Type, Foam::fvPatchField, Foam::volMesh >& theArg )
    {
        return get_ref( self ) + theArg;
    }

    Foam::tmp< Foam::fvMatrix< Type > > __radd__( const Foam::GeometricField< Type, Foam::fvPatchField, Foam::volMesh >& theArg )
    {
        return theArg + get_ref( self )  ;
    }

    Foam::tmp< Foam::fvMatrix< Type > > __sub__( const Foam::GeometricField< Type, Foam::fvPatchField, Foam::volMesh >& theArg )
    {
        return get_ref( self ) - theArg;
    }

    Foam::tmp< Foam::fvMatrix< Type > > __eq__( const Foam::fvMatrix< Type >& theArg )
    {
        return get_ref( self ) == theArg;
    }
    Foam::tmp< Foam::fvMatrix< Type > > __eq__( const Foam::GeometricField< Type, Foam::fvPatchField, Foam::volMesh >& theArg )
    {
        return get_ref( self ) == theArg;
    }
    
    Foam::tmp< Foam::fvMatrix< Type > > __eq__( const Foam::dimensioned< Type >& theArg )
    {
        return get_ref( self ) == theArg;
    }
}
%enddef


//---------------------------------------------------------------------------
%define FVMATRIX_TEMPLATE_FUNC( Type )

%include "src/OpenFOAM/fields/tmp/tmp.cxx"

NO_TMP_TYPEMAP_FVMATRIX( Type );

%extend Foam::fvMatrix< Type > COMMON_EXTENDS;

%extend Foam::tmp< Foam::fvMatrix< Type > > COMMON_EXTENDS;


%extend Foam::fvMatrix< Type > __COMMON_FVMATRIX_TEMPLATE_FUNC__( Type )

%extend Foam::tmp< Foam::fvMatrix< Type > > __COMMON_FVMATRIX_TEMPLATE_FUNC__( Type )


%include "src/OpenFOAM/matrices/lduMatrix/lduMatrix.cxx"
%include "src/OpenFOAM/db/IOstreams/IOstreams/Istream.cxx"

%inline
%{
    Foam::lduSolverPerformance solve( Foam::fvMatrix< Type >& fvm, Foam::Istream& solverControls )
    {
        return Foam::solve( fvm, solverControls );
    }
#if ( __FOAM_VERSION__ >= 010600 )
    Foam::lduSolverPerformance solve( Foam::fvMatrix< Type >& fvm, Foam::dictionary& solverControls )
    {
        return Foam::solve( fvm, solverControls );
    }
#endif    
    Foam::lduSolverPerformance solve( Foam::fvMatrix< Type >& fvm )
    {
        return Foam::solve( fvm );
    }

%}


%inline
%{
    void checkMethod( const Foam::fvMatrix< Type >& fvm1, const Foam::fvMatrix< Type >& fvm2, const char* op )
    {
        return checkMethod< Type >( fvm1, fvm2, op );
    }

#if ( __FOAM_VERSION__ < 010600 )
    void checkMethod( const Foam::fvMatrix< Type >& fvm, const Foam::GeometricField< Type, Foam::fvPatchField, Foam::volMesh >& gf, const char* op )
    {
        return checkMethod< Type >( fvm, gf, op );
    }
#else
    void checkMethod( const Foam::fvMatrix< Type >& fvm, const Foam::DimensionedField< Type, Foam::volMesh >& df, const char* op )
    {
        return checkMethod< Type >( fvm, df, op );
    }
#endif

    void checkMethod( const Foam::fvMatrix< Type >& fvm, const Foam::dimensioned< Type >& dt, const char* op)
    {
        return checkMethod< Type >( fvm, dt, op );
    }
%}

%enddef


//---------------------------------------------------------------------------

#endif

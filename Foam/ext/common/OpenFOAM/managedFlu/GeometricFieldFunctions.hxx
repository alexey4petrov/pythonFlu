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
//  Author : Alexey PETROV, Andrey SIMURZIN


//---------------------------------------------------------------------------
#ifndef GeometricFieldFunctions_hxx
#define GeometricFieldFunctions_hxx


//---------------------------------------------------------------------------
%define GEOMETRICFIELDHOLDER_PYAPPEND_RETURN_SELF_COMPOUND_OPERATOR( Type, TPatchField, TMesh )

PYAPPEND_RETURN_SELF_COMPOUND_OPERATOR_TEMPLATE_3( Foam::GeometricFieldHolder, Type, TPatchField, TMesh, __imul__ );

PYAPPEND_RETURN_SELF_COMPOUND_OPERATOR_TEMPLATE_3( Foam::GeometricFieldHolder, Type, TPatchField, TMesh, __iadd__ );

PYAPPEND_RETURN_SELF_COMPOUND_OPERATOR_TEMPLATE_3( Foam::GeometricFieldHolder, Type, TPatchField, TMesh, __isub__ );

PYAPPEND_RETURN_SELF_COMPOUND_OPERATOR_TEMPLATE_3( Foam::GeometricFieldHolder, Type, TPatchField, TMesh, __idiv__ );

%enddef

%define GEOMETRICFIELDHOLDER_CLEAR_PYAPPEND_RETURN_SELF_COMPOUND_OPERATOR( Type, TPatchField, TMesh )

CLEAR_PYAPPEND_RETURN_SELF_COMPOUND_OPERATOR_TEMPLATE_3( Foam::GeometricFieldHolder, Type, TPatchField, TMesh, __idiv__ );

CLEAR_PYAPPEND_RETURN_SELF_COMPOUND_OPERATOR_TEMPLATE_3( Foam::GeometricFieldHolder, Type, TPatchField, TMesh, __isub__ );

CLEAR_PYAPPEND_RETURN_SELF_COMPOUND_OPERATOR_TEMPLATE_3( Foam::GeometricFieldHolder, Type, TPatchField, TMesh, __iadd__ );

CLEAR_PYAPPEND_RETURN_SELF_COMPOUND_OPERATOR_TEMPLATE_3( Foam::GeometricFieldHolder, Type, TPatchField, TMesh, __imul__ );

%enddef


//--------------------------------------------------------------------------------------
%define COMMON_EXTEND_GEOMETRICFIELDHOLDER( Type, TPatchField, TMesh )

  Foam::GeometricFieldHolder< Type, TPatchField, TMesh > __add__ ( 
    const Foam::GeometricFieldHolder< Type, TPatchField, TMesh >& field )
  {
    return *self + field;
  }
  
  Foam::GeometricFieldHolder< Type, TPatchField, TMesh > __sub__ ( 
    const Foam::GeometricFieldHolder< Type, TPatchField, TMesh >& field )
  {
    return *self - field;
  }


  HOLDERS_CALL_SMART_TMP_EXTENSION_TEMPLATE3( Foam::GeometricField, Type, TPatchField, TMesh );
  
  void __lshift__( const Foam::dimensioned< Type >& theArg )
  {
    get_ref( self ) = theArg;
  }

  void __lshift__ ( const Foam::GeometricFieldHolder< Type, TPatchField, TMesh >& field )
  {
    *self = field;
  }

  void __lshift__ ( const Foam::smart_tmp< Foam::GeometricField< Type, TPatchField, TMesh > >& field )
  {
    *self = field;
  }
  
  void __imul__( const Foam::smart_tmp< Foam::GeometricField< Foam::scalar, TPatchField, TMesh > >& theArg )
  {
    get_ref( self ) *= theArg;
  }    

  void __idiv__( const Foam::smart_tmp< Foam::GeometricField< Foam::scalar, TPatchField, TMesh > >& theArg )
  {
    get_ref( self ) /= theArg;
  }    

  void __iadd__( const Foam::smart_tmp< Foam::GeometricField< Type, TPatchField, TMesh > >& theArg )
  {
    get_ref( self ) += theArg;
  }    

  void __isub__( const Foam::smart_tmp< Foam::GeometricField< Type, TPatchField, TMesh > >& theArg )
  {
    get_ref( self ) -= theArg;
  }    
  
  void __imul__( const Foam::dimensioned< Foam::scalar >& theArg )
  {
    get_ref( self ) *= theArg;
  }    

  void __idiv__( const Foam::dimensioned< Foam::scalar >& theArg )
  {
    get_ref( self ) /= theArg;
  }    

  void __iadd__( const Foam::dimensioned< Type >& theArg )
  {
    get_ref( self ) += theArg;
  }    

  void __isub__( const Foam::dimensioned< Type >& theArg )
  {
    get_ref( self ) -= theArg;
  }
  
  Foam::GeometricFieldHolder< Type, TPatchField, TMesh > __div__ ( 
    const Foam::GeometricFieldHolder< Foam::scalar, TPatchField, TMesh >& field )
  {
    return *self / field;
  }

  Foam::GeometricFieldHolder< Type, TPatchField, TMesh > __div__ ( 
    const Foam::dimensionedScalar& dm )
  {
    return *self / dm;
  }
  
  Foam::GeometricFieldHolder< Type, TPatchField, TMesh > __neg__ ()
  {
    return - *self;
  }
  
  Foam::GeometricFieldHolder< scalar, TPatchField, TMesh > mag ()
  {
    return Foam::mag( *self );
  }

  Foam::GeometricFieldHolder< Type, TPatchField, TMesh > __rmul__ ( 
    const Foam::GeometricFieldHolder< Foam::scalar, TPatchField, TMesh >& field )
  {
    return field * *self;
  }
  
  Foam::GeometricFieldHolder< Type, TPatchField, TMesh > __radd__ ( 
    const Foam::dimensioned< Type >& dmS )
  {
    return dmS + *self;
  }



%enddef


//---------------------------------------------------------------------------
%define SCALARFIELDHOLDER_EXTEND( TPatchField, TMesh )

  Foam::GeometricFieldHolder< Foam::scalar, TPatchField, TMesh > __rmul__ ( 
    const Foam::dimensioned< Foam::scalar >& dmS )
  {
    return dmS * *self;
  }
    
  Foam::GeometricFieldHolder< Foam::scalar, TPatchField, TMesh > __mul__ ( 
    const Foam::dimensioned< Foam::scalar >& dmS )
  {
    return *self * dmS;
  }
  
  Foam::GeometricFieldHolder< Foam::scalar, TPatchField, TMesh > __rdiv__ ( const Foam::scalar& value )
  {
    return value / *self;
  }

  Foam::GeometricFieldHolder< Foam::scalar, TPatchField, TMesh > __rsub__ ( const Foam::scalar& value )
  {
    return value - *self;
  }
  
  Foam::GeometricFieldHolder< Foam::scalar, TPatchField, TMesh > __sub__ ( const Foam::scalar& value )
  {
    return *self - value;
  }

  Foam::GeometricFieldHolder< Foam::scalar, TPatchField, TMesh > __rmul__ ( const Foam::scalar& value )
  {
    return value * *self;
  }

  Foam::GeometricFieldHolder< Foam::vector, TPatchField, TMesh  > __mul__ ( 
    const Foam::GeometricFieldHolder< Foam::vector, TPatchField, TMesh  >& field )
  {
    return *self * field;
  }

  Foam::GeometricFieldHolder< Foam::scalar, TPatchField, TMesh  > __mul__ ( 
    const Foam::GeometricFieldHolder< Foam::scalar, TPatchField, TMesh  >& field )
  {
    return *self * field;
  }

%enddef


//---------------------------------------------------------------------------
%define VECTORFIELDHOLDER_EXTEND( TPatchField, TMesh )
  
  Foam::GeometricFieldHolder< Foam::scalar, TPatchField, TMesh > __and__ ( 
    const Foam::GeometricFieldHolder< Foam::vector, TPatchField, TMesh >& field )
  {
    return *self & field;
  }
  
  Foam::GeometricFieldHolder< Foam::scalar, TPatchField, TMesh  >
    __rand__( const Foam::UniformDimensionedFieldHolder< Foam::vector >& theArg ) const
  {
    return theArg & *self;
  }

  Foam::GeometricFieldHolder< Foam::vector, TPatchField, TMesh  >
    __rand__( const Foam::GeometricFieldHolder< Foam::tensor, TPatchField, TMesh  >& theArg ) const
  {
    return theArg & *self;
  }
  
  Foam::GeometricFieldHolder< Foam::scalar, TPatchField, TMesh  >
    __rand__( const Foam::vector& theArg ) const
  {
    return theArg & *self;
  }

%enddef


//---------------------------------------------------------------------------
%define EXTEND_VOLSCALARFIELDHOLDER

%extend Foam::GeometricFieldHolder< Foam::scalar, Foam::fvPatchField, Foam::volMesh >
{

  GEOMETRICFIELDHOLDER_PYAPPEND_RETURN_SELF_COMPOUND_OPERATOR( Foam::scalar, Foam::fvPatchField, Foam::volMesh );
  COMMON_EXTEND_GEOMETRICFIELDHOLDER( Foam::scalar, Foam::fvPatchField, Foam::volMesh );  
  GEOMETRICFIELDHOLDER_CLEAR_PYAPPEND_RETURN_SELF_COMPOUND_OPERATOR( Foam::scalar, Foam::fvPatchField, Foam::volMesh );
  
  SCALARFIELDHOLDER_EXTEND( Foam::fvPatchField, Foam::volMesh );
}
%enddef


//--------------------------------------------------------------------------------------
%define EXTEND_VOLVECTORFIELDHOLDER
%extend Foam::GeometricFieldHolder< Foam::vector, Foam::fvPatchField, Foam::volMesh >
{
  VECTORFIELDHOLDER_EXTEND( Foam::fvPatchField, Foam::volMesh );
  
}
%enddef


//--------------------------------------------------------------------------------------
%define EXTEND_SURFACEVECTORFIELDHOLDER
%extend Foam::GeometricFieldHolder< Foam::vector, Foam::fvsPatchField, Foam::surfaceMesh >
{
  VECTORFIELDHOLDER_EXTEND( Foam::fvsPatchField, Foam::surfaceMesh );
}
%enddef


//--------------------------------------------------------------------------------------
%define EXTEND_SURFACESCALARFIELDHOLDER
%extend Foam::GeometricFieldHolder< Foam::scalar, Foam::fvsPatchField, Foam::surfaceMesh >
{
  GEOMETRICFIELDHOLDER_PYAPPEND_RETURN_SELF_COMPOUND_OPERATOR( Foam::scalar, Foam::fvsPatchField, Foam::surfaceMesh );
  COMMON_EXTEND_GEOMETRICFIELDHOLDER( Foam::scalar, Foam::fvsPatchField, Foam::surfaceMesh );
  GEOMETRICFIELDHOLDER_CLEAR_PYAPPEND_RETURN_SELF_COMPOUND_OPERATOR( Foam::scalar, Foam::fvsPatchField, Foam::surfaceMesh );
  
  SCALARFIELDHOLDER_EXTEND( Foam::fvsPatchField, Foam::surfaceMesh );  
}
%enddef


//--------------------------------------------------------------------------------------
%define EXTEND_VOLTENSORFIELDHOLDER

%extend Foam::GeometricFieldHolder< Foam::tensor, Foam::fvPatchField, Foam::volMesh >
{

  GEOMETRICFIELDHOLDER_PYAPPEND_RETURN_SELF_COMPOUND_OPERATOR( Foam::tensor, Foam::fvPatchField, Foam::volMesh );
  COMMON_EXTEND_GEOMETRICFIELDHOLDER( Foam::tensor, Foam::fvPatchField, Foam::volMesh );  
  GEOMETRICFIELDHOLDER_CLEAR_PYAPPEND_RETURN_SELF_COMPOUND_OPERATOR( Foam::tensor, Foam::fvPatchField, Foam::volMesh );
}

%enddef

//--------------------------------------------------------------------------------------
#endif

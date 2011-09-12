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
%define EXTEND_VOLSCALARFIELDHOLDER
%extend Foam::GeometricFieldHolder< Foam::scalar, Foam::fvPatchField, Foam::volMesh >
{
  Foam::GeometricFieldHolder< Foam::scalar, Foam::fvPatchField, Foam::volMesh > __add__ ( 
    const Foam::GeometricFieldHolder< Foam::scalar, Foam::fvPatchField, Foam::volMesh >& field )
  {
    return *self + field;
  }
  
  void ext_assign ( const Foam::GeometricFieldHolder< Foam::scalar, Foam::fvPatchField, Foam::volMesh >& field )
  {
    *self = field;
  }
  
  Foam::GeometricFieldHolder< Foam::scalar, Foam::fvPatchField, Foam::volMesh > mag ()
  {
    return Foam::mag( *self );
  }

  Foam::GeometricFieldHolder< Foam::scalar, Foam::fvPatchField, Foam::volMesh > __rdiv__ ( const Foam::scalar& value )
  {
    return value / *self;
  }

  Foam::GeometricFieldHolder< Foam::vector, Foam::fvPatchField, Foam::volMesh > __mul__ ( 
    const Foam::GeometricFieldHolder< Foam::vector, Foam::fvPatchField, Foam::volMesh >& field )
  {
    return *self * field;
  }

  Foam::GeometricFieldHolder< Foam::scalar, Foam::fvPatchField, Foam::volMesh > __mul__ ( 
    const Foam::GeometricFieldHolder< Foam::scalar, Foam::fvPatchField, Foam::volMesh >& field )
  {
    return *self * field;
  }

  Foam::GeometricFieldHolder< Foam::scalar, Foam::fvPatchField, Foam::volMesh > __sub__ ( 
    const Foam::GeometricFieldHolder< Foam::scalar, Foam::fvPatchField, Foam::volMesh >& field )
  {
    return *self - field;
  }

}
%enddef


//--------------------------------------------------------------------------------------
%define EXTEND_VOLVECTORFIELDHOLDER
%extend Foam::GeometricFieldHolder< Foam::vector, Foam::fvPatchField, Foam::volMesh >
{
  Foam::GeometricFieldHolder< Foam::vector, Foam::fvPatchField, Foam::volMesh > __add__ ( 
    const Foam::GeometricFieldHolder< Foam::vector, Foam::fvPatchField, Foam::volMesh >& field )
  {
    return *self + field;
  }

  Foam::GeometricFieldHolder< Foam::vector, Foam::fvPatchField, Foam::volMesh > __sub__ ( 
    const Foam::GeometricFieldHolder< Foam::vector, Foam::fvPatchField, Foam::volMesh >& field )
  {
    return *self - field;
  }

  void ext_assign( const Foam::GeometricFieldHolder< Foam::vector, Foam::fvPatchField, Foam::volMesh >& field )
  {
    *self = field;
  }
  
  Foam::GeometricFieldHolder< Foam::vector, Foam::fvPatchField, Foam::volMesh > __neg__ ()
  {
    return - *self;
  }

}
%enddef


//--------------------------------------------------------------------------------------
%define EXTEND_SURFACEVECTORFIELDHOLDER
%extend Foam::GeometricFieldHolder< Foam::vector, Foam::fvsPatchField, Foam::surfaceMesh >
{
  Foam::GeometricFieldHolder< Foam::vector, Foam::fvsPatchField, Foam::surfaceMesh > __add__ ( 
    const Foam::GeometricFieldHolder< Foam::vector, Foam::fvsPatchField, Foam::surfaceMesh >& field )
  {
    return *self + field;
  }

  void ext_assign( const Foam::GeometricFieldHolder< Foam::vector, Foam::fvsPatchField, Foam::surfaceMesh >& field )
  {
    *self = field;
  }


  Foam::GeometricFieldHolder< Foam::scalar, Foam::fvsPatchField, Foam::surfaceMesh > __and__ ( 
    const Foam::GeometricFieldHolder< Foam::vector, Foam::fvsPatchField, Foam::surfaceMesh >& field )
  {
    return *self & field;
  }
  
}
%enddef


//--------------------------------------------------------------------------------------
%define EXTEND_SURFACESCALARFIELDHOLDER
%extend Foam::GeometricFieldHolder< Foam::scalar, Foam::fvsPatchField, Foam::surfaceMesh >
{
  Foam::GeometricFieldHolder< Foam::scalar, Foam::fvsPatchField, Foam::surfaceMesh > __add__ ( 
    const Foam::GeometricFieldHolder< Foam::scalar, Foam::fvsPatchField, Foam::surfaceMesh >& field )
  {
    return *self + field;
  }

  Foam::GeometricFieldHolder< Foam::scalar, Foam::fvsPatchField, Foam::surfaceMesh > __mul__ ( 
    const Foam::GeometricFieldHolder< Foam::scalar, Foam::fvsPatchField, Foam::surfaceMesh >& field )
  {
    return *self * field;
  }
  
  Foam::GeometricFieldHolder< Foam::scalar, Foam::fvsPatchField, Foam::surfaceMesh > __sub__ ( 
    const Foam::GeometricFieldHolder< Foam::scalar, Foam::fvsPatchField, Foam::surfaceMesh >& field )
  {
    return *self - field;
  }

  void ext_assign( const Foam::GeometricFieldHolder< Foam::scalar, Foam::fvsPatchField, Foam::surfaceMesh >& field )
  {
    *self = field;
  }


  Foam::GeometricFieldHolder< Foam::scalar, Foam::fvsPatchField, Foam::surfaceMesh > mag ()
  {
    return Foam::mag( *self );
  }
  
  Foam::GeometricFieldHolder< Foam::scalar, Foam::fvsPatchField, Foam::surfaceMesh > __neg__ ()
  {
    return - *self;
  }

}
%enddef


//--------------------------------------------------------------------------------------
#endif

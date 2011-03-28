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
#ifndef volMesh_hxx
#define volMesh_hxx


//---------------------------------------------------------------------------
%include "src/OpenFOAM/meshes/GeoMesh_fvMesh.hxx"

%import "src/OpenFOAM/dimensionedTypes/dimensionedScalar.cxx"

%import "src/OpenFOAM/fields/Fields/scalarField.cxx"

%import "src/OpenFOAM/dimensionSet.cxx"


//---------------------------------------------------------------------------
%typecheck( SWIG_TYPECHECK_POINTER ) const Foam::volMesh::Mesh &
{
  void *ptr;
  int res = SWIG_ConvertPtr( $input, (void **) &ptr, $descriptor( Foam::volMesh::Mesh * ), 0 );
  int res1 = SWIG_ConvertPtr( $input, (void **) &ptr, $descriptor( Foam::fvMesh * ), 0 );
  $1 = SWIG_CheckState( res ) || SWIG_CheckState( res1 );
}


//---------------------------------------------------------------------------
%typemap( in ) const Foam::volMesh::Mesh & 
{
  void  *argp = 0;
  int res = 0;
  
  res = SWIG_ConvertPtr( $input, &argp, $descriptor( Foam::volMesh::Mesh * ), %convertptr_flags );
  if ( SWIG_IsOK( res )&& argp  ){
    $1 = %reinterpret_cast( argp, Foam::volMesh::Mesh * );;
  } else {
    res = SWIG_ConvertPtr( $input, &argp, $descriptor( Foam::fvMesh * ), %convertptr_flags );
    if ( SWIG_IsOK( res ) && argp ) {
      $1 = %reinterpret_cast( argp, fvMesh * );
    } else {
      %argument_fail( res, "$type", $symname, $argnum );
    }
  }
}


//---------------------------------------------------------------------------
#endif

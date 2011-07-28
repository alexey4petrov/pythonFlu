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
#ifndef fvcSup_cxx
#define fvcSup_cxx


//---------------------------------------------------------------------------
%module "Foam.src.finiteVolume.finiteVolume.fvc.fvcSup";
%{
  #include "Foam/src/finiteVolume/finiteVolume/fvc/fvcSup.hh"
%}


//---------------------------------------------------------------------------
%import "Foam/src/finiteVolume/fvMesh/fvMeshes.cxx"

%import "Foam/src/OpenFOAM/dimensionedTypes/dimensionedScalar.cxx"


//---------------------------------------------------------------------------
%define FVC_SUP_TEMPLATE_FUNC( Type )
%{

Foam::tmp< Foam::GeometricField< Type, Foam::fvPatchField, Foam::volMesh > >
fvc_Su( const Foam::GeometricField< Type, Foam::fvPatchField, Foam::volMesh>& su, 
        Foam::GeometricField< Type, Foam::fvPatchField, Foam::volMesh>& vf )
{
  return Foam::fvc::Su( su, vf );
}
    
Foam::tmp< Foam::GeometricField< Type, Foam::fvPatchField, Foam::volMesh > >
fvc_Sp( const Foam::volScalarField& sp,
        Foam::GeometricField< Type, Foam::fvPatchField, Foam::volMesh >& vf )
{
  return Foam::fvc::Sp( sp, vf );
}

Foam::tmp< Foam::GeometricField< Type, Foam::fvPatchField, Foam::volMesh > >
fvc_Sp( const Foam::dimensionedScalar& sp,
        Foam::GeometricField< Type, Foam::fvPatchField, Foam::volMesh >& vf )
{
  return Foam::fvc::Sp( sp, vf );
}


Foam::tmp< Foam::GeometricField< Type, Foam::fvPatchField, Foam::volMesh > >
fvc_SuSp( const Foam::volScalarField& sp,
          Foam::GeometricField< Type, Foam::fvPatchField, Foam::volMesh >& vf)
{
  return Foam::fvc::SuSp( sp, vf );
}

%}
%enddef


//---------------------------------------------------------------------------
%inline FVC_SUP_TEMPLATE_FUNC( Foam::scalar );

%inline FVC_SUP_TEMPLATE_FUNC( Foam::vector );


//---------------------------------------------------------------------------
%include <fvcSup.H>


//---------------------------------------------------------------------------
#endif

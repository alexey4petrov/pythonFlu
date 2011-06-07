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
#ifndef fvcVolumeIntegrate_cxx
#define fvcVolumeIntegrate_cxx


//---------------------------------------------------------------------------
%module "Foam.src.finiteVolume.finiteVolume.fvc.fvcVolumeIntegrate";
%{
  #include "src/finiteVolume/finiteVolume/fvc/fvcVolumeIntegrate.hh"
%}


//---------------------------------------------------------------------------
%import "src/finiteVolume/fvMesh/fvMeshes.cxx"

%import "src/OpenFOAM/fields/Fields/primitiveFields.cxx"

%import "src/OpenFOAM/dimensionedTypes/dimensionedTypes.cxx"


//---------------------------------------------------------------------------
%define FVC_VOLUME_INTEGRATE_ADDONS( Type )

%inline
{
  Foam::tmp< Foam::Field< Type > > 
  fvc_volumeIntegrate( const Foam::GeometricField< Type, Foam::fvPatchField, Foam::volMesh >& vf )
  {
    return Foam::fvc::volumeIntegrate( vf );
  }
}

%inline
{
  Foam::dimensioned< Type > 
  fvc_domainIntegrate( const Foam::GeometricField< Type, Foam::fvPatchField, Foam::volMesh >& vf )
  {
    return Foam::fvc::domainIntegrate( vf );
  }
}

%enddef


//---------------------------------------------------------------------------
FVC_VOLUME_INTEGRATE_ADDONS( Foam::vector );

FVC_VOLUME_INTEGRATE_ADDONS( Foam::scalar );


//---------------------------------------------------------------------------
%include <fvcVolumeIntegrate.H>


//---------------------------------------------------------------------------
#endif

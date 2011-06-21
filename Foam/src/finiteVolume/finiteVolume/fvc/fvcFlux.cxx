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
#ifndef fvcFlux_cxx
#define fvcFlux_cxx


//---------------------------------------------------------------------------
%module "Foam.src.finiteVolume.finiteVolume.fvc.fvcFlux";
%{
  #include "Foam/src/finiteVolume/finiteVolume/fvc/fvcFlux.hh"
%}


//---------------------------------------------------------------------------
%import "Foam/src/finiteVolume/fvMesh/fvMeshes.cxx"


//---------------------------------------------------------------------------
%define FVC_FLUX_TEMPLATE_FUNC( Type )
%{
  Foam::tmp< Foam::GeometricField< Type, Foam::fvsPatchField, Foam::surfaceMesh > > 
  fvc_flux( const Foam::surfaceScalarField& phi,
            const Foam::GeometricField< Type, Foam::fvPatchField, Foam::volMesh >& vf,
            const Foam::word& name )
  {
    return Foam::fvc::flux( phi, vf, name );
  }
    
  Foam::tmp< Foam::GeometricField< Type, Foam::fvsPatchField, Foam::surfaceMesh > > 
  fvc_flux( const Foam::surfaceScalarField& phi,
            const Foam::GeometricField< Type, Foam::fvPatchField, Foam::volMesh >& vf )
  {
    return Foam::fvc::flux( phi, vf);
  }
%}
%enddef


//---------------------------------------------------------------------------
%inline FVC_FLUX_TEMPLATE_FUNC( Foam::scalar );

%inline FVC_FLUX_TEMPLATE_FUNC( Foam::vector );

%inline FVC_FLUX_TEMPLATE_FUNC( Foam::tensor );


//---------------------------------------------------------------------------
%include <fvcFlux.H>


//---------------------------------------------------------------------------
#endif

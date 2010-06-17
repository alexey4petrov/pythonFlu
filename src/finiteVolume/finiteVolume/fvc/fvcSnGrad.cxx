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
#ifndef fvcSnGrad_cxx
#define fvcSnGrad_cxx


//---------------------------------------------------------------------------
// Keep on corresponding "director" includes at the top of SWIG defintion file

%include "src/OpenFOAM/directors.hxx"

%include "src/finiteVolume/directors.hxx"


//---------------------------------------------------------------------------
%include "src/finiteVolume/fields/volFields/volFields.cxx"
%include "src/finiteVolume/fields/surfaceFields/surfaceFields.cxx"

%{
    #include "fvcSnGrad.H"
%}


//---------------------------------------------------------------------------
%define FVC_SNGRAD_ADDONS( Type )

%inline
{
  Foam::tmp< Foam::GeometricField< Type, Foam::fvsPatchField, Foam::surfaceMesh > > fvc_snGrad
  ( const Foam::GeometricField< Type, Foam::fvPatchField, Foam::volMesh >& vf,
    const Foam::word& name
  )
  {
    return Foam::fvc::snGrad( vf, name) ;
  }
  
  Foam::tmp< Foam::GeometricField< Type, Foam::fvsPatchField, Foam::surfaceMesh > > fvc_snGrad
  ( const Foam::GeometricField< Type, Foam::fvPatchField, Foam::volMesh >& vf )
  {
    return Foam::fvc::snGrad(vf);
  }
  
}
%enddef


//---------------------------------------------------------------------------
%include "src/OpenFOAM/fields/tmp/tmp_volVectorField.cxx"

FVC_SNGRAD_ADDONS( Foam::vector )


//---------------------------------------------------------------------------
%include "src/OpenFOAM/fields/tmp/tmp_volScalarField.cxx"

FVC_SNGRAD_ADDONS( Foam::scalar )


//----------------------------------------------------------------------------
%include "fvcGrad.H"


//---------------------------------------------------------------------------
#endif

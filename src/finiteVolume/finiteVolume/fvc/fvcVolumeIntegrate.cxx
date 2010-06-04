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
#ifndef fvcVolumeIntegrate_cxx
#define fvcVolumeIntegrate_cxx


//---------------------------------------------------------------------------
// Keep on corresponding "director" includes at the top of SWIG defintion file

%include "src/OpenFOAM/directors.hxx"

%include "src/finiteVolume/directors.hxx"


//---------------------------------------------------------------------------
%include "src/finiteVolume/fields/volFields/volFields.cxx"

%include "src/OpenFOAM/fields/Fields/primitiveFields.cxx"

%include "src/OpenFOAM/dimensionedTypes/dimensionedTypes.cxx"

%{
    #include "fvcVolumeIntegrate.H"
%}


//---------------------------------------------------------------------------
%define FVC_VOLUME_INTEGRATE_ADDONS( Type )

%inline
{
    Foam::tmp< Foam::Field< Type > > fvc_volumeIntegrate
    ( 
        const Foam::GeometricField< Type, Foam::fvPatchField, Foam::volMesh >& vf 
    )
    {
        return Foam::fvc::volumeIntegrate( vf );
    }
}

%inline
{
    Foam::dimensioned< Type > fvc_domainIntegrate
    ( 
        const Foam::GeometricField< Type, Foam::fvPatchField, Foam::volMesh >& vf 
    )
    {
        return Foam::fvc::domainIntegrate( vf );
    }
}

%enddef


//---------------------------------------------------------------------------
%include "src/OpenFOAM/fields/tmp/tmp_volVectorField.cxx"

FVC_VOLUME_INTEGRATE_ADDONS( Foam::vector )


//---------------------------------------------------------------------------
%include "src/OpenFOAM/fields/tmp/tmp_volScalarField.cxx"

FVC_VOLUME_INTEGRATE_ADDONS( Foam::scalar )


//---------------------------------------------------------------------------
%include "fvcVolumeIntegrate.H"


//---------------------------------------------------------------------------
#endif

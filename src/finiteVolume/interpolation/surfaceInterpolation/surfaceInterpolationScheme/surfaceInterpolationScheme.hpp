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
#ifndef surfaceInterpolationScheme_cxx
#define surfaceInterpolationScheme_cxx

//---------------------------------------------------------------------------
// Keep on corresponding "director" includes at the top of SWIG defintion file

%include "src/OpenFOAM/directors.hxx"

%include "src/finiteVolume/directors.hxx"


//---------------------------------------------------------------------------
%include "src/finiteVolume/fields/volFields/volFields.cxx"

%include "src/finiteVolume/fields/surfaceFields/surfaceFields.cxx"


//---------------------------------------------------------------------------
%{
    #include "surfaceInterpolationScheme.H"
%}


//---------------------------------------------------------------------------
%include "surfaceInterpolationScheme.H"


//---------------------------------------------------------------------------
%define SURFACEINTRPOLATIONSCHEME_TEMPLATE_FUNC( Type )
{
   Foam::surfaceScalarField& ext_weights( const Foam::GeometricField< Foam::Type, Foam::fvPatchField, Foam::volMesh >& theArg )
   {
      return self->weights( theArg )();
   }
   
   static Foam::tmp<Foam::GeometricField< Foam::Type, Foam::fvsPatchField, Foam::surfaceMesh > >
   ext_interpolate( 
              const Foam::GeometricField< Foam::Type, fvPatchField, volMesh >& vf,
              const Foam::tmp< Foam::surfaceScalarField >& tlambdas,
              const Foam::tmp< Foam::surfaceScalarField >& tys )
   {
     return Foam::surfaceInterpolationScheme< Foam::Type >::interpolate( vf, tlambdas, tys );
   }
   
   static Foam::tmp<Foam::GeometricField< Foam::Type, Foam::fvsPatchField, Foam::surfaceMesh > >
   ext_interpolate( 
              const Foam::GeometricField< Foam::Type, fvPatchField, volMesh >& vf,
              const Foam::tmp< Foam::surfaceScalarField >& tlambdas )
   {
     return Foam::surfaceInterpolationScheme< Foam::Type >::interpolate( vf, tlambdas );
   }
}
%enddef
#endif

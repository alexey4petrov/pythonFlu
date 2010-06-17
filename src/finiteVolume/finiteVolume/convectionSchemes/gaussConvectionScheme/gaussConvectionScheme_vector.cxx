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
#ifndef gaussConvectionScheme_vector_cxx
#define gaussConvectionScheme_vector_cxx


//---------------------------------------------------------------------------
// Keep on corresponding "director" includes at the top of SWIG defintion file

%include "src/OpenFOAM/directors.hxx"

%include "src/finiteVolume/directors.hxx"


//---------------------------------------------------------------------------
%include "src/finiteVolume/finiteVolume/convectionSchemes/gaussConvectionScheme/gaussConvectionScheme.cxx"
%include "src/finiteVolume/finiteVolume/convectionSchemes/convectionScheme/convectionScheme_vector.cxx"


//----------------------------------------------------------------------------
%template ( gaussConvectionScheme_vector ) Foam::fv::gaussConvectionScheme< Foam::vector >;


//---------------------------------------------------------------------------
%extend Foam::fv::gaussConvectionScheme< Foam::vector >
{
  Foam::fv::gaussConvectionScheme< Foam::vector >( const Foam::fvMesh& mesh,
                                                   const Foam::surfaceScalarField& faceFlux,
                                                   const Foam::surfaceInterpolationScheme< Foam::vector >& scheme )
  {
     return new Foam::fv::gaussConvectionScheme< Foam::vector >( mesh, faceFlux, scheme );
  }                                                 

}
#endif

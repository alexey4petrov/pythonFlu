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
#ifndef LimitedScheme_vector_MUSCLLimiter_NVDTVD_limitFuncs_magSqr_cxx
#define LimitedScheme_vector_MUSCLLimiter_NVDTVD_limitFuncs_magSqr_cxx

//---------------------------------------------------------------------------
// Keep on corresponding "director" includes at the top of SWIG defintion file

%include "src/OpenFOAM/directors.hxx"

%include "src/finiteVolume/directors.hxx"


//---------------------------------------------------------------------------
%include "src/finiteVolume/interpolation/surfaceInterpolation/limitedSchemes/limitedSurfaceInterpolationScheme/limitedSurfaceInterpolationScheme_vector.cxx"

%include "src/finiteVolume/interpolation/surfaceInterpolation/limitedSchemes/MUSCL/MUSCL_NVDTVD.cxx"

%include "src/finiteVolume/interpolation/surfaceInterpolation/limitedSchemes/LimitedScheme/LimitFuncs.cxx"

%include "src/finiteVolume/interpolation/surfaceInterpolation/limitedSchemes/LimitedScheme/LimitedScheme.cxx"


//----------------------------------------------------------------------------
%ignore Foam::LimitedScheme< Foam::vector, Foam::MUSCLLimiter< Foam::NVDTVD>, Foam::limitFuncs::magSqr>::typeName;


%template ( LimitedScheme_vector_MUSCLLimiter_NVDTVD_limitFuncs_magSqr ) Foam::LimitedScheme< Foam::vector, Foam::MUSCLLimiter< Foam::NVDTVD>, Foam::limitFuncs::magSqr>;


//---------------------------------------------------------------------------
#endif

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
//  See http://sourceforge.net/projects/pythonflu
//
//  Author : Alexey PETROV


//---------------------------------------------------------------------------
#ifndef LimitedScheme_vector_MUSCLLimiter_NVDTVD_limitFuncs_magSqr_cxx
#define LimitedScheme_vector_MUSCLLimiter_NVDTVD_limitFuncs_magSqr_cxx

//---------------------------------------------------------------------------
%module "Foam.src.finiteVolume.interpolation.surfaceInterpolation.limitedSchemes.LimitedScheme.LimitedScheme_vector_MUSCLLimiter_NVDTVD_limitFuncs_magSqr";
%{
    #include "src/finiteVolume/interpolation/surfaceInterpolation/limitedSchemes/LimitedScheme/LimitedScheme_vector_MUSCLLimiter_NVDTVD_limitFuncs_magSqr.hh"
%}


//---------------------------------------------------------------------------
%import "src/finiteVolume/interpolation/surfaceInterpolation/limitedSchemes/limitedSurfaceInterpolationScheme/limitedSurfaceInterpolationScheme_vector.cxx"

%import "src/finiteVolume/interpolation/surfaceInterpolation/limitedSchemes/MUSCL/MUSCL_NVDTVD.cxx"

%import "src/finiteVolume/interpolation/surfaceInterpolation/limitedSchemes/LimitedScheme/LimitFuncs.cxx"

%import "src/finiteVolume/interpolation/surfaceInterpolation/limitedSchemes/LimitedScheme/LimitedScheme.cxx"


//----------------------------------------------------------------------------
%ignore Foam::LimitedScheme< Foam::vector, Foam::MUSCLLimiter< Foam::NVDTVD>, Foam::limitFuncs::magSqr>::typeName;


%template ( LimitedScheme_vector_MUSCLLimiter_NVDTVD_limitFuncs_magSqr ) Foam::LimitedScheme< Foam::vector, Foam::MUSCLLimiter< Foam::NVDTVD>, Foam::limitFuncs::magSqr>;


//---------------------------------------------------------------------------
#endif

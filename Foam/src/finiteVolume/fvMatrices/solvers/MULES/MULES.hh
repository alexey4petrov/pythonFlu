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
#ifndef MULES_hh
#define MULES_hh


//---------------------------------------------------------------------------
#include "Foam/src/finiteVolume/fvMesh/fvMeshes.hh"

#include "Foam/src/OpenFOAM/fields/GeometricFields/geometricOneField.hh"

#include <MULES.H>

#if FOAM_REF_VERSION( >, 010600 ) || FOAM_BRANCH_VERSION( __OPENFOAM_EXT__, >, 010500 )
namespace Foam
{
  namespace MULES
  {
    void explicitSolve( const geometricOneField& rho,
                        volScalarField& psi,
                        const surfaceScalarField& phiBD,
                        surfaceScalarField& phiPsi,
                        const DimensionedField< scalar, volMesh >& Sp,
                        const DimensionedField< scalar, volMesh >& Su,
                        const scalar psiMax,
                        const scalar psiMin )
    {
      explicitSolve< >( rho, psi, phiBD, phiPsi, Sp, Su, psiMax, psiMin );
    }
  }
}
#endif

//----------------------------------------------------------------------------
#endif

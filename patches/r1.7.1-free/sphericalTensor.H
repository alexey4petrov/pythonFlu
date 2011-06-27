/*---------------------------------------------------------------------------*\
  =========                 |
  \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox
   \\    /   O peration     |
    \\  /    A nd           | Copyright (C) 1991-2010 OpenCFD Ltd.
     \\/     M anipulation  |
-------------------------------------------------------------------------------
License
    This file is part of OpenFOAM.

    OpenFOAM is free software: you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    OpenFOAM is distributed in the hope that it will be useful, but WITHOUT
    ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
    FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
    for more details.

    You should have received a copy of the GNU General Public License
    along with OpenFOAM.  If not, see <http://www.gnu.org/licenses/>.

Typedef
    Foam::sphericalTensor

Description
    SphericalTensor of scalars.

SourceFiles
    sphericalTensor.C

\*---------------------------------------------------------------------------*/

#ifndef sphericalTensor_H
#define sphericalTensor_H

#include <OpenFOAM/SphericalTensor_.H>
#include <OpenFOAM/contiguous.H>

// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

namespace Foam
{

// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

typedef SphericalTensor<scalar> sphericalTensor;
#ifndef SWIG
// Identity tensor
static const sphericalTensor I(1);

static const sphericalTensor oneThirdI(1.0/3.0);
static const sphericalTensor twoThirdsI(2.0/3.0);
#else
// Identity tensor
static const sphericalTensor I;

static const sphericalTensor oneThirdI;
static const sphericalTensor twoThirdsI;
#endif


//- Specify data associated with sphericalTensor type are contiguous
template<>
inline bool contiguous<sphericalTensor>() {return true;}


// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

} // End namespace Foam

// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

#endif

// ************************ vim: set sw=4 sts=4 et: ************************ //

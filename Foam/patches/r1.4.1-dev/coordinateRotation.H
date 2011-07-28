/*---------------------------------------------------------------------------*\
  =========                 |
  \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox
   \\    /   O peration     |
    \\  /    A nd           | Copyright (C) 1991-2007 OpenCFD Ltd.
     \\/     M anipulation  |
-------------------------------------------------------------------------------
License
    This file is part of OpenFOAM.

    OpenFOAM is free software; you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by the
    Free Software Foundation; either version 2 of the License, or (at your
    option) any later version.

    OpenFOAM is distributed in the hope that it will be useful, but WITHOUT
    ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
    FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
    for more details.

    You should have received a copy of the GNU General Public License
    along with OpenFOAM; if not, write to the Free Software Foundation,
    Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA

Class
    coordinateRotation

Description
    Base class for coordinate rotation.

    The rotation is defined by a combination of local vectors.
    The local vectors can be specified by an 'axis' (usually the z-axis)
    and a 'direction' (effectively the x-axis), or by another combination
    of local vectors (e1/e2), (e2/e3) or (e3/e1).
    Any nonorthogonality will absorbed into the second vector.

\*---------------------------------------------------------------------------*/

#ifndef coordinateRotation_H
#define coordinateRotation_H

#include "vector.H"
#include "tensor.H"
#include "runTimeSelectionTables.H"

// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

namespace Foam
{

class dictionary;

/*---------------------------------------------------------------------------*\
                    Class coordinateRotation Declaration
\*---------------------------------------------------------------------------*/

class coordinateRotation
:
    public tensor
{
    // Private data

        //- the combination of local axes to be used
        enum axisOrder {
            e1e2,
            e2e3,
            e3e1
        };

    // Private Member Functions

        //- Calculate transformation tensor
        void calcTransform
        (
            const vector& axis1,
            const vector& axis2,
            const axisOrder& order = e3e1
        );

public:

    //- Runtime type information
    TypeName("coordinateRotation");

    // Constructors

        //- Construct null
        coordinateRotation();

        //- Construct from 2 axes
        coordinateRotation
        (
            const vector& axis,
            const vector& dir
        );

        //- Construct from dictionary
        coordinateRotation(const dictionary&);


    // Declare run-time constructor selection table
#ifndef SWIG
        declareRunTimeSelectionTable
        (
            autoPtr,
            coordinateRotation,
            dictionary,
            (
                const dictionary& dict
            ),
            (dict)
        );

#endif
    // Selectors

        //- Select constructed from Istream
        static autoPtr<coordinateRotation> New
        (
            const dictionary& dict
        );


    // Destructor

        virtual ~coordinateRotation()
        {}


    // Member Functions

        //- Return local-to-global transformation tensor
        const tensor& R() const
        {
            return (*this);
        }

        //- Return local Cartesian x-axis
        vector& e1() const
        {
            return tensor::T().x();
        }

        //- Return local Cartesian y-axis
        vector& e2() const
        {
            return tensor::T().y();
        }

        //- Return local Cartesian z-axis
        vector& e3() const
        {
            return tensor::T().z();
        }


    // Member Operators

        //- assign from dictionary
        void operator=(const dictionary&);

};


// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

} // End namespace Foam

// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

#endif

// ************************************************************************* //

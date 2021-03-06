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
    coordinateSystem

Description
    Base class for coordinate systems.
    All systems are defined by an origin and a coordinate rotation.

SourceFiles
    coordinateSystem.C

\*---------------------------------------------------------------------------*/

#ifndef coordinateSystem_H
#define coordinateSystem_H

#include "vector.H"
#include "point.H"
#include "tensor.H"
#include "vectorField.H"
#include "pointField.H"
#include "tmp.H"
#include "coordinateRotation.H"
#include "objectRegistry.H"

// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

namespace Foam
{

/*---------------------------------------------------------------------------*\
                     Class coordinateSystem Declaration
\*---------------------------------------------------------------------------*/

class coordinateSystem
{
    // Private data

        //- Name of coordinate system
        mutable word name_;

        //- Origin
        mutable point origin_;

        //- Local-to-Global transformation tensor
        coordinateRotation R_;

        //- Global-to-Local transformation tensor
        tensor Rtr_;

protected:

    // Protected Member Functions

        //- Convert from local coordinate system to the global Cartesian system
        //  with optional translation for the origin
        virtual vector localToGlobal(const vector&, bool translate) const;

        //- Convert from local coordinate system to the global Cartesian system
        //  with optional translation for the origin
        virtual tmp<vectorField> localToGlobal
        (
            const vectorField&,
            bool translate
        ) const;

        //- Convert from global Cartesian system to the local coordinate system
        //  with optional translation for the origin
        virtual vector globalToLocal(const vector&, bool translate) const;

        //- Convert from global Cartesian system to the local coordinate system
        //  with optional translation for the origin
        virtual tmp<vectorField> globalToLocal
        (
            const vectorField&,
            bool translate
        ) const;

public:

    //- Runtime type information
    TypeName("coordinateSystem");


    // Constructors

        //- Construct null
        coordinateSystem();

        //- Construct from origin and 2 axes
        coordinateSystem
        (
            const word& name,
            const point& origin,
            const vector& axis,
            const vector& dir
        );

        //- Construct from origin and rotation angles
        coordinateSystem
        (
            const word& name,
            const point& origin,
            const coordinateRotation&
        );

        //- Construct from dictionary with default name
        coordinateSystem(const dictionary&);

        //- Construct from dictionary
        coordinateSystem(const word& name, const dictionary&);

        //- Construct from Istream
        coordinateSystem(Istream&);

        //- Return clone
        autoPtr<coordinateSystem> clone() const
        {
            return autoPtr<coordinateSystem>
            (
                new coordinateSystem
                (
                    name(),
                    origin(),
                    rotation()
                )
            );
        }
#ifndef SWIG
    // Declare run-time constructor selection table

        declareRunTimeSelectionTable
        (
            autoPtr,
            coordinateSystem,
            origAxisDir,
            (
                const word& name,
                const point& origin,
                const vector& axis,
                const vector& dir
            ),
            (name, origin, axis, dir)
        );

        declareRunTimeSelectionTable
        (
            autoPtr,
            coordinateSystem,
            origRotation,
            (
                const word& name,
                const point& origin,
                const coordinateRotation& cr
            ),
            (name, origin, cr)
        );

        declareRunTimeSelectionTable
        (
            autoPtr,
            coordinateSystem,
            dictionary,
            (
                const word& name,
                const dictionary& dict
            ),
            (name, dict)
        );

#endif
    // Selectors

        //- Select constructed from origin and 2 axes
        static autoPtr<coordinateSystem> New
        (
            const word& coordType,
            const word& name,
            const point& origin,
            const vector& axis,
            const vector& dir
        );

        //- Select constructed from origin and rotation
        static autoPtr<coordinateSystem> New
        (
            const word& coordType,
            const word& name,
            const point& origin,
            const coordinateRotation& cr
        );

        //- Select constructed from dictionary
        static autoPtr<coordinateSystem> New
        (
            const word& name,
            const dictionary& dict
        );

        //- Select constructed from Istream
        static autoPtr<coordinateSystem> New(Istream& is);

    // Destructor

        virtual ~coordinateSystem();


    // Member Functions

      // Access

        //- Return name
        const word& name() const
        {
            return name_;
        }

        //- Return origin
        const point& origin() const
        {
            return origin_;
        }

        //- Return coordinate rotation
        const coordinateRotation& rotation() const
        {
            return R_;
        }

        //- Return local-to-global transformation tensor
        const tensor& R() const
        {
            return R_;
        }

        //- Return local Cartesian x-axis
        const vector& e1() const
        {
           return Rtr_.x();
        }

        //- Return local Cartesian y-axis
        const vector& e2() const
        {
           return Rtr_.y();
        }

        //- Return local Cartesian z-axis
        const vector& e3() const
        {
           return Rtr_.z();
        }
   
        //- Return axis (e3: local Cartesian z-axis)
        const vector& axis() const
        {
           return Rtr_.z();
        }

        //- Return direction (e1: local Cartesian x-axis)
        const vector& direction() const
        {
            return Rtr_.x();
        }

        //- Return as dictionary of entries
        virtual dictionary dict(bool ignoreType = false) const;


      // Edit

        //- Rename
        virtual void rename(const word& newName)
        {
            name_ = newName;
        }

        //- Edit access to origin
        point& origin()
        {
            return origin_;
        }

      // Write

        //- Write
        virtual void write(Ostream&) const;

        //- Write dictionary
        virtual void writeDict(Ostream&, bool subDict = true) const;

      // Transformations

        //- Convert from position in local coordinate system to global Cartesian position
        point globalPosition(const point& local) const
        {
            return localToGlobal(local, true);
        }

        //- Convert from position in local coordinate system to global Cartesian position
        tmp<pointField> globalPosition(const pointField& local) const
        {
            return localToGlobal(local, true);
        }

        //- Convert from vector components in local coordinate system to global Cartesian vector
        vector globalVector(const vector& local) const
        {
            return localToGlobal(local, false);
        }

        //- Convert from vector components in local coordinate system to global Cartesian vector
        tmp<vectorField> globalVector(const vectorField& local) const
        {
            return localToGlobal(local, false);
        }

        //- Convert from global Cartesian position to position in local coordinate system
        point localPosition(const point& global) const
        {
            return globalToLocal(global, true);
        }

        //- Convert from global Cartesian position to position in local coordinate system
        tmp<pointField> localPosition(const pointField& global) const
        {
            return globalToLocal(global, true);
        }

        //- Convert from global Cartesian vector to components in local coordinate system
        vector localVector(const vector& global) const
        {
            return globalToLocal(global, false);
        }

        //- Convert from global Cartesian vector to components in local coordinate system
        tmp<vectorField> localVector(const vectorField& global) const
        {
            return globalToLocal(global, false);
        }


    // Member Operators

        //- assign from dictionary
        void operator=(const dictionary&);


    // friend Operators

        friend bool operator!=(const coordinateSystem&, const coordinateSystem&);

    // IOstream Operators

        friend Ostream& operator<<(Ostream&, const coordinateSystem&);
};


// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

} // End namespace Foam

// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

#endif

// ************************************************************************* //

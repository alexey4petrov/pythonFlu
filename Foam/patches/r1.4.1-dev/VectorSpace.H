/*---------------------------------------------------------------------------*\
  =========                 |
  \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox
   \\    /   O peration     |
    \\  /    A nd           | Copyright held by original author
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
    VectorSpace

Description
    Templated vector space.
    Template arguments are the Form the vector space will be used to create,
    the type of the elements and the number of elements.

SourceFiles
    VectorSpaceI.H
    VectorSpace.C

\*---------------------------------------------------------------------------*/

#ifndef VectorSpace_H
#define VectorSpace_H

#include "direction.H"
#include "scalar.H"
#include "word.H"

// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

namespace Foam
{

// * * * * * * Forward declaration of template friend fuctions * * * * * * * //

template<class Form, class Cmpt, int nCmpt> class VectorSpace;

template<class Form, class Cmpt, int nCmpt>
Istream& operator>>
(
    Istream&,
    VectorSpace<Form, Cmpt, nCmpt>&
);

template<class Form, class Cmpt, int nCmpt>
Ostream& operator<<
(
    Ostream&,
    const VectorSpace<Form, Cmpt, nCmpt>&
);


/*---------------------------------------------------------------------------*\
                           Class VectorSpace Declaration
\*---------------------------------------------------------------------------*/

template<class Form, class Cmpt, int nCmpt>
class VectorSpace
{

public:

    //- Component type
    typedef Cmpt cmptType;


    // Member constants

        enum
        {
            dim = 3,            // Dimensionality of space
            nComponents = nCmpt // Number of components in this vector space
        };


    // Static data members

        //- The components of this vector space
        Cmpt v_[nCmpt];


    // Constructors

        //- Construct null
        inline VectorSpace();

        //- Construct from Istream
        VectorSpace(Istream&);

        //- Construct as copy
        inline VectorSpace(const VectorSpace<Form, Cmpt, nCmpt>&);


    // Member Functions

        //- Return the number of elements in the FixedList.
        inline label size() const;

        inline const Cmpt& component(const direction) const;
        inline Cmpt& component(const direction);

        inline void component(Cmpt&, const direction) const;
        inline void replace(const direction, const Cmpt&);


    // Member Operators

        inline const Cmpt& operator[](const direction) const;
        inline Cmpt& operator[](const direction);

        inline void operator=(const VectorSpace<Form, Cmpt, nCmpt>&);
        inline void operator+=(const VectorSpace<Form, Cmpt, nCmpt>&);
        inline void operator-=(const VectorSpace<Form, Cmpt, nCmpt>&);

        inline void operator*=(const scalar);
        inline void operator/=(const scalar);


    // IOstream Operators
#ifndef SWIG
        friend Istream& operator>> <Form, Cmpt, nCmpt>
        (
            Istream&,
            VectorSpace<Form, Cmpt, nCmpt>&
        );

        friend Ostream& operator<< <Form, Cmpt, nCmpt>
        (
            Ostream&,
            const VectorSpace<Form, Cmpt, nCmpt>&
        );
#endif
};


// * * * * * * * * * * * * * * Global functions  * * * * * * * * * * * * * * //

//- Return a string representation of a VectorSpace
template<class Form, class Cmpt, int nCmpt>
word name(const VectorSpace<Form, Cmpt, nCmpt>&);

// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

} // End namespace Foam

// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

#include "VectorSpaceI.H"

#ifdef NoRepository
#   include "VectorSpace.C"
#endif

// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

#endif

// ************************************************************************* //

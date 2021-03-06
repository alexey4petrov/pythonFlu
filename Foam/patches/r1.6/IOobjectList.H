/*---------------------------------------------------------------------------*\
  =========                 |
  \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox
   \\    /   O peration     |
    \\  /    A nd           | Copyright (C) 1991-2009 OpenCFD Ltd.
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
    Foam::IOobjectList

Description
    List of IOobjects with searching and retrieving facilities.

SourceFiles
    IOobjectList.C

\*---------------------------------------------------------------------------*/

#ifndef IOobjectList_H
#define IOobjectList_H

#include "HashPtrTable.H"
#include "IOobject.H"

// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

namespace Foam
{

/*---------------------------------------------------------------------------*\
                           Class IOobjectList Declaration
\*---------------------------------------------------------------------------*/

class IOobjectList
:
#ifndef SWIG
    public HashPtrTable<IOobject>
#else
    public HashPtrTable<IOobject, word, string_hash>
#endif
{
    // Private Member Functions

        //- Disallow default bitwise assignment
        void operator=(const IOobjectList&);


public:

    // Constructors

        //- Construct given an initial estimate for the number of entries
        explicit IOobjectList(const label nIoObjects = 128);

        //- Construct from objectRegistry and instance path
        IOobjectList
        (
            const objectRegistry& db,
            const fileName& instance,
            const fileName& local = ""
        );

        //- Construct as copy
        IOobjectList(const IOobjectList&);


    // Destructor

        ~IOobjectList();


    // Member functions

        //- Add an IOobject to list
        bool add(IOobject&);

        //- Remove an IOobject from list
        bool remove(IOobject&);

        //- Lookup a given name and return IOobject ptr if found else NULL
        IOobject* lookup(const word& name) const;

        //- Return the list for all IOobjects of given class
        IOobjectList lookupClass(const word& className) const;

        //- Return the list of names of the IOobjects
        wordList names() const;

        //- Return the list of names of the IOobjects of given class
        wordList names(const word& className) const;
};


// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

} // End namespace Foam

// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

#endif

// ************************************************************************* //

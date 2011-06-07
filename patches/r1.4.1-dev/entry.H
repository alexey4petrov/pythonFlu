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
    entry

Description
    A keyword and a list of tokens is an 'entry'.
    An entry can be read, written and printed, and the types and values of its
    tokens analysed.  An entry is a high-level building block for data
    description.  It is a front-end for the token parser. A list of entries can
    be used as a set of keyword syntax elements, for example.

SourceFiles
    entry.C
    entryIO.C

\*---------------------------------------------------------------------------*/

#ifndef entry_H
#define entry_H

#include "IDLList.H"
#include "fileName.H"
#include "autoPtr.H"

// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

namespace Foam
{

class ITstream;
class dictionary;

/*---------------------------------------------------------------------------*\
                           Class entry Declaration
\*---------------------------------------------------------------------------*/

class entry
#ifndef SWIG
:
    public IDLList<entry>::link
#endif
{
    // Private data

        //- Keyword of entry
        word keyword_;


public:

    // Constructors

        //- Construct from keyword
        entry(const word& keyword);

        //- Construct as copy
        entry(const entry&);

        virtual autoPtr<entry> clone() const = 0;

        //- Construct on freestore from Istream
        static autoPtr<entry> New(Istream& is);


    // Destructor

        virtual ~entry()
        {}


    // Member functions

        //- Return keyword
        const word& keyword() const
        {
            return keyword_;
        }

        //- Return non-const access to keyword
        word& keyword()
        {
            return keyword_;
        }

        //- Return the dictionary name
        virtual const fileName& name() const = 0;

        //- Return the dictionary name
        virtual fileName& name() = 0;

        //- Return line number of first token in dictionary
        virtual label startLineNumber() const = 0;

        //- Return line number of last token in dictionary
        virtual label endLineNumber() const = 0;

        //- Return true if this entry is a stream
        virtual bool isStream() const
        {
            return false;
        }

        //- Return token stream if this entry is a primitive entry
        virtual ITstream& stream() const = 0;

        //- Return true if this entry is a dictionary
        virtual bool isDict() const
        {
            return false;
        }

        //- Return token stream if this entry is a primitive entry
        virtual const dictionary& dict() const = 0;

        //- Write
        virtual void write(Ostream&) const = 0;


    // Member operators

        void operator=(const entry&);

        bool operator==(const entry&) const;
        bool operator!=(const entry&) const;


    // Ostream operator

        friend Ostream& operator<<(Ostream&, const entry&);
};


// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

} // End namespace Foam

// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

#endif

// ************************************************************************* //

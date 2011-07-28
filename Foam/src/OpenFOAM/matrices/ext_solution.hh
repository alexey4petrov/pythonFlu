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
#ifndef ext_solution_hh
#define ext_solution_hh


//---------------------------------------------------------------------------
#include "Foam/src/OpenFOAM/db/IOdictionary.hh"


//---------------------------------------------------------------------------
namespace Foam
{
/*---------------------------------------------------------------------------*\
                           Class solution Declaration
          Selector class for relaxation factors, solver type and solution.
\*---------------------------------------------------------------------------*/

class ext_solution
:
    public IOdictionary
{
    // Private data

        dictionary relaxationFactors_;
        dictionary solvers_;


    // Private Member Functions

        //- Disallow default bitwise copy construct and assignment
        ext_solution(const ext_solution&);
        void operator=(const ext_solution&);


public:

    //- Debug switch
    static int debug;


    // Constructors

        //- Construct given objectRegistry and dictionary name
        ext_solution(const objectRegistry& obr, const fileName& dictName);


        //- Construct given objectRegistry and dictionary name
        ext_solution(const objectRegistry& obr, const fileName& dictName, const dictionary& dict);


    // Member Functions

        // Access

            //- Return constant reference to solution dictionary
            const dictionary& solutionDict() const;

            bool relax(const word& name) const;
            scalar relaxationFactor(const word& name) const;

            ITstream& solver(const word& name) const;

            //- Add a solver primitive entry to the solvers subdict
            bool addSolver(const word& fieldName, const word& solverName, const dictionary& dict);

            //- Add a relaxation factor entry to the relaxationFactors subdict
            bool addRelaxationFactor(const word& fieldName, scalar alpha);


        // Read

            //- Read the solution
            bool read();
};

} // End namespace Foam


//---------------------------------------------------------------------------

#include "Time.H"

// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

namespace Foam
{

#ifndef SWIG
int ext_solution::debug( Foam::debug::debugSwitch( "solution", false ) );
#endif

// * * * * * * * * * * * * * * * * Constructors  * * * * * * * * * * * * * * //

ext_solution::ext_solution(const objectRegistry& obr, const fileName& dictName)
:
    IOdictionary
    (
        IOobject
        (
            dictName,
            obr.time().system(),
            obr,
            IOobject::MUST_READ,
            IOobject::NO_WRITE
        )
    ),
    relaxationFactors_(ITstream("relaxationFactors", tokenList())()),
    solvers_(ITstream("solvers", tokenList())())
{
    read();
}


ext_solution::ext_solution(const objectRegistry& obr, const fileName& dictName, const dictionary& dict)
:
    IOdictionary
    (
        IOobject
        (
            dictName,
            obr.time().system(),
            obr,
            IOobject::NO_READ,
            IOobject::NO_WRITE
        ),
        dict
    ),
    relaxationFactors_(ITstream("relaxationFactors", tokenList())()),
    solvers_(ITstream("solvers", tokenList())())
{
    read();
}


// * * * * * * * * * * * * * * * Member Functions  * * * * * * * * * * * * * //

bool ext_solution::read()
{
    if
    (
        readOpt() == IOobject::MUST_READ
     || (readOpt() == IOobject::READ_IF_PRESENT && headerOk())
    )
    {
        if (!regIOobject::read())
        {
            return false;
        }
    }

    const dictionary& dict = solutionDict();

    if (dict.found("relaxationFactors"))
    {
        relaxationFactors_ = dict.subDict("relaxationFactors");
    }

    if (dict.found("solvers"))
    {
        solvers_ = dict.subDict("solvers");
    }

    return true;
}


const dictionary& ext_solution::solutionDict() const
{
    if (found("select"))
    {
        return subDict(word(lookup("select")));
    }
    else
    {
        return *this;
    }
}


bool ext_solution::relax(const word& name) const
{
    if (debug)
    {
        Info<< "Lookup relax for " << name << endl;
    }

    return relaxationFactors_.found(name);
}

scalar ext_solution::relaxationFactor(const word& name) const
{
    if (debug)
    {
        Info<< "Lookup relaxationFactor for " << name << endl;
    }

    return readScalar(relaxationFactors_.lookup(name));
}

ITstream& ext_solution::solver(const word& name) const
{
    if (debug)
    {
        Info<< "Lookup solver for " << name << endl;
    }

    return solvers_.lookup(name);
}


//- Add a solver primitive entry to the solvers subdict
bool ext_solution::addSolver(const word& fieldName, const word& solverName, const dictionary& dict)
{
    OStringStream os;
    os << solverName << dict << token::END_STATEMENT;

    primitiveEntry solverEntry 
    (
        fieldName,
        IStringStream(os.str())()
    );

    solvers_.add(solverEntry);

    //- Reapply the updated subdictionary
    if (found("select"))
    {
        word dictName(lookup("select"));

        dictionary dict(subDict(dictName));
        if (dict.found("solvers")) dict.remove("solvers");
        dict.add("solvers", solvers_);

        remove(dictName);
        add(dictName, dict);
    }
    else
    {
        if (found("solvers")) remove("solvers");
        add("solvers", solvers_);
    }

    return true;
}


//- Add a relaxation factor entry to the relaxationFactors subdict
bool ext_solution::addRelaxationFactor(const word& fieldName, scalar alpha)
{
    relaxationFactors_.add(fieldName, alpha);

    //- Reapply the updated subdictionary
    if (found("select"))
    {
        word dictName(lookup("select"));

        dictionary dict(subDict(dictName));
        if (dict.found("relaxationFactors")) dict.remove("relaxationFactors");
        dict.add("relaxationFactors", relaxationFactors_);

        remove(dictName);
        add(dictName, dict);
    }
    else
    {
        if (found("relaxationFactors")) remove("relaxationFactors");
        add("relaxationFactors", relaxationFactors_);
    }

    return true;
}

// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

} // End namespace Foam



//---------------------------------------------------------------------------
#endif

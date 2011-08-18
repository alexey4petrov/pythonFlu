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

Class
    Foam::Pstream

Description
    Inter-processor communications stream

SourceFiles
    Pstream.C
    PstreamsPrint.C
    PstreamCommsStruct.C
    gatherScatter.C
    combineGatherScatter.C
    gatherScatterList.C

\*---------------------------------------------------------------------------*/

#ifndef Pstream_H
#define Pstream_H

#include "PstreamImpl.H"
#include <OpenFOAM/labelList.H>
#include <OpenFOAM/DynamicList.H>
#include <OpenFOAM/HashTable.H>
#include <OpenFOAM/string.H>
#include <OpenFOAM/NamedEnum.H>

// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

namespace Foam
{

/*---------------------------------------------------------------------------*\
                           Class Pstream Declaration
\*---------------------------------------------------------------------------*/

class Pstream
#ifndef SWIG
: public helper_::PstreamBase
#endif
{

public:
#ifndef SWIG
    //- Types of communications
    using helper_::PstreamBase::commsTypes;

    static const NamedEnum<commsTypes, 3> commsTypeNames;
#endif

    //- Structure for communicating between processors
    class commsStruct
    {
        // Private data

            //- procID of above processor
            label above_;

            //- procIDs of processors directly below me
            labelList below_;

            //- procIDs of all processors below (so not just directly below)
            labelList allBelow_;

            //- procIDs of all processors not below. (inverse set of allBelow_
            //  and minus myProcNo)
            labelList allNotBelow_;


    public:

        // Constructors

            //- Construct null
            commsStruct();

            //- Construct from components
            commsStruct
            (
                const label,
                const labelList&,
                const labelList&,
                const labelList&
            );

            //- Construct from components; construct allNotBelow_
            commsStruct
            (
                const label nProcs,
                const label myProcID,
                const label,
                const labelList&,
                const labelList&
            );


        // Member Functions

            // Access

                label above() const
                {
                    return above_;
                }

                const labelList& below() const
                {
                    return below_;
                }

                const labelList& allBelow() const
                {
                    return allBelow_;
                }

                const labelList& allNotBelow() const
                {
                    return allNotBelow_;
                }


        // Member operators

            bool operator==(const commsStruct&) const;

            bool operator!=(const commsStruct&) const;


         // Ostream Operator

            friend Ostream& operator<<(Ostream&, const commsStruct&);
    };


private:

    // Private data

        static int myProcNo_;
        static bool parRun_;

        static List<int> procIDs_;
        static const int msgType_;

        static List<commsStruct> linearCommunication_;
        static List<commsStruct> treeCommunication_;

        static autoPtr<PstreamImpl> impl_;


    // Private member functions

        //- Calculate linear communication schedule
        static void calcLinearComm(const label nProcs);

        //- Calculate tree communication schedule
        static void calcTreeComm(const label nProcs);

        //- Helper function for tree communication schedule determination
        //  Collects all processorIDs below a processor
        static void collectReceives
        (
            const label procID,
            const List<DynamicList<label> >& receives,
            DynamicList<label>& allReceives
        );

        //- Initialize all communication schedules. Callback from
        //  PstreamImpl::init()
        static void initCommunicationSchedule();

        //- Fetches the PstreamImpl instance if necessary
        static autoPtr<PstreamImpl>& impl()
        {
            if(!impl_.valid())
            {
                impl_ = PstreamImpl::New();
            }
            return impl_;
        }


protected:

    // Protected data
#ifndef SWIG
        //- Communications type of this stream
        commsTypes commsType_;
#endif
        //- Transfer buffer
        List<char> buf_;

        //- Current buffer read/write location
        int bufPosition_;


    // Protected member functions

        //- Increase the size of the transfer buffer
        inline void enlargeBuffer(size_t count);


public:

    // Declare name of the class and its debug switch
    ClassName("Pstream");


    // Static data

        //- Should compact transfer be used in which floats replace doubles
        //  reducing the bandwidth requirement at the expense of some loss
        //  in accuracy
        static bool floatTransfer;

        //- Number of processors at which the sum algorithm changes from linear
        //  to tree
        static int nProcsSimpleSum;
#ifndef SWIG
        //- Default commsType
        static commsTypes defaultCommsType;
#endif

    // Constructors
#ifndef SWIG
        //- Construct given optional buffer size
        Pstream
        (
            const commsTypes commsType,
            const label bufSize = 0
        )
        :
            commsType_(commsType),
            bufPosition_(0)
        {
            if (bufSize)
            {
                buf_.setSize(bufSize + 2*sizeof(scalar) + 1);
            }
        }
#endif

    // Member functions

        //- Add the valid option this type of communications library
        //  adds/requires on the command line
        static void addValidParOptions(HashTable<string>& validParOptions)
        {
            impl()->addValidParOptions(validParOptions);
        }

        //- Initialisation function called from main
        //  Spawns slave processes and initialises inter-communication
        static bool init(int& argc, char**& argv)
        {
            return impl()->init(argc, argv, myProcNo_, procIDs_, parRun_);
        }

        //- Is this a parallel run?
        static bool parRun()
        {
            return parRun_;
        }

        //- Number of processes in parallel run
        static label nProcs()
        {
            return procIDs_.size();
        }

        //- Am I the master process
        static bool master()
        {
            return myProcNo_ == 0;
        }

        //- Process index of the master
        static int masterNo()
        {
            return 0;
        }

        //- Number of this process (starting from masterNo() = 0)
        static int myProcNo()
        {
            return myProcNo_;
        }

        //- Process IDs
        static const List<int>& procIDs()
        {
            return procIDs_;
        }

        //- Process ID of given process index
        static int procID(int procNo)
        {
            return procIDs_[procNo];
        }

        //- Process index of first slave
        static int firstSlave()
        {
            return 1;
        }

        //- Process index of last slave
        static int lastSlave()
        {
            return nProcs() - 1;
        }

        //- Communication schedule for linear all-to-master (proc 0)
        static const List<commsStruct>& linearCommunication()
        {
            return linearCommunication_;
        }

        //- Communication schedule for tree all-to-master (proc 0)
        static const List<commsStruct>& treeCommunication()
        {
            return treeCommunication_;
        }

        //- Message tag of standard messages
        static int msgType()
        {
            return msgType_;
        }
#ifndef SWIG
            //- Get the communications type of the stream
            commsTypes commsType() const
            {
                return commsType_;
            }

            //- Set the communications type of the stream
            commsTypes commsType(const commsTypes ct)
            {
                commsTypes oldCommsType = commsType_;
                commsType_ = ct;
                return oldCommsType;
            }
#endif
        //- Exit program
        static void exit(int errnum = 1)
        {
            impl()->exit(errnum);
        }

        //- Abort program
        static void abort()
        {
            impl()->abort();
        }


        // Gather and scatter

            //- Gather data. Apply bop to combine Value
            //  from different processors
            template <class T, class BinaryOp>
            static void gather
            (
                const List<commsStruct>& comms,
                T& Value,
                const BinaryOp& bop
            );

            //- Like above but switches between linear/tree communication
            template <class T, class BinaryOp>
            static void gather(T& Value, const BinaryOp& bop);

            //- Scatter data. Distribute without modification. Reverse of gather
            template <class T>
            static void scatter(const List<commsStruct>& comms, T& Value);

            //- Like above but switches between linear/tree communication
            template <class T>
            static void scatter(T& Value);


        // Combine variants. Inplace combine values from processors.
        // (Uses construct from Istream instead of <<)

            template <class T, class CombineOp>
            static void combineGather
            (
                const List<commsStruct>& comms,
                T& Value,
                const CombineOp& cop
            );

            //- Like above but switches between linear/tree communication
            template <class T, class CombineOp>
            static void combineGather(T& Value, const CombineOp& cop);

            //- Scatter data. Reverse of combineGather
            template <class T>
            static void combineScatter
            (
                const List<commsStruct>& comms,
                T& Value
            );

            //- Like above but switches between linear/tree communication
            template <class T>
            static void combineScatter(T& Value);

        // Combine variants working on whole List at a time.

            template <class T, class CombineOp>
            static void listCombineGather
            (
                const List<commsStruct>& comms,
                List<T>& Value,
                const CombineOp& cop
            );

            //- Like above but switches between linear/tree communication
            template <class T, class CombineOp>
            static void listCombineGather(List<T>& Value, const CombineOp& cop);

            //- Scatter data. Reverse of combineGather
            template <class T>
            static void listCombineScatter
            (
                const List<commsStruct>& comms,
                List<T>& Value
            );

            //- Like above but switches between linear/tree communication
            template <class T>
            static void listCombineScatter(List<T>& Value);

        // Combine variants working on whole map at a time. Container needs to
        // have iterators and find() defined.

            template <class Container, class CombineOp>
            static void mapCombineGather
            (
                const List<commsStruct>& comms,
                Container& Values,
                const CombineOp& cop
            );

            //- Like above but switches between linear/tree communication
            template <class Container, class CombineOp>
            static void mapCombineGather
            (
                Container& Values,
                const CombineOp& cop
            );

            //- Scatter data. Reverse of combineGather
            template <class Container>
            static void mapCombineScatter
            (
                const List<commsStruct>& comms,
                Container& Values
            );

            //- Like above but switches between linear/tree communication
            template <class Container>
            static void mapCombineScatter(Container& Values);



        // Gather/scatter keeping the individual processor data separate.
        // Values is a List of size Pstream::nProcs() where
        // Values[Pstream::myProcNo()] is the data for the current processor.

            //- Gather data but keep individual values separate
            template <class T>
            static void gatherList
            (
                const List<commsStruct>& comms,
                List<T>& Values
            );

            //- Like above but switches between linear/tree communication
            template <class T>
            static void gatherList(List<T>& Values);

            //- Scatter data. Reverse of gatherList
            template <class T>
            static void scatterList
            (
                const List<commsStruct>& comms,
                List<T>& Values
            );

            //- Like above but switches between linear/tree communication
            template <class T>
            static void scatterList(List<T>& Values);

    // Friends

        friend void ::Foam::reduce(scalar& Value, const sumOp<scalar>& bop);
        friend void ::Foam::PstreamImpl::initCommunicationSchedule();

};


inline void Pstream::enlargeBuffer(size_t count)
{
    buf_.setSize(max(int(buf_.size() + count), 2*buf_.size()));
}


Ostream& operator<<(Ostream&, const Pstream::commsStruct&);


// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

} // End namespace Foam

// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

#ifdef NoRepository
#   include <OpenFOAM/gatherScatter.C>
#   include <OpenFOAM/combineGatherScatter.C>
#   include <OpenFOAM/gatherScatterList.C>
#endif


// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

#endif

// ************************ vim: set sw=4 sts=4 et: ************************ //

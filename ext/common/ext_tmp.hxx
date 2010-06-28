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
//  See https://vulashaka.svn.sourceforge.net/svnroot/vulashaka
//
//  Author : Alexey PETROV


//---------------------------------------------------------------------------
#ifndef ext_tmp_H
#define ext_tmp_H


//---------------------------------------------------------------------------
%include "src/OpenFOAM/fields/tmp/tmp.cxx"
%include "src/OpenFOAM/fields/tmp/autoPtr.cxx"


//---------------------------------------------------------------------------
%inline
{
 namespace Foam
 {
    //---------------------------------------------------------------------------
    template< class T >
    struct ext_tmp
    {
        autoPtr< tmp< T > > engine;

        explicit ext_tmp( T* tPtr = 0 )
            : engine( new tmp< T >( tPtr ) )
        {}

        ext_tmp( const T& tRef )
            : engine( new tmp< T >( tRef ) )
        {}

        ext_tmp( const tmp< T >& t )
            : engine( new tmp< T >( t ) )
        {}

        ext_tmp( const ext_tmp< T >& at )
            : engine( new tmp< T >( at.engine ) )
        {}

        void operator=( T* tPtr )
        {
            this->engine.reset( new tmp< T >( tPtr ) );
        }

        void operator=( const T& tRef )
        {
            this->engine.reset( new tmp< T >( tRef ) );
        }

        void operator=( const tmp< T >& t )
        {
            this->engine.reset( new tmp< T >( t ) );
        }

        void operator=( const ext_tmp< T >& at )
        {
            this->engine.reset( new tmp< T >( at.engine ) );
        }

        T* operator->()
        {
            return this->engine->operator -> ();
        }

        const T* operator->() const
        {
            return this->engine->operator -> ();
        }

        T& operator()()
        {
            return this->engine->operator () ();
        }
   };


    //---------------------------------------------------------------------------
 }
}

//---------------------------------------------------------------------------
#endif


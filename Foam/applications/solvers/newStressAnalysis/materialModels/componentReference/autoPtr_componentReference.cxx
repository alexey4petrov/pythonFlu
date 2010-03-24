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
//  See https://vulashaka.svn.sourceforge.net/svnroot/vulashaka/pyfoam
//
//  Author : Alexey PETROV


//---------------------------------------------------------------------------
#if ( __FOAM_VERSION__ > 010401 )
%include "src/common.hxx"
#define autoPtr_componentReference_cxx
#endif


//---------------------------------------------------------------------------
#ifndef autoPtr_componentReference_cxx
#define autoPtr_componentReference_cxx


//---------------------------------------------------------------------------
%include "src/OpenFOAM/fields/tmp/autoPtr.cxx"

%include "Foam/applications/solvers/newStressAnalysis/materialModels/componentReference/componentReference_.cxx"

%template( autoPtr_componentReference ) Foam::autoPtr< Foam::componentReference >;

%inline
{
    namespace Foam
    {
        typedef autoPtr< componentReference > autoPtr_componentReference;
    }
}


//---------------------------------------------------------------------------
#endif

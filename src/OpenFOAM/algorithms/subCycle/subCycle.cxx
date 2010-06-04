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
#ifndef subCycle_cxx
#define subCycle_cxx


//---------------------------------------------------------------------------
%include "src/OpenFOAM/db/Time/subCycleTime.cxx"

%{
    #include "subCycle.H"
%}

%include "subCycle.H"


//---------------------------------------------------------------------------
// To support native Python of iteration over subCycle
%inline
%{
  namespace Foam
  {
    template< class TsubCycle >
    struct subCycleIterator
    {
     subCycleIterator( TsubCycle& the_subCycle )
        : m_subCycle( the_subCycle )
      {}

      subCycleTime& __iter__()
      {
        return this->m_subCycle++;
      }

      subCycleTime& next() throw( const TStopIterationException& )
      {
        if ( !this->m_subCycle.end() )
          return this->__iter__();
        
        throw TStopIterationException();
      }

    private :
      TsubCycle& m_subCycle;
    }; 
  }
%}


//---------------------------------------------------------------------------
%define SUBCYCLE_SEQUENCE_ADDONS( TItem )
{
  Foam::subCycleIterator< Foam::subCycle< TItem > >* __iter__()
  {
    return new Foam::subCycleIterator< Foam::subCycle< TItem > >( *self );
  }
}
%enddef


//----------------------------------------------------------------------------
%define SUBCYCLE_ADDONS( TItem )

%extend Foam::subCycle< TItem > SUBCYCLE_SEQUENCE_ADDONS( TItem )

%enddef


//----------------------------------------------------------------------------
#endif

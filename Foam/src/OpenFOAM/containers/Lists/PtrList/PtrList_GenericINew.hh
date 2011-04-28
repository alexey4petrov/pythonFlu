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
#ifndef PtrList_GenericINew_hh
#define PtrList_GenericINew_hh


//---------------------------------------------------------------------------
#include "src/director.hh"

#include "src/OpenFOAM/containers/Lists/PtrList/PtrList_GenericType.hh"

#include "src/OpenFOAM/fields/tmp/autoPtr.hh"


//---------------------------------------------------------------------------
namespace Foam
{
  struct PtrList_INewBase
  {
    PtrList_INewBase() {}
    virtual autoPtr< PtrList_TypeHolder > operator()( Istream & is ) const  = 0;
    virtual ~PtrList_INewBase(){}
  };

  struct PtrList_INewHolder: PtrList_INewBase
  {
    PtrList_INewHolder( PtrList_INewBase* the_PtrList_INewBase ): m_engine( the_PtrList_INewBase ){};
    PtrList_INewHolder(){};
    virtual autoPtr< PtrList_TypeHolder > operator()( Istream& is ) const
    {
      return this->m_engine->operator()( is );
    };
    PtrList_INewBase* operator->() 
    {
      return this->m_engine;
    }
  private :
    PtrList_INewBase* m_engine;
  }; 
}


//---------------------------------------------------------------------------
#endif

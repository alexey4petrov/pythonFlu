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
#ifndef PtrList_GenericType_hh
#define PtrList_GenericType_hh


//---------------------------------------------------------------------------
#include "Foam/src/director.hh"

#include "Foam/src/OpenFOAM/fields/tmp/autoPtr.hh"

#include <Istream.H>
#include <refCount.H>
#include <direction.H>
#include <scalar.H>

namespace Foam
{
  struct PtrList_TypeHolder;
  struct PtrList_TypeBase    
  {
    PtrList_TypeBase() {}
    virtual autoPtr< PtrList_TypeHolder >  clone() = 0;
    virtual ~PtrList_TypeBase() {}
  };

  struct PtrList_TypeHolder : PtrList_TypeBase
  {
    PtrList_TypeHolder( PtrList_TypeBase* the_PtrList_TypeBase ): m_engine( the_PtrList_TypeBase )
    {};
    PtrList_TypeHolder(){}
    
    virtual autoPtr< PtrList_TypeHolder > clone()
    {
      return this->m_engine->clone() ;
    }       
    PtrList_TypeBase* operator->() 
    {
      return this->m_engine;
    }
    PtrList_TypeBase* base() 
    {
      return this->m_engine;
    }
  private :
    PtrList_TypeBase* m_engine;
  };
}


//---------------------------------------------------------------------------
#endif

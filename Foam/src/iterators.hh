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
#ifndef iterators_hh
#define iterators_hh


//---------------------------------------------------------------------------
#include "Foam/src/common.hh"

// To support native Python of iteration over containers
namespace Foam
{
  struct TStopIterationException
  {};

  template< class TContainer >
  struct TContainer_iterator
  {
    typedef typename TContainer::reference TReturnType;
    
    TContainer_iterator( TContainer& the_Container )
      : m_container( the_Container )
      , m_iter( the_Container.begin() )
    {}
    
    TReturnType __iter__()
    {
      return *(this->m_iter++);
    }
    
    TReturnType next() throw( const TStopIterationException& )
    {
      if ( this->m_iter != m_container.end() )
        return this->__iter__();
      
      throw TStopIterationException();
    }
    
  private :
    TContainer& m_container;
    typename TContainer::iterator m_iter;
  };
  
  
  template< class TPtrContainer >
  struct TPtrContainer_iterator
  {
    typedef typename TPtrContainer::value_type TReturnType;
    
    TPtrContainer_iterator( TPtrContainer& the_Container )
      : m_container( the_Container )
      , m_iter( the_Container.begin() )
    {}
    
    TReturnType __iter__()
    {
      return *(this->m_iter++);
    }
    
    TReturnType next() throw( const TStopIterationException& )
    {
      if ( this->m_iter != m_container.end() )
        return this->__iter__();
      
      throw TStopIterationException();
    }
    
  private :
    TPtrContainer& m_container;
    typename TPtrContainer::iterator m_iter;
  };
}


//---------------------------------------------------------------------------
#endif

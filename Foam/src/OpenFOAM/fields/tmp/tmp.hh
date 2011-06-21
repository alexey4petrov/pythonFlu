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
#ifndef tmp_hh
#define tmp_hh


//---------------------------------------------------------------------------
#include "Foam/src/OpenFOAM/fields/tmp/refCount.hh"

#include "Foam/ext/common/ext_tmp.hh"

#include <tmp.H>


//---------------------------------------------------------------------------
namespace Foam
{
  template< class T >
  T& get_ref( T* theArg )
  {
    return *theArg;
  }

  template< class T >
  T& get_ref( tmp< T >* theArg )
  {
    return (*theArg)();
  }

  template< class T >
  const T& get_ref( const tmp< T >* theArg )
  {
    return *theArg;
  }
  
  template< class T >
  T& get_ref( ext_tmp< T >* theArg )
  {
    return (*theArg)();
  }
  template< class T >
  const T& get_ref( const ext_tmp< T >* theArg )
  {
    return (*theArg)();
  }

}


//---------------------------------------------------------------------------
#endif

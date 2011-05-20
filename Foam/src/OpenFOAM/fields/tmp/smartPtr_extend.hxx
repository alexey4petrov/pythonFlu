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
#ifndef smartPtr_extend_hxx
#define smartPtr_extend_hxx


//---------------------------------------------------------------------------
//For using tmp<T> & autoPtr<T> as T
%define SMARTPTR_PYAPPEND_GETATTR( Type ) __getattr__
%{
    name = args[ 0 ]
    try:
        return _swig_getattr( self, Type, name )
    except AttributeError:
        if self.valid() :
            attr = None
            exec "attr = self.__call__().%s" % name
            return attr
        pass
    raise AttributeError()
%}
%enddef


//---------------------------------------------------------------------------
%define SMARTPTR_EXTEND_ATTR( Type )
    void __getattr__( const char* name ){} // dummy function
%enddef


//---------------------------------------------------------------------------
%define SMARTPTR_EXTEND_OPERATOR_EQ( UList_Type )
  bool operator==( const Foam::UList< UList_Type >& theArg )
  {
    const Foam::UList< UList_Type > * aSelf = static_cast< const Foam::UList< UList_Type > * >( self->ptr() );
    return *aSelf == theArg;
  }
%enddef


//---------------------------------------------------------------------------
#endif

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
#ifndef redirect2base_hxx
#define redirect2base_hxx


//---------------------------------------------------------------------------
// This trick allows to access to the base class's 
// ( member's of the nested class or if inheritance not correctly wrapped )
// the class(the struct which redirect call to the nested class) 
// should be extended by base() function( return baseClass& )
%define REDIRECT2BASE_PYAPPEND_GETATTR( Type ) __getattr__
%{
    name = args[ 0 ]
    try:
        return _swig_getattr( self, Type, name )
    except AttributeError:
        attr = None
        exec "attr = self.base().%s" % name
        return attr
    raise AttributeError()
%}
%enddef


//---------------------------------------------------------------------------
%define REDIRECT2BASE_EXTEND_ATTR( Type )
    void __getattr__( const char* name ){} // dummy function
%enddef


//---------------------------------------------------------------------------






#endif


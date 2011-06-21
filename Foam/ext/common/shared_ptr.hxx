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
#ifndef shared_ptr_hxx
#define shared_ptr_hxx


//---------------------------------------------------------------------------
%include "Foam/src/common.hxx"

%{
    #include "boost/shared_ptr.hpp"
%}

namespace boost
{
    template <class T> struct shared_ptr 
    {
        shared_ptr( shared_ptr const & r );

        T * operator-> () const;

        T * get() const;

        bool unique() const;

        long use_count() const;

        %extend
        {
            T& operator() () const
            {
                return *self->get();
            }

            bool __nonzero__() const
            {
                return self->get() != 0;
            }
        }
    };
}


//---------------------------------------------------------------------------
%define SHAREDPTR_TYPEMAP( TYPE )

%feature("novaluewrapper") boost::shared_ptr< TYPE >;

%typemap(in) const boost::shared_ptr< TYPE > & ( void  *argp = 0, int res = 0, boost::shared_ptr< TYPE > tempshared ) {
    res = SWIG_ConvertPtr( $input, &argp, $descriptor( boost::shared_ptr< TYPE > * ), %convertptr_flags );
    if ( SWIG_IsOK( res ) && argp ) {
        tempshared = *%reinterpret_cast( argp, boost::shared_ptr< TYPE > * );
    } else {
        res = SWIG_ConvertPtr( $input, &argp, $descriptor( TYPE * ), SWIG_POINTER_DISOWN | %convertptr_flags );
        if ( SWIG_IsOK( res ) && argp ) {
            tempshared.reset( %reinterpret_cast( argp, TYPE * ) );
        } else {
            %argument_fail( res, "$type", $symname, $argnum ); 
        }
    }
    $1 = &tempshared;
}

%enddef


//---------------------------------------------------------------------------
#endif

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
#ifndef direction_cxx
#define direction_cxx


//---------------------------------------------------------------------------
%include "src/common.hxx"

%include "direction.H"

%{
    #include "direction.H"
%}


//---------------------------------------------------------------------------
%typecheck( SWIG_TYPECHECK_POINTER ) const Foam::direction &
{
    void *ptr;
    if ( SWIG_ConvertPtr( $input, (void **) &ptr, $1_descriptor, 0 ) == -1 ) {
        $1 = PyInt_Check( $input );
    } else {
        $1 = true;
    }
}


%typemap( in ) const Foam::direction &
{
    void *ptr;
    if ( SWIG_ConvertPtr( $input, (void **) &ptr, $1_descriptor, 0 ) == -1 ) {
        Foam::scalar aValue = PyInt_AsLong( $input );
        $1 = new $1_basetype( aValue );
    } else {
        $1 = reinterpret_cast< $1_ltype >( ptr );
    }
}


%typemap( out ) Foam::direction 
{
    $result = PyInt_FromLong( *&$1 );
}


//---------------------------------------------------------------------------
#endif

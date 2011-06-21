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
#ifndef shared_ptr_dimensionedScalar_cxx
#define shared_ptr_dimensionedScalar_cxx


//---------------------------------------------------------------------------
%include "Foam/ext/common/shared_ptr.hxx"

%include "Foam/src/OpenFOAM/dimensionedTypes/dimensionedScalar.cxx"

SHAREDPTR_TYPEMAP( Foam::dimensionedScalar );

//%ignore boost::shared_ptr< Foam::dimensionedScalar >::operator->;

%template( shared_ptr_dimensionedScalar ) boost::shared_ptr< Foam::dimensionedScalar >;


//---------------------------------------------------------------------------
#endif

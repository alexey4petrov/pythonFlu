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
//  Author : Alexey PETROV, Andrey SIMURZIN


//---------------------------------------------------------------------------
#ifndef uniformDimensionedVectorFieldHolder_cpp
#define uniformDimensionedVectorFieldHolder_cpp


//---------------------------------------------------------------------------
%{
  #include "Foam/ext/common/OpenFOAM/managedFlu/uniformDimensionedVectorFieldHolder.hh"
%}


//---------------------------------------------------------------------------
%include "Foam/ext/common/OpenFOAM/shared_ptr/shared_ptr_uniformDimensionedVectorField.hpp"

%include "Foam/ext/common/OpenFOAM/managedFlu/UniformDimensionedFieldHolder.hxx"

%include <uniformDimensionedFieldHolders.hpp>

%template ( uniformDimensionedVectorFieldHolder ) Foam::UniformDimensionedFieldHolder< Foam::vector >;


//---------------------------------------------------------------------------
%feature( "pythonappend" ) Foam::UniformDimensionedFieldHolder< Foam::vector >::SMARTPTR_PYAPPEND_GETATTR( uniformDimensionedVectorFieldHolder );

%extend Foam::FieldHolder< Foam::vector >
{
  SMARTPTR_EXTEND_ATTR( uniformDimensionedVectorFieldHolder );
}


//---------------------------------------------------------------------------
%import "Foam/src/try_reverse_operator.hxx"

%feature ("pythonprepend") Foam::UniformDimensionedFieldHolder< Foam::vector >::TRY_REVERSE_PYPREPEND( and );

%extend Foam::UniformDimensionedFieldHolder< Foam::vector >
{
  TRY_REVERSE_EXTEND( and );
}

%extend Foam::UniformDimensionedField< Foam::vector > FUNCTION_HOLDER_EXTEND_SHARED_PTR_TEMPLATE1( Foam::UniformDimensionedField, Foam::vector );


//--------------------------------------------------------------------------------------
#endif

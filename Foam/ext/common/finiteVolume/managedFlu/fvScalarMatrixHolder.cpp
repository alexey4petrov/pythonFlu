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
#ifndef fvScalarMatrixHolder_cpp
#define fvScalarMatrixHolder_cpp


//---------------------------------------------------------------------------
%{
  #include "Foam/ext/common/finiteVolume/managedFlu/fvScalarMatrixHolder.hh"
%}


//---------------------------------------------------------------------------
%include "Foam/ext/common/finiteVolume/smart_tmp/smart_tmp_fvScalarMatrix.cpp"

%include "Foam/ext/common/finiteVolume/managedFlu/fvMatrixHolder.hxx"

%template (fvScalarMatrixHolder) Foam::fvMatrixHolder< Foam::scalar >;

SCALAR_FVMATRIXHOLDER_TEMPLATE_FUNC;


//---------------------------------------------------------------------------
%feature( "pythonappend" ) Foam::fvMatrixHolder< Foam::scalar >::SMARTPTR_PYAPPEND_GETATTR( fvScalarMatrixHolder );

%extend Foam::fvMatrixHolder< Foam::scalar >
{
  SMARTPTR_EXTEND_ATTR( fvScalarMatrixHolder );
}


//--------------------------------------------------------------------------------------
#endif

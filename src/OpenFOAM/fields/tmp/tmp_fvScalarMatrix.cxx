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
#ifndef tmp_fvScalarMatrix_cxx
#define tmp_fvScalarMatrix_cxx


//---------------------------------------------------------------------------
// Keep on corresponding "director" includes at the top of SWIG defintion file

%include "src/OpenFOAM/directors.hxx"

%include "src/finiteVolume/directors.hxx"


//---------------------------------------------------------------------------
%include "src/OpenFOAM/fields/tmp/tmp.cxx"

%include "src/finiteVolume/fvMatrices/fvScalarMatrix.cxx"


//---------------------------------------------------------------------------
%template( tmp_fvScalarMatrix ) Foam::tmp< Foam::fvMatrix< Foam::scalar > >;

%inline
{
    namespace Foam
    {
        typedef tmp< fvMatrix< scalar > > tmp_fvScalarMatrix;
    }
}


//---------------------------------------------------------------------------
%feature( "pythonappend" ) Foam::tmp< Foam::fvMatrix< Foam::scalar > >::SMARTPTR_PYAPPEND_GETATTR( tmp_fvScalarMatrix );

%extend Foam::tmp< Foam::fvMatrix< Foam::scalar > >
{
    SMARTPTR_EXTEND_ATTR( tmp_fvScalarMatrix )
}


//---------------------------------------------------------------------------
#endif

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
//  See https://csrcs.pbmr.co.za/svn/nea/prototypes/reaktor/pyfoam
//
//  Author : Alexey PETROV


//---------------------------------------------------------------------------
#ifndef tmp_fvScalarMatrix_cxx
#define tmp_fvScalarMatrix_cxx


//---------------------------------------------------------------------------
%include "src/OpenFOAM/fields/tmp/tmp.cxx"

%include "src/finiteVolume/fvMatrices/fvScalarMatrix.cxx"


//---------------------------------------------------------------------------
%inline
{
    namespace Foam
    {
        typedef tmp< fvMatrix< scalar > > tmp_fvScalarMatrix;
    }
}

%feature( "pythonappend" ) Foam::tmp< Foam::fvMatrix< Foam::scalar > >::TMP_PYTHONAPPEND_ATTR( tmp_fvScalarMatrix );

%extend Foam::tmp< Foam::fvMatrix< Foam::scalar > >
{
    TMP_EXTEND_ATTR( tmp_fvScalarMatrix )
}


//---------------------------------------------------------------------------
%template( tmp_fvScalarMatrix ) Foam::tmp< Foam::fvMatrix< Foam::scalar > >;


//---------------------------------------------------------------------------
#endif

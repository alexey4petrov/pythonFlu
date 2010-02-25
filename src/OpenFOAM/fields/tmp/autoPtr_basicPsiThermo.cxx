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
#if ( __FOAM_VERSION__ < 010600 )
#define autoPtr_basicPsiThermo_cxx
%include "src/common.hxx"
#endif


//---------------------------------------------------------------------------
#ifndef autoPtr_basicPsiThermo_cxx
#define autoPtr_basicPsiThermo_cxx


//---------------------------------------------------------------------------
%include "src/OpenFOAM/fields/tmp/autoPtr.cxx"

%include "src/thermophysicalModels/basic/psiThermo/basicPsiThermo.cxx"


//---------------------------------------------------------------------------
AUTOPTR_TYPEMAP( Foam::basicPsiThermo )

%ignore Foam::autoPtr< Foam::basicPsiThermo >::operator->;

%template( autoPtr_basicPsiThermo ) Foam::autoPtr< Foam::basicPsiThermo >;

%inline
{
  namespace Foam
  {
    typedef autoPtr< basicPsiThermo > autoPtr_basicPsiThermo;
  }
}


//------------------------------------------------------------------------------
%feature( "pythonappend" ) Foam::autoPtr< Foam::basicPsiThermo >::TMP_PYTHONAPPEND_ATTR( autoPtr_basicPsiThermo );

%extend Foam::autoPtr< Foam::basicPsiThermo >
{
  TMP_EXTEND_ATTR( autoPtr_basicPsiThermo )
}

//---------------------------------------------------------------------------
#endif

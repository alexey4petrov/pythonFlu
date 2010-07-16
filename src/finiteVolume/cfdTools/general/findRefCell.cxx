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
#ifndef findRefCell_cxx
#define findRefCell_cxx


//---------------------------------------------------------------------------
// Keep on corresponding "director" includes at the top of SWIG defintion file

%include "src/OpenFOAM/directors.hxx"

%include "src/finiteVolume/directors.hxx"


//-------------------------------------------------------------------------------------
%include "src/common.hxx"

%include "src/OpenFOAM/primitives/label.cxx"
%include "src/OpenFOAM/primitives/scalar.cxx"
%include "src/finiteVolume/fields/volFields/volFields.cxx"

%{
    #include "findRefCell.H"
%}


//--------------------------------------------------------------------------------------
%inline
{
  namespace Foam
  {
    struct t_setRefCell
    {
      label m_refCelli;
      scalar m_refValue;
      t_setRefCell( label the_refCelli, scalar the_refValue ): m_refCelli( the_refCelli ),
                                                               m_refValue( the_refValue )
      {}
    };
  }
}


//--------------------------------------------------------------------------------------
%inline
{
#if ( __FOAM_VERSION__ < 010500 )
Foam::t_setRefCell ext_setRefCell( const Foam::volScalarField& field,
                                   const Foam::dictionary& dict,
                                   Foam::label refCelli,
                                   Foam::scalar refValue )
{
   Foam::setRefCell( field, dict, refCelli, refValue );
   return t_setRefCell( refCelli, refValue );
}                    
#endif

#if ( __FOAM_VERSION__ >= 010500 )
Foam::t_setRefCell ext_setRefCell( const Foam::volScalarField& field,
                                   const Foam::dictionary& dict,
                                   Foam::label refCelli,
                                   Foam::scalar refValue,
                                   const bool forceReference = false )
{
   Foam::setRefCell( field, dict, refCelli, refValue, forceReference);
   return t_setRefCell( refCelli, refValue );
}

#endif
}

//---------------------------------------------------------------------------
#endif

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
#ifndef PorousZonesHolder_thermalPorousZone_cpp
#define PorousZonesHolder_thermalPorousZone_cpp


//---------------------------------------------------------------------------
%import "Foam/src/finiteVolume/cfdTools/general/porousMedia/porousZones.cxx"

%import "Foam/src/thermophysicalModels/thermalPorousZone/thermalPorousZone.cxx"

%include "Foam/ext/common/thermophysicalModels/shared_ptr/shared_ptr_PorousZones_thermalPorousZone.hpp"

%template (PorousZonesHolder_thermalPorousZone) Foam::PorousZonesHolder< Foam::thermalPorousZone >;


//---------------------------------------------------------------------------
%feature( "pythonappend" ) Foam::PorousZonesHolder< Foam::thermalPorousZone >::SMARTPTR_PYAPPEND_GETATTR( PorousZonesHolder_thermalPorousZone );

%extend Foam::PorousZonesHolder< Foam::thermalPorousZone >
{
  SMARTPTR_EXTEND_ATTR( PorousZonesHolder_thermalPorousZone );
  HOLDERS_CALL_SHARED_PTR_EXTENSION_TEMPLATE1( Foam::PorousZones, Foam::thermalPorousZone )
}


//--------------------------------------------------------------------------------------
#endif

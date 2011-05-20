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
//  See http://sourceforge.net/projects/pythonflu
//
//  Author : Alexey PETROV


//---------------------------------------------------------------------------
#ifndef clock_cxx
#define clock_cxx


//---------------------------------------------------------------------------
%module "Foam.src.OpenFOAM.db.Time.clock";
%{
  #include "src/OpenFOAM/db/Time/clock.hh"
%}


//---------------------------------------------------------------------------
%import "src/OpenFOAM/primitives/strings/string.cxx"

%typemap( out ) time_t
{
  $result = PyInt_FromLong( $1 );
}

%include <clock.H>


//---------------------------------------------------------------------------
#endif

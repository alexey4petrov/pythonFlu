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
#ifndef OFstream_cxx
#define OFstream_cxx


//---------------------------------------------------------------------------
%module "Foam.src.OpenFOAM.db.IOstreams.Fstreams.OFstream";
%{
   #include "src/OpenFOAM/db/IOstreams/Fstreams/OFstream.hpp"
%}


//---------------------------------------------------------------------------
%import "src/common.hxx"

%import "src/OpenFOAM/primitives/strings/fileName.cxx"

%import "src/OpenFOAM/db/typeInfo/className.hxx"

%import "src/OpenFOAM/db/IOstreams/Sstreams/OSstream.cxx"

%ignore Foam::Snull;

%include <OFstream.H>


//---------------------------------------------------------------------------
#endif

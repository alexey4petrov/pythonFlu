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
#ifndef nuclearField_cxx
#define nuclearField_cxx


//---------------------------------------------------------------------------
%include "src/OpenFOAM/db/IOdictionary.cxx"

%include "ext/pbmr/diffusion/diffusion.hxx"

%include "ext/pbmr/diffusion/fluxGroups.cxx"
%include "ext/pbmr/diffusion/globalNuclearParameters.cxx"
%include "ext/pbmr/diffusion/heatProduction.cxx"
%include "ext/pbmr/diffusion/crossSectionSets.cxx"

%{
    #include "nuclearField.H"
%}

%include "nuclearField.H"


//---------------------------------------------------------------------------
#endif

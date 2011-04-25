// VulaSHAKA (Simultaneous Neutronic, Fuel Performance, Heat And Kinetics Analysis)
// Copyright (C) 2009-2010 Pebble Bed Modular Reactor (Pty) Limited (PBMR)
// 
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
// 
// You should have received a copy of the GNU General Public License
// along with this program.  If not, see <http://www.gnu.org/licenses/>.
// 
//  See https://vulashaka.svn.sourceforge.net/svnroot/vulashaka
//
// Author : Alexey PETROV


//---------------------------------------------------------------------------
#ifndef ext_tmp_scalarField_cxx
#define ext_tmp_scalarField_cxx


//---------------------------------------------------------------------------
%module "Foam.ext.common.OpenFOAM.ext_tmp.ext_tmp_scalarField";
%{
  #include "ext/common/OpenFOAM/ext_tmp/ext_tmp_scalarField.hh"
%}


//---------------------------------------------------------------------------
%import "src/common.hxx"

%import "ext/common/ext_tmp.hxx"

%import "src/OpenFOAM/fields/Fields/scalarField.cxx"

%ignore Foam::ext_tmp< Foam::Field< Foam::scalar > >::operator=;

%template ( ext_tmp_scalarField ) Foam::ext_tmp< Foam::Field< Foam::scalar > >;


//---------------------------------------------------------------------------
#endif


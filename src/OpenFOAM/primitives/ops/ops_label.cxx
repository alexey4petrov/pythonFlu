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
#ifndef ops_label_cxx
#define ops_label_cxx

%include "src/OpenFOAM/primitives/ops/ops.cxx"
%include "src/OpenFOAM/primitives/label.cxx"


//---------------------------------------------------------------------------
%template (eqOp_label) Foam::eqOp<Foam::label>;
%template (plusEqOp_label) Foam::plusEqOp<Foam::label>;
%template (minusEqOp_label) Foam::minusEqOp<Foam::label>;
%template (multiplyEqOp_label) Foam::multiplyEqOp<Foam::label>;
%template (divideEqOp_label) Foam::divideEqOp<Foam::label>;
%template (eqMagOp_label) Foam::eqMagOp<Foam::label>;
%template (maxEqOp_label) Foam::maxEqOp<Foam::label>;
%template (minEqOp_label) Foam::minEqOp<Foam::label>;
%template (andEqOp_label) Foam::andEqOp<Foam::label>;
%template (orEqOp_label) Foam::orEqOp<Foam::label>;
%template (eqMinusOp_label) Foam::eqMinusOp<Foam::label>;


%template (sumOp_label) Foam::sumOp<Foam::label>;
%template (plusOp_label) Foam::plusOp<Foam::label>;
%template (minusOp_label) Foam::minusOp<Foam::label>;
%template (multiplyOp_label) Foam::multiplyOp<Foam::label>;
%template (divideOp_label) Foam::divideOp<Foam::label>;
%template (maxOp_label) Foam::maxOp<Foam::label>;
%template (minOp_label) Foam::minOp<Foam::label>;
%template (andOp_label) Foam::andOp<Foam::label>;


//---------------------------------------------------------------------------
#endif

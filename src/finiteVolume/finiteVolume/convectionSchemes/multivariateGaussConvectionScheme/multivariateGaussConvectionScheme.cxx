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
#ifndef multivariateGaussConvectionScheme_cxx
#define multivariateGaussConvectionScheme_cxx


//---------------------------------------------------------------------------
// Keep on corresponding "director" includes at the top of SWIG defintion file

%include "src/OpenFOAM/directors.hxx"

%include "src/finiteVolume/directors.hxx"


//---------------------------------------------------------------------------
%include "src/finiteVolume/finiteVolume/convectionSchemes/convectionScheme/convectionScheme.cxx"


//----------------------------------------------------------------------------
%{
    #include "multivariateGaussConvectionScheme.H"
%}

%include "multivariateGaussConvectionScheme.H"


//---------------------------------------------------------------------------
%define MULTIVARIATEGAUSSCONVECTIONSCHEME_TEMPLATE_FUNC( Type )
{
 Foam::fv::multivariateGaussConvectionScheme< Foam::Type>( const Foam::fvMesh& mesh,
                                                           const Foam::TfieldTable< Foam::Type >& fields,
                                                           const surfaceScalarField& faceFlux,
                                                                 Istream& is)
 {
    return new Foam::fv::multivariateGaussConvectionScheme< Foam::Type >( mesh, fields.get_self(), faceFlux, is );
 }
}  
%enddef


//---------------------------------------------------------------------------
#endif

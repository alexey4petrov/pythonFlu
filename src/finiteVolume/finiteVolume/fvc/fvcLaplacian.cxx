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
#ifndef fvcLaplacian_cxx
#define fvcLaplacian_cxx


//---------------------------------------------------------------------------
// Keep on corresponding "director" includes at the top of SWIG defintion file

%include "src/OpenFOAM/directors.hxx"

%include "src/finiteVolume/directors.hxx"


//---------------------------------------------------------------------------
%{
    #include "fvcLaplacian.H"
%}


//---------------------------------------------------------------------------
%include "src/finiteVolume/fields/volFields/volFields.cxx"


//---------------------------------------------------------------------------
%define FVC_LAPLACIAN_TEMPLATE_FUNC( Type1, Type2 )
%{
    Foam::tmp< Foam::GeometricField< Type1, Foam::fvPatchField, Foam::volMesh> > fvc_laplacian
    (
       const Foam::GeometricField< Type2, Foam::fvPatchField, Foam::volMesh>& gamma,
       const Foam::GeometricField< Type1, Foam::fvPatchField, Foam::volMesh>& vf
    )
    {
        return Foam::fvc::laplacian( gamma, vf );
    }
%}
%enddef 


//---------------------------------------------------------------------------
%inline FVC_LAPLACIAN_TEMPLATE_FUNC( Foam::scalar, Foam::scalar )


//---------------------------------------------------------------------------
%include "fvcLaplacian.H"


//---------------------------------------------------------------------------
#endif

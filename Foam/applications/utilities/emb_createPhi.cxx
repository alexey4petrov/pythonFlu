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
//  Author : Ivor CLIFFORD


//---------------------------------------------------------------------------
#ifndef emb_createPhi_cxx
#define emb_createPhi_cxx


//---------------------------------------------------------------------------
// Keep on corresponding "director" includes at the top of SWIG defintion file

%include "src/OpenFOAM/directors.hxx"

%include "src/finiteVolume/directors.hxx"


//---------------------------------------------------------------------------
%include "src/OpenFOAM/fields/GeometricFields/GeometricField_vector_fvPatchField_volMesh.cxx"
%include "src/OpenFOAM/fields/GeometricFields/GeometricField_scalar_fvsPatchField_surfaceMesh.cxx"


//---------------------------------------------------------------------------
%typemap( out ) Foam::surfaceScalarField
{
    $result = SWIG_NewPointerObj( ( new $1_type( *&$1 ) ), $&1_descriptor, SWIG_POINTER_OWN |  0 );
}


//---------------------------------------------------------------------------
%inline
%{
    #include "linear.H"

    namespace Foam
    {
        //- Global function for flux creation
        surfaceScalarField execute( const volVectorField& U )
        {
            return surfaceScalarField
                (
                    IOobject
                    (
                        "phi",
                        U.db().time().timeName(),
                        U.mesh(),
                        IOobject::READ_IF_PRESENT,
                        IOobject::AUTO_WRITE
                        ),
                    linearInterpolate(U) & U.mesh().Sf()
                    );
        }
    }
%}


//---------------------------------------------------------------------------
#endif

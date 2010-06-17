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
#ifndef sphericalTensor_cxx
#define sphericalTensor_cxx


//---------------------------------------------------------------------------
%include "src/OpenFOAM/primitives/vector.cxx"

%include "src/OpenFOAM/primitives/scalar.cxx"

%include "src/OpenFOAM/primitives/SphericalTensor.cxx"

%include "src/OpenFOAM/primitives/contiguous.cxx"

%template( VectorSpace_sphericalTensor ) Foam::VectorSpace< Foam::SphericalTensor< Foam::scalar >, Foam::scalar, 1 >;

%extend Foam::VectorSpace< Foam::Foam::SphericalTensor< Foam::scalar >, Foam::scalar, 1 >
{
    int __len__()
    {
        return self->size();
    }
    
    Foam::scalar __getitem__( const Foam::direction theIndex )
    {
            return self->operator[]( theIndex );
    }

    void __setitem__( const Foam::direction theIndex, const Foam::scalar& theValue )
    {
        self->operator[]( theIndex ) = theValue;
    }
}

%{
    #include "sphericalTensor.H"
%}

%include "sphericalTensor.H"

%template ( sphericalTensor ) Foam::SphericalTensor< Foam::scalar >;


//---------------------------------------------------------------------------
#endif

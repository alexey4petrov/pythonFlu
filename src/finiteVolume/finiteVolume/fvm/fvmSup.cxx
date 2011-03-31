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
#ifndef fvmSup_cxx
#define fvmSup_cxx


//---------------------------------------------------------------------------
// Keep on corresponding "director" includes at the top of SWIG defintion file

%include "src/OpenFOAM/directors.hxx"

%include "src/finiteVolume/directors.hxx"


//---------------------------------------------------------------------------
%include "src/finiteVolume/fields/fvPatchFields/fvPatchField.cxx"

%{
    #include "fvmSup.H"
%}


//---------------------------------------------------------------------------
%include "src/OpenFOAM/dimensionedTypes/dimensionedScalar.cxx"
%include "src/OpenFOAM/fields/DimensionedFields/DimensionedField_scalar_volMesh.cxx"
%include "src/OpenFOAM/fields/tmp/tmp_volScalarField.cxx"
%include "src/OpenFOAM/fields/tmp/tmp_DimensionedField_scalar_volMesh.cxx"
%include "src/OpenFOAM/dimensionedTypes/dimensionedScalar.cxx"



//---------------------------------------------------------------------------
%define FVM_SUP_TEMPLATE_FUNC( Type )
%{
    #if FOAM_VERSION( <, 010500 )
    Foam::tmp<Foam::fvMatrix<Type> > fvm_Sp( const Foam::volScalarField& sp, 
                                               Foam::GeometricField<Type, Foam::fvPatchField, Foam::volMesh>& vf)
    {
      return Foam::fvm::Sp( sp, vf );
    }
    //The zero is not implemented yet
    /*Foam::zero  Sp( const zero&, GeometricField<Type, fvPatchField, volMesh>& )
    {
      return zero();
    }*/
    #endif
    
    
    #if FOAM_VERSION( >=, 010500 )
    Foam::tmp<Foam::fvMatrix<Type> > fvm_Sp( const Foam::DimensionedField<scalar, volMesh>& sp, 
                                               Foam::GeometricField<Type, Foam::fvPatchField, Foam::volMesh>& vf )
    {
      return Foam::fvm::Sp( sp, vf );
    }
    
    //The zeroField is not implemented yet
    /*Foam::zeroField  Sp( const zeroField&, GeometricField<Type, fvPatchField, volMesh>& )
    {
      return zeroField();
    }*/
    #endif
   
   
    Foam::tmp<Foam::fvMatrix<Type> > fvm_Sp( const Foam::tmp<volScalarField>& tsp, 
                                               Foam::GeometricField<Type, Foam::fvPatchField, Foam::volMesh>& vf )
    {
      return Foam::fvm::Sp( tsp, vf );
    }
    
    Foam::tmp<Foam::fvMatrix<Type> > fvm_Sp( const Foam::dimensionedScalar& sp, 
                                               Foam::GeometricField<Type, Foam::fvPatchField, Foam::volMesh>& vf )
    {
      return Foam::fvm::Sp( sp, vf );
    }
    
    
%}
%enddef


//---------------------------------------------------------------------------
%include "src/OpenFOAM/fields/tmp/tmp_fvScalarMatrix.cxx"
%include "src/OpenFOAM/fields/GeometricFields/GeometricField_scalar_fvPatchField_volMesh.cxx"

%inline FVM_SUP_TEMPLATE_FUNC( Foam::scalar )

//---------------------------------------------------------------------------
%include "src/OpenFOAM/fields/tmp/tmp_fvVectorMatrix.cxx"
%include "src/OpenFOAM/fields/GeometricFields/GeometricField_vector_fvPatchField_volMesh.cxx"

%inline FVM_SUP_TEMPLATE_FUNC( Foam::vector )

//---------------------------------------------------------------------------
%include "src/finiteVolume/volMesh.cxx"


//---------------------------------------------------------------------------
%include "fvmSup.H"


//---------------------------------------------------------------------------
#endif

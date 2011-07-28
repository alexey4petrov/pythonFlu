//  pythonFlu - Python wrapping for OpenFOAM C++ API
//  Copyright (C) 2010- Alexey Petrov
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
#ifndef lduMatrix_cxx
#define lduMatrix_cxx


//---------------------------------------------------------------------------
%module "Foam.src.OpenFOAM.matrices.lduMatrix.lduMatrix"
%{
  #include "Foam/src/OpenFOAM/matrices/lduMatrix/lduMatrix.hh"
%}


//---------------------------------------------------------------------------
%import "Foam/src/OpenFOAM/matrices/lduMatrix/lduAddressing/lduAddressing.cxx"

%import "Foam/src/OpenFOAM/matrices/lduMatrix/lduAddressing/lduSchedule.cxx"

%import "Foam/src/OpenFOAM/meshes/lduMesh.cxx"

%import "Foam/src/OpenFOAM/fields/Fields/primitiveFields.cxx"


//---------------------------------------------------------------------------
//- Class returned by the solver
//  containing performance statistics

%rename( ext_print ) Foam::lduSolverPerformance::print;

namespace Foam
{
  struct lduSolverPerformance
  {
    // Constructors
    
    lduSolverPerformance();
    
    lduSolverPerformance
    (
     const word&  solverName,
     const word&  fieldName,
     const scalar iRes = 0,
     const scalar fRes = 0,
     const label  nIter = 0,
     const bool   converged = false,
     const bool   singular = false
     );

    // Member functions
    
    //- Return solver name
    const word& solverName() const;
    
    //- Return initial residual
    scalar initialResidual() const;
    
    //- Return initial residual
    scalar& initialResidual();
    
    //- Return final residual
    scalar finalResidual() const;
    
    //- Return final residual
    scalar& finalResidual();
    
    //- Return number of iterations
    label nIterations() const;
    
    //- Return number of iterations
    label& nIterations();
    
    //- Has the solver converged?
    bool converged() const;
    
    //- Is the matrix singular?
    bool singular() const;
    
    //- Convergence test
    bool checkConvergence
    (
     const scalar tolerance,
     const scalar relTolerance
     );
    
    //- Singularity test
    bool checkSingularity(const scalar residual);
    
    //- Print summary of solver performance
    void print() const;
  };
}


//---------------------------------------------------------------------------
%import "Foam/src/OpenFOAM/db/typeInfo/className.hxx"

#if FOAM_BRANCH_VERSION( dev, >=, 010500 )
%ignore Foam::lduMatrix::bufferedUpdateMatrixInterfaces;
%ignore Foam::lduMatrix::bufferedInitMatrixInterfaces;
#endif

%include <lduMatrix.H>


//---------------------------------------------------------------------------
%include "Foam/src/OpenFOAM/matrices/lduMatrix/lduMatrix.hh"

// This trick intends to publish nested class into SWIG domain
%typemap( out ) Foam::lduMatrix::solverPerformance
{
  $result = SWIG_NewPointerObj( ( new $1_type( *&$1 ) ), $descriptor( Foam::lduSolverPerformance* ), SWIG_POINTER_OWN |  0 );
}


//---------------------------------------------------------------------------
#endif

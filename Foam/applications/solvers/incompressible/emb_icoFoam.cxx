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
#ifndef emb_icoFoam_cxx
#define emb_icoFoam_cxx


//---------------------------------------------------------------------------
// Keep on corresponding "director" includes at the top of SWIG defintion file

%include "src/OpenFOAM/directors.hxx"

%include "src/finiteVolume/directors.hxx"


//---------------------------------------------------------------------------
%include "src/finiteVolume/fields/volFields/volVectorField.cxx"
%include "src/finiteVolume/fields/volFields/volScalarField.cxx"
%include "src/finiteVolume/fields/surfaceFields/surfaceScalarField.cxx"
%include "src/OpenFOAM/db/IOdictionary.cxx"


//---------------------------------------------------------------------------
%inline
%{
    #include "fvCFD.H"

    namespace Foam
    {
        class solver
        {
        private:
            
            // Run time
            Time& runTime_;
            
            //- Velocity field
            volVectorField& U_;
            
            //- Pressure field
            volScalarField& p_;
            
            //- Flux field
            surfaceScalarField& phi_;
            
            //- Transport properties
            const IOdictionary& transportProperties_;
            
            // Mesh
            const fvMesh& mesh_;
            
            //- Reference cells
            label pRefCell_;
            scalar pRefValue_;
            
            //- Residuals
            scalar pressureRes_;
            scalar velocityRes_;
            
        public:
 
            //- Construct given fields and transport properties
            solver
            (
                Time& runTime,
                volVectorField& U,
                volScalarField& p,
                surfaceScalarField& phi,
                const IOdictionary& transportProperties
                )
                :
                runTime_(runTime),
                U_(U),
                p_(p),
                phi_(phi),
                transportProperties_(transportProperties),
                mesh_(U.mesh()),
                pRefCell_(0),
                pRefValue_(0),
                pressureRes_(0),
                velocityRes_(0)
                {
                    // Grab reference cell
                    setRefCell
                        (
                            p_,
                            mesh_.solutionDict().subDict("PISO"),
                            pRefCell_,
                            pRefValue_
                            );
                }
            
            
            // Step
            void step()
            {
                if (runTime_.end())
                {
                    Info << "Reached end time.  Exiting" << endl;
                    return;
                }
                
                runTime_++;
                
                // Read transport properties
                dimensionedScalar nu(transportProperties_.lookup("nu"));
                
                if (mesh_.nInternalFaces())
                {
                    surfaceScalarField SfUfbyDelta = 
                        mesh_.surfaceInterpolation::deltaCoeffs()*mag(phi_);
                    
                    scalar CoNum = max(SfUfbyDelta/mesh_.magSf())
                        .value()*runTime_.deltaT().value();
                    
                    scalar meanCoNum = (sum(SfUfbyDelta)/sum(mesh_.magSf()))
                        .value()*runTime_.deltaT().value();
                    
                    Info<< "Courant Number mean: " << meanCoNum
                        << " max: " << CoNum << endl;
                }
                
                // Read controls
                dictionary piso = mesh_.solutionDict().subDict("PISO");
                
                int nCorr(readInt(piso.lookup("nCorrectors")));
                
                int nNonOrthCorr = 0;
                if (piso.found("nNonOrthogonalCorrectors"))
                {
                    nNonOrthCorr = readInt(piso.lookup("nNonOrthogonalCorrectors"));
                }
                
                fvVectorMatrix UEqn
                    (
                        fvm::ddt(U_)
                        + fvm::div(phi_, U_)
                        - fvm::laplacian(nu, U_)
                        );
                
                velocityRes_ = solve(UEqn == -fvc::grad(p_)).initialResidual();
                
                // --- PISO loop
                
                for (int corr=0; corr<nCorr; corr++)
                {
                    volScalarField rUA = 1.0/UEqn.A();
                    
                    U_ = rUA*UEqn.H();
                    phi_ = (fvc::interpolate(U_) & mesh_.Sf()) 
                        + fvc::ddtPhiCorr(rUA, U_, phi_);
                    
//             adjustPhi(phi_, U_, p_);
                    
                    for (int nonOrth=0; nonOrth<=nNonOrthCorr; nonOrth++)
                    {
                        fvScalarMatrix pEqn
                            (
                                fvm::laplacian(rUA, p_) == fvc::div(phi_)
                                );
                        
                        pEqn.setReference(pRefCell_, pRefValue_);
                        pressureRes_ = pEqn.solve().initialResidual();
                        
                        if (nonOrth == nNonOrthCorr)
                        {
                            phi_ -= pEqn.flux();
                        }
                    }
                    
                    // Continuity errors
                    volScalarField contErr = fvc::div(phi_);
                    
                    scalar sumLocalContErr = runTime_.deltaT().value()*
                        mag(contErr)().weightedAverage(mesh_.V()).value();
                    
                    scalar globalContErr = runTime_.deltaT().value()*
                        contErr.weightedAverage(mesh_.V()).value();
                    
                    Info<< "time step continuity errors : sum local = "
                        << sumLocalContErr << ", global = " << globalContErr << endl;
                    
                    // Correct velocity
                    U_ -= rUA*fvc::grad(p_);
                    U_.correctBoundaryConditions();
                }
                
                Info<< "ExecutionTime = " << runTime_.elapsedCpuTime() << " s"
                    << "  ClockTime = " << runTime_.elapsedClockTime() << " s"
                    << nl << endl;
            }
            
            //- Residuals
            scalar pressureRes() const
            {
                return pressureRes_;
            }
            
            scalar velocityRes() const
            {
                return velocityRes_;
            }
        };
    }
%}


//---------------------------------------------------------------------------
#endif

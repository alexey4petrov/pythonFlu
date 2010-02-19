#include "fvCFD.H"
#include <boost/shared_ptr.hpp>
typedef boost::shared_ptr<Foam::Time> t_time_ptr;
typedef boost::shared_ptr<Foam::fvMesh> t_fvMesh_ptr;
typedef boost::shared_ptr<Foam::IOdictionary> t_IOdictionary_ptr;
typedef boost::shared_ptr<Foam::volScalarField> t_volScalarField_ptr;
typedef boost::shared_ptr<Foam::volVectorField> t_volVectorField_ptr;
typedef boost::shared_ptr<Foam::surfaceScalarField> t_surfaceScalarField_ptr;
typedef boost::shared_ptr<Foam::dimensionedScalar> t_dimensionedScalar_ptr;

namespace Foam
{

struct t_piso_controls
{
  dictionary piso;
  int nCorr;
  int nNonOrthCorr;
  bool momentumPredictor;
  bool fluxGradp;
  bool transSonic;
  int nOuterCorr;
};

struct t_fields
{
  t_IOdictionary_ptr transportProperties_ptr;
  t_volScalarField_ptr p_ptr;
  t_volVectorField_ptr U_ptr;
  t_surfaceScalarField_ptr phi_ptr;
  t_dimensionedScalar_ptr nu_ptr;
  label pRefCell;
  scalar pRefValue;
};
  

  class t_get_time_base 
  {
  public:
    virtual t_time_ptr call() const = 0;
  };
  
  class t_get_mesh_base
  {
    public:
      virtual t_fvMesh_ptr call(const Time& the_runTime) const = 0; 
  };

  class t_piso_controls_base
  {
    public:
      virtual t_piso_controls call(const fvMesh& the_mesh) const = 0;
  };
  
  class t_get_fields_base
  {
  public:
    virtual t_fields call(const Time& the_run_time, const fvMesh& the_mesh) const = 0;
  };
  
 
  class t_get_time:public t_get_time_base
  {
  public:
    t_time_ptr m_time_ptr;
    t_get_time(const word& the_dict, const  fileName& the_rootPath, const fileName& the_caseName )
    {
      t_time_ptr a_time_ptr(new Time(the_dict, the_rootPath, the_caseName));
      m_time_ptr=a_time_ptr;
    } 
    virtual t_time_ptr call() const
    { 
      return m_time_ptr;
    }
  };
  
  
  
  class t_get_mesh :public t_get_mesh_base
  {
    public:
      virtual t_fvMesh_ptr call(const Time& the_runTime) const 
      {
        Info<< "Create mesh for time = "
        << the_runTime.timeName() << nl << endl;

        t_fvMesh_ptr  a_mesh(new fvMesh
        (
          IOobject
          (
            fvMesh::defaultRegion,
            the_runTime.timeName(),
            the_runTime,
            IOobject::MUST_READ
          )
        ) 
        );
        return a_mesh;
      } 
  };
  
  class t_read_piso_controls :
             public t_piso_controls_base
  {
    public:
      virtual t_piso_controls call(const fvMesh& the_mesh) const 
      {
        t_piso_controls a_piso_ctrls;
        
        a_piso_ctrls.piso = the_mesh.solutionDict().subDict("PISO");

        a_piso_ctrls.nCorr=readInt(a_piso_ctrls.piso.lookup("nCorrectors"));

        a_piso_ctrls.nNonOrthCorr = 0;
          if (a_piso_ctrls.piso.found("nNonOrthogonalCorrectors"))
          {
            a_piso_ctrls.nNonOrthCorr = readInt(a_piso_ctrls.piso.lookup("nNonOrthogonalCorrectors"));
          }

          a_piso_ctrls.momentumPredictor = true;
            if (a_piso_ctrls.piso.found("momentumPredictor"))
            {
              a_piso_ctrls.momentumPredictor = Switch(a_piso_ctrls.piso.lookup("momentumPredictor"));
            }

          a_piso_ctrls.fluxGradp = false;
            if (a_piso_ctrls.piso.found("fluxGradp"))
            {
              a_piso_ctrls.fluxGradp = Switch(a_piso_ctrls.piso.lookup("fluxGradp"));
            }

          a_piso_ctrls.transSonic = false;
            if (a_piso_ctrls.piso.found("transSonic"))
              {
                a_piso_ctrls.transSonic = Switch(a_piso_ctrls.piso.lookup("transSonic"));
              }

          a_piso_ctrls.nOuterCorr = 1;
          if (a_piso_ctrls.piso.found("nOuterCorrectors"))
          {
            a_piso_ctrls.nOuterCorr = readInt(a_piso_ctrls.piso.lookup("nOuterCorrectors"));
          }
          return a_piso_ctrls;
      }
  };
  
  
  class t_get_fields: public t_get_fields_base
  {
  public:
    virtual t_fields call(const Time& the_run_time, const fvMesh& the_mesh) const 
    {
      t_fields a_fields;
      
      Info<< "Reading transportProperties\n" << endl;

      t_IOdictionary_ptr a_transportProperties_ptr
      ( new IOdictionary
        (
          IOobject
          (
            "transportProperties",
            the_run_time.constant(),
            the_mesh,
            IOobject::MUST_READ,
            IOobject::NO_WRITE
          )
        )
      );
      a_fields.transportProperties_ptr = a_transportProperties_ptr;

      // nu
      IOdictionary& a_transportProperties = *a_fields.transportProperties_ptr;
      
      t_dimensionedScalar_ptr a_nu_ptr(new dimensionedScalar(a_transportProperties.lookup("nu")));
      
      
      a_fields.nu_ptr=a_nu_ptr;

      // p
      Info<< "Reading field p\n" << endl;
      t_volScalarField_ptr a_p_ptr
      ( new volScalarField
       (
         IOobject
         (
            "p",
            the_run_time.timeName(),
            the_mesh,
            IOobject::MUST_READ,
            IOobject::AUTO_WRITE
          ),
          the_mesh
        )
      );
      a_fields.p_ptr=a_p_ptr;

      //U
      Info<< "Reading field U\n" << endl;
      t_volVectorField_ptr a_U_ptr
      ( new volVectorField
        (
          IOobject
          (
            "U",
            the_run_time.timeName(),
            the_mesh,
            IOobject::MUST_READ,
            IOobject::AUTO_WRITE
          ),
          the_mesh
        )  
      );
      a_fields.U_ptr = a_U_ptr;
    
      volVectorField& a_U = *a_fields.U_ptr; 
      //phi
      Info<< "Reading/calculating face flux field phi\n" << endl;

      t_surfaceScalarField_ptr a_phi_ptr
       ( new surfaceScalarField
        (
          IOobject
          (
            "phi",
            the_run_time.timeName(),
            the_mesh,
            IOobject::READ_IF_PRESENT,
            IOobject::AUTO_WRITE
          ),
        linearInterpolate(a_U) & the_mesh.Sf()
       )
    );

    a_fields.pRefCell = 0;
    a_fields.pRefValue = 0.0;
    volScalarField& a_p=*a_fields.p_ptr;
    setRefCell(a_p, the_mesh.solutionDict().subDict("PISO"), a_fields.pRefCell, a_fields.pRefValue);
      
    return a_fields;
    }
  };
  
   
 
  class solver
  {
  private:
    //  Time
    t_time_ptr m_run_time_ptr;
    
    //- Velocity field
    t_volVectorField_ptr m_U_ptr;
	    
    //- Pressure field
    t_volScalarField_ptr m_p_ptr;
	    
    //- Flux field
    t_surfaceScalarField_ptr m_phi_ptr;
    
    // NU
    t_dimensionedScalar_ptr m_nu_ptr;
	    
    //- Transport properties
    t_IOdictionary_ptr m_transportProperties_ptr;
	    
    // Mesh
    t_fvMesh_ptr  m_mesh_ptr;
	    
    //- Reference cells
    label m_pRefCell;
    scalar m_pRefValue;
    
    //Cumulative errors
    scalar m_cumulativeContErr;
	    
    	    
  public:
 
    //- Construct given fields and transport properties
    solver( t_get_time_base* the_get_time, t_get_mesh_base* the_get_mesh, t_get_fields_base* the_get_fields) : m_cumulativeContErr(0)
       
    {
      // get Time
      m_run_time_ptr = the_get_time->call();
      Time& a_run_time = *m_run_time_ptr;
           
      //get Mesh
      m_mesh_ptr = the_get_mesh->call( a_run_time );

      fvMesh& a_mesh = *m_mesh_ptr;
      
      //get Fields
      t_fields a_fields=the_get_fields->call( a_run_time, a_mesh );
      
      m_transportProperties_ptr=a_fields.transportProperties_ptr;
      m_U_ptr=a_fields.U_ptr;
      m_p_ptr=a_fields.p_ptr;
      m_phi_ptr=a_fields.phi_ptr;
      m_nu_ptr=a_fields.nu_ptr;
      m_pRefCell=a_fields.pRefCell;
      m_pRefValue=a_fields.pRefValue;
	    
      
    }
	    
	   
    // Step

    void step(t_piso_controls_base* the_read_piso_controls)
    { 
      //dereferencing
       
      Time& a_run_time = *m_run_time_ptr;
      fvMesh& a_mesh = *m_mesh_ptr;
      volVectorField& a_U = *m_U_ptr;
      volScalarField& a_p = *m_p_ptr;
      
      surfaceScalarField& a_phi = *m_phi_ptr;

      dimensionedScalar& a_nu = *m_nu_ptr;
      IOdictionary a_transportProperties = *m_transportProperties_ptr;
      
     
      //Read PISOControls
      t_piso_controls a_piso_ctrls;
      a_piso_ctrls = the_read_piso_controls->call(a_mesh);
      
      int a_nCorr = a_piso_ctrls.nCorr;
      int a_nNonOrthCorr=a_piso_ctrls.nNonOrthCorr;
      
      
      
      scalar CoNum = 0.0;
      scalar meanCoNum = 0.0;
      // scalar acousticCoNum = 0.0;

      if (a_mesh.nInternalFaces())
      {
        surfaceScalarField SfUfbyDelta = 
             a_mesh.surfaceInterpolation::deltaCoeffs()*mag(a_phi);

        CoNum = max(SfUfbyDelta/a_mesh.magSf())
             .value()*a_run_time.deltaT().value();

        meanCoNum = (sum(SfUfbyDelta)/sum(a_mesh.magSf()))
              .value()*a_run_time.deltaT().value();

      }

      Info<< "Courant Number mean: " << meanCoNum
          << " max: " << CoNum
          << endl;
          
      fvVectorMatrix UEqn
        (
            fvm::ddt(a_U)
          + fvm::div(a_phi, a_U)
          - fvm::laplacian(a_nu, a_U)
        );

        solve(UEqn == -fvc::grad(a_p));

        // --- PISO loop

        for (int corr=0; corr<a_nCorr; corr++)
        {
            volScalarField rUA = 1.0/UEqn.A();

            a_U = rUA*UEqn.H();
            a_phi = (fvc::interpolate(a_U) & a_mesh.Sf()) 
                + fvc::ddtPhiCorr(rUA, a_U, a_phi);

            adjustPhi(a_phi, a_U, a_p);

            for (int nonOrth=0; nonOrth<=a_nNonOrthCorr; nonOrth++)
            {
                fvScalarMatrix pEqn
                (
                    fvm::laplacian(rUA, a_p) == fvc::div(a_phi)
                );

                pEqn.setReference(m_pRefCell, m_pRefValue);
                pEqn.solve();

                if (nonOrth == a_nNonOrthCorr)
                {
                    a_phi -= pEqn.flux();
                }
            }
            
            volScalarField contErr = fvc::div(a_phi);

            scalar sumLocalContErr = a_run_time.deltaT().value()*
                mag(contErr)().weightedAverage(a_mesh.V()).value();

            scalar globalContErr = a_run_time.deltaT().value()*
                contErr.weightedAverage(a_mesh.V()).value();
            
            m_cumulativeContErr += globalContErr;

            Info<< "time step continuity errors : sum local = " << sumLocalContErr
                << ", global = " << globalContErr
                << ", cumulative = " << m_cumulativeContErr
                << endl;
                
            a_U -= rUA*fvc::grad(a_p);
            a_U.correctBoundaryConditions();
        }

        a_run_time.write();

        Info<< "ExecutionTime = " << a_run_time.elapsedCpuTime() << " s"
            << "  ClockTime = " << a_run_time.elapsedClockTime() << " s"
            << nl << endl;
    }
	    
    
    void run(t_piso_controls_base* the_read_piso_controls)
    {
       
      Info<< "\nStarting time loop\n" << endl;
      Time& a_run_time = *m_run_time_ptr;
      for (a_run_time++; !a_run_time.end(); a_run_time++)
      {
        this->step(the_read_piso_controls);
      }
    }
    
  };
}



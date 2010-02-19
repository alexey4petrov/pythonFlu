//---------------------------------------------------------------------------
#ifndef createPhi_cxx
#define createPhi_cxx


//---------------------------------------------------------------------------
%include "src/OpenFOAM/fields/GeometricFields/GeometricField_vector_fvPatchField_volMesh.cxx"

%include "src/OpenFOAM/fields/GeometricFields/GeometricField_scalar_fvsPatchField_surfaceMesh.cxx"

%typemap( out ) Foam::surfaceScalarField
{
    $result = SWIG_NewPointerObj( ( new $1_type( *&$1 ) ), $&1_descriptor, SWIG_POINTER_OWN |  0 );
}

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

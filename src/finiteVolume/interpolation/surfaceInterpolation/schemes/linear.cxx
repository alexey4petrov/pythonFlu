//---------------------------------------------------------------------------
#ifndef linear_cxx
#define linear_cxx

//---------------------------------------------------------------------------
// Keep on corresponding "director" includes at the top of SWIG defintion file

%include "src/OpenFOAM/directors.hxx"

%include "src/finiteVolume/directors.hxx"


//---------------------------------------------------------------------------
%include "src/OpenFOAM/fields/tmp/tmp.cxx"

%include "src/finiteVolume/fields/volFields/volFields.cxx"

%include "src/finiteVolume/fields/surfaceFields/surfaceFields.cxx"

%{
    #include "linear.H"
%}

%include "linear.H"


//---------------------------------------------------------------------------
%define FOAM_LINEAR_INTERPOLATE_TEMPLATE_FUNC( Type )
%{
    Foam::tmp< Foam::GeometricField< Type, Foam::fvsPatchField, Foam::surfaceMesh > > linearInterpolate
    (
        const Foam::GeometricField< Type, Foam::fvPatchField, Foam::volMesh >& vf
    )
    {
        return Foam::linearInterpolate( vf );
    }

%}
%enddef


//---------------------------------------------------------------------------
%inline FOAM_LINEAR_INTERPOLATE_TEMPLATE_FUNC( Foam::vector )

%inline FOAM_LINEAR_INTERPOLATE_TEMPLATE_FUNC( Foam::scalar )


//---------------------------------------------------------------------------
#endif

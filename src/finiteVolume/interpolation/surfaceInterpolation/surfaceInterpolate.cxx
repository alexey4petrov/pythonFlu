//---------------------------------------------------------------------------
#ifndef surfaceInterpolate_cxx
#define surfaceInterpolate_cxx


//---------------------------------------------------------------------------
// Keep on corresponding "director" includes at the top of SWIG defintion file

%include "src/OpenFOAM/directors.hxx"

%include "src/finiteVolume/directors.hxx"


//---------------------------------------------------------------------------
%include "src/finiteVolume/fields/volFields/volFields.cxx"

%include "src/finiteVolume/fields/surfaceFields/surfaceFields.cxx"

%{
    #include "surfaceInterpolate.H"
%}

%include "surfaceInterpolate.H"


//---------------------------------------------------------------------------
%define FVC_INTERPOLATE_TEMPLATE_FUNC( Type )
%{
    Foam::tmp< Foam::GeometricField< Type, Foam::fvsPatchField, Foam::surfaceMesh > > interpolate
    (
        const Foam::GeometricField< Type, Foam::fvPatchField, Foam::volMesh >& vf
    )
    {
        return Foam::fvc::interpolate( vf );
    }

    Foam::tmp< GeometricField< Type, Foam::fvsPatchField, Foam::surfaceMesh> > interpolate
    (
        const Foam::GeometricField<Type, Foam::fvPatchField, Foam::volMesh>& tvf,
        const Foam::word& name
    )
    {
        return Foam::fvc::interpolate( tvf, name );
    }
    
%}
%enddef


//---------------------------------------------------------------------------
%inline FVC_INTERPOLATE_TEMPLATE_FUNC( Foam::vector )

%inline FVC_INTERPOLATE_TEMPLATE_FUNC( Foam::scalar )


//---------------------------------------------------------------------------
#endif

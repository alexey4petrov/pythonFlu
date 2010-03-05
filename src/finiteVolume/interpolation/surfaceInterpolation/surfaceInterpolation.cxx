//---------------------------------------------------------------------------
#ifndef surfaceInterpolation_cxx
#define surfaceInterpolation_cxx


//---------------------------------------------------------------------------
// Keep on corresponding "director" includes at the top of SWIG defintion file

%include "src/OpenFOAM/directors.hxx"

%include "src/finiteVolume/directors.hxx"


//---------------------------------------------------------------------------
%include "src/OpenFOAM/fields/tmp/tmp.cxx"

%include "src/OpenFOAM/primitives/scalar.cxx"
%include "src/finiteVolume/finiteVolume/fvSchemes.cxx"
%include "src/finiteVolume/finiteVolume/fvSolution.cxx"

%include "src/finiteVolume/fields/volFields/volFieldsFwd.hxx"
%include "src/finiteVolume/fields/surfaceFields/surfaceFieldsFwd.hxx"

%{
    #include "surfaceInterpolation.H"
%}

%include "surfaceInterpolation.H"


//---------------------------------------------------------------------------
#endif

%{
    #include "vtkFoamInterfaces.H"
%}

%include "src/OpenFOAM/db/typeInfo/className.hxx"

%include "src/finiteVolume/fields/volFields/volScalarField.cxx"

%include "src/finiteVolume/fields/volFields/volVectorField.cxx"

%include "vtkFoamInterface.H"


//--------------------------------------------------------------------------------------
%template( volScalarFieldSource ) Foam::vtkFoamInterface< Foam::scalar >;


//--------------------------------------------------------------------------------------
%template( volVectorFieldSource ) Foam::vtkFoamInterface< Foam::vector >;


//--------------------------------------------------------------------------------------

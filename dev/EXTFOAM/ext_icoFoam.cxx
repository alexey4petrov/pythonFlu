%module(directors="1") ext_icoFoam

%include "ext/common/OpenFOAM/shared_ptr/shared_ptr_Time.cxx"
%include "ext/common/finiteVolume/shared_ptr/shared_ptr_fvMesh.cxx"
%include "ext/common/finiteVolume/shared_ptr/shared_ptr_volScalarField.cxx"
%include "ext/common/OpenFOAM/shared_ptr/shared_ptr_IOdictionary.cxx"
%include "ext/common/finiteVolume/shared_ptr/shared_ptr_volVectorField.cxx"
%include "ext/common/finiteVolume/shared_ptr/shared_ptr_surfaceScalarField.cxx"
%include "ext/common/OpenFOAM/shared_ptr/shared_ptr_dimensionedScalar.cxx"

%{
#include "ext_icoFoam.hpp"
%}

%feature("director") t_get_time_base;
%feature("director") t_get_mesh_base;
%feature("director") t_get_fields_base;
%feature("director") t_piso_controls_base;

%include "ext_icoFoam.hpp"


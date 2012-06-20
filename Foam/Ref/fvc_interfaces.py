## pythonFlu - Python wrapping for OpenFOAM C++ API
## Copyright (C) 2010- Alexey Petrov
## Copyright (C) 2009-2010 Pebble Bed Modular Reactor (Pty) Limited (PBMR)
## 
## This program is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
## 
## You should have received a copy of the GNU General Public License
## along with this program.  If not, see <http://www.gnu.org/licenses/>.
## 
## See http://sourceforge.net/projects/pythonflu
##
## Author : Alexey PETROV, Andrey SIMURZIN
##


#--------------------------------------------------------------------------------------
attr2interface={ 'ddt' : 'Foam.src.finiteVolume.finiteVolume.fvc.fvcDdt.fvc_ddt',
                 'ddtPhiCorr' : 'Foam.src.finiteVolume.finiteVolume.fvc.fvcDdt.fvc_ddtPhiCorr',
                 'DDt' : 'Foam.src.finiteVolume.finiteVolume.fvc.fvcD_Dt.fvc_DDt',
                 'div' : 'Foam.src.finiteVolume.finiteVolume.fvc.fvcDiv.fvc_div',
                 'grad' :'Foam.src.finiteVolume.finiteVolume.fvc.fvcGrad.fvc_grad',
                 'snGrad' :'Foam.src.finiteVolume.finiteVolume.fvc.fvcSnGrad.fvc_snGrad',
                 'reconstruct' :'Foam.src.finiteVolume.finiteVolume.fvc.fvcReconstruct.fvc_reconstruct',
                 'interpolate' : 'Foam.src.finiteVolume.interpolation.surfaceInterpolation.surfaceInterpolate.interpolate',
                 'volumeIntegrate' : 'Foam.src.finiteVolume.finiteVolume.fvc.fvcVolumeIntegrate.fvc_volumeIntegrate',
                 'domainIntegrate' : 'Foam.src.finiteVolume.finiteVolume.fvc.fvcVolumeIntegrate.fvc_domainIntegrate',
                 'surfaceIntegrate' : 'Foam.src.finiteVolume.finiteVolume.fvc.fvcSurfaceIntegrate.fvc_surfaceIntegrate',
                 'surfaceSum' : 'Foam.src.finiteVolume.finiteVolume.fvc.fvcSurfaceIntegrate.fvc_surfaceSum',
                 'laplacian' : 'Foam.src.finiteVolume.finiteVolume.fvc.fvcLaplacian.fvc_laplacian',
                 'meshPhi' : 'Foam.src.finiteVolume.finiteVolume.fvc.fvcMeshPhi.fvc_meshPhi',
                 'makeRelative' : 'Foam.src.finiteVolume.finiteVolume.fvc.fvcMeshPhi.fvc_makeRelative',
                 'makeAbsolute' : 'Foam.src.finiteVolume.finiteVolume.fvc.fvcMeshPhi.fvc_makeAbsolute',
                 'flux' : 'Foam.src.finiteVolume.finiteVolume.fvc.fvcFlux.fvc_flux',
                 'Sp' : 'Foam.src.finiteVolume.finiteVolume.fvc.fvcSup.fvc_Sp',
                 'Su' : 'Foam.src.finiteVolume.finiteVolume.fvc.fvcSup.fvc_Su',
                 'SuSp' : 'Foam.src.finiteVolume.finiteVolume.fvc.fvcSup.fvc_SuSp',
                 'smooth' : 'Foam.src.finiteVolume.finiteVolume.fvc.fvcSmooth.fvcSmooth.smooth',
                 'spread' : 'Foam.src.finiteVolume.finiteVolume.fvc.fvcSmooth.fvcSmooth.spread',
                 'sweep' : 'Foam.src.finiteVolume.finiteVolume.fvc.fvcSmooth.fvcSmooth.sweep'
                 }
                 


#!/usr/bin/env python

#--------------------------------------------------------------------------------------
## VulaSHAKA (Simultaneous Neutronic, Fuel Performance, Heat And Kinetics Analysis)
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
## See https://vulashaka.svn.sourceforge.net/svnroot/vulashaka
##
## Author : Alexey PETROV
##


#-----------------------------------------------------------------
def createSolidMeshes( rp, runTime ):
    
    from Foam.finiteVolume import PtrList_fvMesh, fvMesh
    solidRegions = PtrList_fvMesh( rp.solidRegionNames().size() )
    
    from Foam.OpenFOAM import word, fileName, IOobject
    for index in range( solidRegions.size() ):
        from Foam.OpenFOAM import ext_Info, nl
        ext_Info()<< "Create solid mesh for region " << rp.solidRegionNames()[ index ] \
            << " for time = " << runTime.timeName() << nl << nl
        
        solidRegions.ext_set(index, fvMesh( IOobject ( word( rp.solidRegionNames()[ index ] ),
                                                       fileName( runTime.timeName() ),
                                                       runTime,
                                                       IOobject.MUST_READ ) ) )
        pass

    return solidRegions


#---------------------------------------------------------------------
def createSolidField( solidRegions, runTime ):

    #Initialise solid field pointer lists
    from Foam.finiteVolume import PtrList_volScalarField, volScalarField
    rhos = PtrList_volScalarField( solidRegions.size() )
    cps = PtrList_volScalarField( solidRegions.size() )
    rhosCps = PtrList_volScalarField( solidRegions.size() )
    Ks = PtrList_volScalarField( solidRegions.size() )
    Ts = PtrList_volScalarField( solidRegions.size() )
    
    from Foam.OpenFOAM import ext_Info, nl
    
    #Populate solid field pointer lists    
    from Foam.OpenFOAM import word, IOobject, fileName
    for index in range( solidRegions.size() ):
        ext_Info()<< "*** Reading solid mesh thermophysical properties for region " \
            << solidRegions[ index ].name() << nl << nl

        ext_Info()<< "    Adding to rhos\n" << nl
        rhos.ext_set( index, volScalarField( IOobject ( word( "rho" ), 
                                                        fileName( runTime.timeName() ), 
                                                        solidRegions[ index ], 
                                                        IOobject.MUST_READ, 
                                                        IOobject.AUTO_WRITE ),
                                             solidRegions[ index ] )  )
        
        ext_Info()<< "    Adding to cps\n" << nl
        cps.ext_set( index, volScalarField( IOobject( word( "cp" ),
                                                      fileName( runTime.timeName() ),
                                                      solidRegions[ index ],
                                                      IOobject.MUST_READ,
                                                      IOobject.AUTO_WRITE ),
                                            solidRegions[ index ] ) )
        
        rhosCps.ext_set( index, volScalarField( word( "rhosCps" ), rhos[ index ] * cps[ index ]  ) )
        
        ext_Info()<< "    Adding to Ks\n" << nl
        Ks.ext_set( index, volScalarField( IOobject( word( "K" ),
                                                     fileName( runTime.timeName() ),
                                                     solidRegions[ index ],
                                                     IOobject.MUST_READ,
                                                     IOobject.AUTO_WRITE ),
                                           solidRegions[ index ] ) )
        
        ext_Info()<< "    Adding to Ts\n" << nl
       
        Ts.ext_set( index, volScalarField( IOobject( word( "T" ),
                                                     fileName( runTime.timeName() ),
                                                     solidRegions[ index ],
                                                     IOobject.MUST_READ,
                                                     IOobject.AUTO_WRITE ),
                                           solidRegions[ index ] ) )
   
    return rhos, cps, rhosCps, Ks, Ts


#-----------------------------------------------------------------------------------------------------
def readSolidMultiRegionPIMPLEControls( mesh ):
    from Foam.OpenFOAM import word
    pimple = mesh.solutionDict().subDict( word( "PIMPLE" ) )
    nNonOrthCorr = pimple.lookupOrDefault( word( "nNonOrthogonalCorrectors" ), 0 )
    
    return pimple, nNonOrthCorr


#-------------------------------------------------------------------------------------------------------
def readSolidTimeControls( runTime ):
    from Foam.OpenFOAM import word 
    maxDi = runTime.controlDict().lookupOrDefault( word( "maxDi" ) , 10.0 )
    
    return maxDi


#-------------------------------------------------------------------------------------------------------
def solidRegionDiffNo( mesh, runTime, Cprho, K ):
    DiNum = 0.0
    meanDiNum = 0.0

    #- Can have fluid domains with 0 cells so do not test.
    if mesh.nInternalFaces():
       from Foam import fvc
       KrhoCpbyDelta = mesh.deltaCoeffs() * fvc.interpolate( K ) / fvc.interpolate(Cprho);
       DiNum = KrhoCpbyDelta.internalField().max() * runTime.deltaT().value()
       meanDiNum = KrhoCpbyDelta.average().value() * runTime.deltaT().value()
       pass
    
    from Foam.OpenFOAM import ext_Info, nl
    ext_Info() << "Region: " << mesh.name() << " Diffusion Number mean: " << meanDiNum << " max: " << DiNum << nl

    return DiNum


#-------------------------------------------------------------------------------------------------------
def solidRegionDiffusionNo( solidRegions, runTime, rhosCps, Ks ):
    from Foam.OpenFOAM import GREAT
    DiNum = -GREAT
    
    for regionI in range( solidRegions.size() ):
        DiNum = max( solidRegionDiffNo( solidRegions[ regionI ], runTime, rhosCps[ regionI ], Ks[ regionI ] ), DiNum )
        pass
    
    return DiNum

#-------------------------------------------------------------------------------------------------------
def setRegionSolidFields( i, solidRegions, rhos, cps, Ks, Ts ):
    mesh = solidRegions[ i ]
    rho = rhos[ i ]
    cp = cps[ i ]
    K = Ks[ i ]
    T = Ts[ i ]
    
    return mesh, rho, cp, K, T


#-------------------------------------------------------------------------------------------------------
def solveSolid( mesh, rho, cp, K, T, nNonOrthCorr ):
    for index in range( nNonOrthCorr + 1 ):
       from Foam import fvm
       TEqn = fvm.ddt( rho * cp, T ) - fvm.laplacian( K, T )
       TEqn.relax()
       TEqn.solve()
       pass
    from Foam.OpenFOAM import ext_Info, nl   
    ext_Info()<< "Min/max T:" << T.ext_min() << ' ' << T.ext_max() << nl
    
    pass

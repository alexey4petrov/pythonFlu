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
## Author : Alexey PETROV
##


#------------------------------------------------------------------------------
def readSIMPLEControls_010401_dev( mesh ):
    from Foam.OpenFOAM import Switch
    from Foam.OpenFOAM import word
   
    simple = mesh.solutionDict().subDict( word( "SIMPLE" ) )
    
    from Foam.OpenFOAM import readInt
    nNonOrthCorr = 0
    if ( simple.found( word( "nNonOrthogonalCorrectors" ) ) ):
       nNonOrthCorr = readInt(simple.lookup( word( "nNonOrthogonalCorrectors" ) ) )
       pass
 
    momentumPredictor = True
    if ( simple.found( word( "momentumPredictor" ) ) ):
       momentumPredictor = Switch(simple.lookup( word( "momentumPredictor" ) ) )
       pass
 
    fluxGradp = False
    if ( simple.found( word( "fluxGradp" ) ) ):
       fluxGradp = Switch( simple.lookup( word( "fluxGradp" ) ) )
       pass
 
    transSonic = False
    if ( simple.found( word( "transSonic" ) ) ):
       transSonic = Switch( simple.lookup( word( "transSonic" ) ) )
       pass
 
    return simple, nNonOrthCorr, momentumPredictor, fluxGradp, transSonic


#--------------------------------------------------------------------------------
def readSIMPLEControls_010500( mesh ):
    from Foam.OpenFOAM import Switch
    from Foam.OpenFOAM import word
    
    simple = mesh.solutionDict().subDict( word( "SIMPLE" ) )
    
    from Foam.OpenFOAM import readInt
    nNonOrthCorr = 0
    if ( simple.found( word( "nNonOrthogonalCorrectors" ) ) ):
       nNonOrthCorr = readInt(simple.lookup( word( "nNonOrthogonalCorrectors" ) ) )
       pass
 
    momentumPredictor = True
    if ( simple.found( word( "momentumPredictor" ) ) ):
       momentumPredictor = Switch(simple.lookup( word( "momentumPredictor" ) ) )
       pass
 
    fluxGradp = False
    if ( simple.found( word( "fluxGradp" ) ) ):
       fluxGradp = Switch( simple.lookup( word( "fluxGradp" ) ) )
       pass
 
    transonic = False
    if ( simple.found( word( "transSonic" ) ) ):
       transonic = Switch( simple.lookup( word( "transSonic" ) ) )
       pass

    return simple, nNonOrthCorr, momentumPredictor, fluxGradp, transonic


#--------------------------------------------------------------------------------
def readSIMPLEControls_010500_dev( mesh ):
    from Foam.OpenFOAM import Switch
    from Foam.OpenFOAM import word
    
    simple = mesh.solutionDict().subDict( word( "SIMPLE" ) )
    
    from Foam.OpenFOAM import readInt
    nNonOrthCorr = 0
    if ( simple.found( word( "nNonOrthogonalCorrectors" ) ) ):
       nNonOrthCorr = readInt(simple.lookup( word( "nNonOrthogonalCorrectors" ) ) )
       pass
 
    momentumPredictor = True
    if ( simple.found( word( "momentumPredictor" ) ) ):
       momentumPredictor = Switch(simple.lookup( word( "momentumPredictor" ) ) )
       pass
 
    fluxGradp = False
    if ( simple.found( word( "fluxGradp" ) ) ):
       fluxGradp = Switch( simple.lookup( word( "fluxGradp" ) ) )
       pass
 
    transonic = False
    if ( simple.found( word( "transSonic" ) ) ):
       transonic = Switch( simple.lookup( word( "transSonic" ) ) )
       pass

    return simple, nNonOrthCorr, momentumPredictor, fluxGradp, transonic


#--------------------------------------------------------------------------------
def readSIMPLEControls_010600( mesh ):
    from Foam.OpenFOAM import Switch
    from Foam.OpenFOAM import word
    
    simple = mesh.solutionDict().subDict( word( "SIMPLE" ) )
    
    nNonOrthCorr = simple.lookupOrDefault( word( "nNonOrthogonalCorrectors" ), 0 )

    momentumPredictor = simple.lookupOrDefault( word( "momentumPredictor" ), Switch( True ) )

    fluxGradp = simple.lookupOrDefault( word( "fluxGradp" ), Switch( False ) )

    transonic = simple.lookupOrDefault( word( "transonic" ), Switch( False ) )
       
    return simple, nNonOrthCorr, momentumPredictor, fluxGradp, transonic


#--------------------------------------------------------------------------------
def readSIMPLEControls_010600_dev( mesh ):
    from Foam.OpenFOAM import Switch
    from Foam.OpenFOAM import word
    
    simple = mesh.solutionDict().subDict( word( "SIMPLE" ) )
    
    nNonOrthCorr = simple.lookupOrDefault( word( "nNonOrthogonalCorrectors" ), 0 )

    momentumPredictor = simple.lookupOrDefault( word( "momentumPredictor" ), Switch( True ) )

    fluxGradp = simple.lookupOrDefault( word( "fluxGradp" ), Switch( False ) )

    transonic = simple.lookupOrDefault( word( "transonic" ), Switch( False ) )
       
    return simple, nNonOrthCorr, momentumPredictor, fluxGradp, transonic


#--------------------------------------------------------------------------------
def readSIMPLEControls_010700( mesh ):
    from Foam.OpenFOAM import Switch
    from Foam.OpenFOAM import word
    
    simple = mesh.solutionDict().subDict( word( "SIMPLE" ) )
    
    nNonOrthCorr = simple.lookupOrDefault( word( "nNonOrthogonalCorrectors" ), 0 )

    momentumPredictor = simple.lookupOrDefault( word( "momentumPredictor" ), Switch( True ) )

    transonic = simple.lookupOrDefault( word( "transonic" ), Switch( False ) )
       
    return simple, nNonOrthCorr, momentumPredictor, transonic

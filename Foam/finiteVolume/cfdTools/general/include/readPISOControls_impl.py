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
def readPISOControls_010401_dev( mesh ):
    from Foam.OpenFOAM import dictionary, readInt, Switch, word

    piso = dictionary( mesh.solutionDict().subDict( word( "PISO" ) ) )
    nCorr = readInt( piso.lookup( word( "nCorrectors" ) ) )

    nNonOrthCorr = 0
    
    if piso.found( word( "nNonOrthogonalCorrectors" ) ) :
       nNonOrthCorr = readInt( piso.lookup( word( "nNonOrthogonalCorrectors" ) ) )
       pass

    momentumPredictor = True
    if piso.found( word( "momentumPredictor" ) ) :
       momentumPredictor = Switch( piso.lookup( word( "momentumPredictor" ) ) )
       pass

    fluxGradp = False
    if piso.found( word( "fluxGradp" ) ):
       fluxGradp = Switch(piso.lookup( word( "fluxGradp" ) ) )
       pass   
 
    transSonic = False
    if piso.found( word( "transonic" ) ) :
       transSonic = Switch( piso.lookup( word( "transonic" ) ) )
       pass

    nOuterCorr = 1
    if piso.found( word( "nOuterCorrectors" ) ) :
       nOuterCorr = readInt( piso.lookup( word( "nOuterCorrectors" ) ) )
       pass
    
    return piso, nCorr, nNonOrthCorr, momentumPredictor, transSonic, nOuterCorr


#------------------------------------------------------------------------------------
def readPISOControls_010500( mesh ):
    from Foam.OpenFOAM import dictionary, readInt, Switch, word

    piso = dictionary( mesh.solutionDict().subDict( word( "PISO" ) ) )

    nCorr = readInt( piso.lookup( word( "nCorrectors" ) ) )

    nNonOrthCorr = 0;
    if piso.found( word( "nNonOrthogonalCorrectors" ) ) :
       nNonOrthCorr = readInt( piso.lookup( word( "nNonOrthogonalCorrectors" ) ) )
       pass
    
    momentumPredictor = True;
    if piso.found( word( "momentumPredictor" ) ) :
       momentumPredictor = Switch( piso.lookup( word( "momentumPredictor" ) ) )
       pass
   
    transonic = False;
    if piso.found( word( "transonic" ) ) :
       transonic = Switch( piso.lookup( word( "transonic" ) ) )
       pass

    nOuterCorr = 1;
    if piso.found( word( "nOuterCorrectors" ) ) :
       nOuterCorr = readInt( piso.lookup( word( "nOuterCorrectors" ) ) )
       pass
    
    ddtPhiCorr = False
    if piso.found( word( "ddtPhiCorr" ) ) :
       ddtPhiCorr = Switch( piso.lookup( word( "ddtPhiCorr" ) ) )
       pass
    
    
    return piso, nCorr, nNonOrthCorr, momentumPredictor, transonic, nOuterCorr, ddtPhiCorr


#------------------------------------------------------------------------------------
def readPISOControls_010500_dev( mesh ):
    from Foam.OpenFOAM import dictionary, readInt, Switch, word

    piso = dictionary( mesh.solutionDict().subDict( word( "PISO" ) ) )

    nCorr = readInt( piso.lookup( word( "nCorrectors" ) ) )

    nNonOrthCorr = 0;
    if piso.found( word( "nNonOrthogonalCorrectors" ) ) :
       nNonOrthCorr = readInt( piso.lookup( word( "nNonOrthogonalCorrectors" ) ) )
       pass
    
    momentumPredictor = True;
    if piso.found( word( "momentumPredictor" ) ) :
       momentumPredictor = Switch( piso.lookup( word( "momentumPredictor" ) ) )
       pass
   
    transonic = False;
    if piso.found( word( "transonic" ) ) :
       transonic = Switch( piso.lookup( word( "transonic" ) ) )
       pass

    nOuterCorr = 1;
    if piso.found( word( "nOuterCorrectors" ) ) :
       nOuterCorr = readInt( piso.lookup( word( "nOuterCorrectors" ) ) )
       pass
    
    ddtPhiCorr = False
    if piso.found( word( "ddtPhiCorr" ) ) :
       ddtPhiCorr = Switch( piso.lookup( word( "ddtPhiCorr" ) ) )
       pass
    
    
    return piso, nCorr, nNonOrthCorr, momentumPredictor, transonic, nOuterCorr, ddtPhiCorr


#---------------------------------------------------------------------------------
def readPISOControls_010600( mesh ):
    from Foam.OpenFOAM import dictionary, readInt, Switch, word

    piso = dictionary( mesh.solutionDict().subDict( word( "PISO" ) ) )
    nCorr = readInt( piso.lookup( word( "nCorrectors" ) ) )
    
    nNonOrthCorr = piso.lookupOrDefault( word( "nNonOrthogonalCorrectors" ), 0 )
       
    momentumPredictor = piso.lookupOrDefault( word( "momentumPredictor" ), Switch( True ) )
      
    transonic = piso.lookupOrDefault( word( "transonic" ), Switch( False ) )
      
    nOuterCorr = piso.lookupOrDefault( word( "nOuterCorrectors" ), 1 )

    return piso, nCorr, nNonOrthCorr, momentumPredictor, transonic, nOuterCorr


#---------------------------------------------------------------------------------
def readPISOControls_010600_dev( mesh ):
    from Foam.OpenFOAM import dictionary, readInt, Switch, word

    piso = dictionary( mesh.solutionDict().subDict( word( "PISO" ) ) )
    nCorr = readInt( piso.lookup( word( "nCorrectors" ) ) )
    
    nNonOrthCorr = piso.lookupOrDefault( word( "nNonOrthogonalCorrectors" ), 0 )
       
    momentumPredictor = piso.lookupOrDefault( word( "momentumPredictor" ), Switch( True ) )
      
    transonic = piso.lookupOrDefault( word( "transonic" ), Switch( False ) )
      
    nOuterCorr = piso.lookupOrDefault( word( "nOuterCorrectors" ), 1 )

    return piso, nCorr, nNonOrthCorr, momentumPredictor, transonic, nOuterCorr


#---------------------------------------------------------------------------------

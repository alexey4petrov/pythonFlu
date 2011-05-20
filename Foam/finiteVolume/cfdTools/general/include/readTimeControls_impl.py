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


#---------------------------------------------------------------------------
def readTimeControls_010401_dev( runTime ):
    from Foam.OpenFOAM import Switch, word, readScalar, GREAT
    
    adjustTimeStep = Switch( runTime.controlDict().lookup( word( "adjustTimeStep" ) ) )
    maxCo = readScalar( runTime.controlDict().lookup( word( "maxCo" ) ) )
    
    maxDeltaT = GREAT
    if runTime.controlDict().found( word( "maxDeltaT" ) ):
       maxDeltaT = readScalar( runTime.controlDict().lookup( word( "maxDeltaT" ) ) )
       pass

    return adjustTimeStep, maxCo, maxDeltaT


#---------------------------------------------------------------------------
def readTimeControls_010600( runTime ):
    from Foam.OpenFOAM import Switch, word, readScalar, GREAT
    
    adjustTimeStep = Switch( runTime.controlDict().lookup( word( "adjustTimeStep" ) ) )
    maxCo = readScalar( runTime.controlDict().lookup( word( "maxCo" ) ) )
    
    maxDeltaT = runTime.controlDict().lookupOrDefault( word( "maxDeltaT" ), GREAT, 0, 1 )

    return adjustTimeStep, maxCo, maxDeltaT


#---------------------------------------------------------------------------
def readTimeControls_010600_dev( runTime ):
    from Foam.OpenFOAM import Switch, word, readScalar, GREAT
    
    adjustTimeStep = Switch( runTime.controlDict().lookup( word( "adjustTimeStep" ) ) )
    maxCo = readScalar( runTime.controlDict().lookup( word( "maxCo" ) ) )
    
    maxDeltaT = runTime.controlDict().lookupOrDefault( word( "maxDeltaT" ), GREAT, 0, 1 )

    return adjustTimeStep, maxCo, maxDeltaT


#---------------------------------------------------------------------------

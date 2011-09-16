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
def createTime_010401_dev( args ):
    from Foam.OpenFOAM import ext_Info, nl
    ext_Info() << "Create time\n" << nl
    
    from Foam.OpenFOAM import TimeHolder, Time
    from Foam.OpenFOAM import argList
    
    runTime = TimeHolder( Time.controlDictName.fget(),
                    args.rootPath(),
                    args.caseName() )
    print repr( runTime )   
    return runTime


#---------------------------------------------------------------------------------------------
def createTime_020000( args ):
    from Foam.OpenFOAM import ext_Info, nl
    ext_Info() << "Create time\n" << nl
    
    from Foam.OpenFOAM import Time, TimeHolder

    runTime = TimeHolder( Time.controlDictName.fget(), args )

    return runTime


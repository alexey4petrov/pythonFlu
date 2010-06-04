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


#---------------------------------------------------------------------------
def createTime( rootPath, caseName ) :
    print "Create time\n"
    
    from Foam.OpenFOAM import Time, fileName
    runTime = Time( Time.controlDictName.fget(),
                    fileName( rootPath ),
                    fileName( caseName ) )
    
    return runTime
                    

#--------------------------------------------------------------------------------------
def copy_geometric_field( the_field_factory, the_source_field, the_source_mesh, the_target_mesh ) :
    from Foam.OpenFOAM import OStringStream
    an_ostream = OStringStream()
    an_ostream << the_source_field
        
    from Foam.OpenFOAM import IStringStream
    an_istream = IStringStream( an_ostream.str() )

    from Foam.finiteVolume import volScalarField
    from Foam.OpenFOAM import IOobject, word, fileName
    a_result = the_field_factory( IOobject( the_source_field.name(),
                                            fileName( the_target_mesh.time().timeName() ),
                                            the_target_mesh,
                                            IOobject.NO_READ,
                                            IOobject.AUTO_WRITE
                                            ),
                                  the_target_mesh,
                                  an_istream
                                  )
    return a_result


#---------------------------------------------------------------------------

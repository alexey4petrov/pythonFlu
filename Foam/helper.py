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
class TLoadHelper( object ):
    def __init__( self, the_dict ):
        self._dict = the_dict
        pass
    
    def __getattr__( self, the_attr ):
        if not self._dict.has_key( the_attr ):
            raise AttributeError( "There is no \"%s\" attribute in man" %the_attr)
            pass
        
        a_result = self._dict[ the_attr ]
        if type( a_result ) == str:
            an_interface =a_result.rpartition('.')[ 2 ]
            #print an_interface
            an_interface_path = a_result.rpartition('.')[ 0 ]
            #print an_interface_path
            exec "from %s import %s as a_result" %( an_interface_path, an_interface )
            pass
        exec "self.%s = a_result" %the_attr        
        
        return a_result
    pass


#--------------------------------------------------------------------------------------
class TManLoadHelper( TLoadHelper ):
    def __call__( self, theExpr, theDeps ):
       result = theExpr.holder( theDeps )

       theExpr.this.disown()
       return result
    pass
    pass


#--------------------------------------------------------------------------------------


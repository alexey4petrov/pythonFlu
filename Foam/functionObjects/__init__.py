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


#----------------------------------------------------------------------------------------       
def getfunctionObjectConstructorToTableBase() :
    aClass = None

    from Foam.OpenFOAM import TConstructorToTableCounter_functionObject
    aCounter = TConstructorToTableCounter_functionObject.counter()
    aClassName = "functionObjectConstructorToTableBase_%d" % aCounter
    anExpression = "from Foam.OpenFOAM import %s; aClass = %s" % ( aClassName, aClassName )
    exec anExpression

    return aClass


#----------------------------------------------------------------------------------------       
from Foam.OpenFOAM import functionObject
class functionObject_pythonFlu( functionObject ):
    @staticmethod
    def type(): 
        from Foam.OpenFOAM import word
        return word( 'pythonFlu' )

    def __init__( self, the_name, the_time, the_dict ) :
        self._time = the_time
        self._dict = the_dict
        
        self._startCode = ''
        self._writeCode = ''
        self._executeCode = ''
        self._executionFrame = {}

        functionObject.__init__( self, the_name )
        self.read( self._dict )
        pass

    def start( self ) : 
        self._executionFrame.update( { 'runTime' : self._time } )
        # print "startCode = \"%s\" in %s" % ( self._startCode, self._executionFrame )
        exec self._startCode in self._executionFrame

        return True

    def execute( self ): 
        # print "executeCode = \"%s\"" % ( self._executeCode )
        exec self._executeCode in self._executionFrame

        return True

    def write( self ) :
        # print "writeCode = \"%s\"" % ( self._writeCode )
        exec self._writeCode in self._executionFrame

        return True

    def read( self, the_dict ): 
        self._startCode = self._readCode( the_dict, 'start' )
        self._writeCode = self._readCode( the_dict, 'write' )
        self._executeCode = self._readCode( the_dict, 'execute' )

        return True

    def _readCode( self, the_dict, the_prefix ) :
        from Foam.OpenFOAM import word
        a_code_prefix = word( the_prefix + 'Code' )
        an_is_string = the_dict.found( a_code_prefix )

        from Foam.OpenFOAM import word
        a_file_prefix = word( the_prefix + 'File' )
        an_is_file = the_dict.found( a_file_prefix )

        if an_is_string and an_is_file :
            raise AssertionError()

        if not an_is_string and not an_is_file :
            raise AssertionError()
        
        a_string = None
        if an_is_string :
            from Foam.src.OpenFOAM.primitives.strings.string import string
            a_string = str( string( the_dict.lookup( a_code_prefix ) ) )
        else:
            from Foam.src.OpenFOAM.primitives.strings.string import string
            a_filename = str( string( the_dict.lookup( a_file_prefix ) ) )
            import os.path
            if not os.path.isfile( a_filename ) :
                raise AssertionError()
            a_file = open( a_filename )
            a_string = a_file.readlines().join( '\n' )
            pass
        
        return a_string

    pass


#----------------------------------------------------------------------------------------       
class functionObjectConstructorToTable_pythonFlu( getfunctionObjectConstructorToTableBase() ):
    def __init__( self ):
        aBaseClass = self.__class__.__bases__[ 0 ]
        aBaseClass.__init__( self )
        
        aBaseClass.init( self, self, functionObject_pythonFlu.type() )
        pass
    
    def _new_( self, the_name, the_time, the_dict ):
        obj = functionObject_pythonFlu( the_name, the_time, the_dict )

        from Foam.OpenFOAM import autoPtr_functionObject
        return autoPtr_functionObject( obj )
            
    pass

      
#----------------------------------------------------------------------------------------------------------
pythonFlu_functionObjectConstructorToTable = functionObjectConstructorToTable_pythonFlu()


#----------------------------------------------------------------------------------------------------------

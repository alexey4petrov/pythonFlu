import Foam.functionObjects
from Foam import ref, man

import unittest


#------------------------------------------------------------------------------------
class testFunctionObject(unittest.TestCase):
    def setUp(self):
        import os
        print os.path.abspath( os.path.curdir )
        argv=["test","-case",os.path.join( os.environ[ "PYTHONFLU_ROOT_DIR" ], "unittest/testFunctionObject" ) ]
        args = ref.setRootCase( len(argv), argv )
        self.runTime = man.createTime( args )

    def testCycle(self):
        while self.runTime.loop():
            pass


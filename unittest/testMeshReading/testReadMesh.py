from Foam.OpenFOAM.include import setRootCase
from Foam.OpenFOAM.include import createTime
from Foam.OpenFOAM.include import createMesh

import testMeshReading as me

import unittest

class testMesh(unittest.TestCase):
    def setUp(self):
        argv=["test","-case",me.pitzDir]
        args = setRootCase( len(argv), argv )
        runTime=createTime(args)
        self.mesh = createMesh( runTime )

    def testMeshCellSize(self):
        self.assertEqual(self.mesh.C().size(),12225)

    def testMeshPointSize(self):
        self.assertEqual(self.mesh.points().size(),25012)

    def testMeshBoundarySize(self):
        self.assertEqual(self.mesh.boundaryMesh().size(),5)

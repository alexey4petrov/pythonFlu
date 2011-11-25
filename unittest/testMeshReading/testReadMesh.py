from Foam import ref, man
import testMeshReading as me

import unittest

class testMesh(unittest.TestCase):
    def setUp(self):
        argv=["test","-case",me.pitzDir]
        args = ref.setRootCase( len(argv), argv )
        runTime = man.createTime(args)
        self.mesh = man.createMesh( runTime )

    def testMeshCellSize(self):
        self.assertEqual(self.mesh.C().size(),12225)

    def testMeshPointSize(self):
        self.assertEqual(self.mesh.points().size(),25012)

    def testMeshBoundarySize(self):
        self.assertEqual(self.mesh.boundaryMesh().size(),5)

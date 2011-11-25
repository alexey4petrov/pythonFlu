from Foam.OpenFOAM import scalarList
from nose.tools import ok_,eq_,nottest,raises

def testListCreation():
    l=scalarList(4,1.)
    eq_(len(l),4)
    eq_(l[2],1.)
    
@raises(NotImplementedError)
def testListCreationFails():
    l=scalarList(4,1)

@raises(TypeError)
def testListIteration():
    l=scalarList(4,1.)
    for i in l:
        eq_(i,1.)

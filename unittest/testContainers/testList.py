from Foam import ref
from nose.tools import ok_,eq_,nottest,raises

def testListCreation():
    l=ref.scalarList(4,1.)
    eq_(len(l),4)
    eq_(l[2],1.)
    
@raises(NotImplementedError)
def testListCreationFails():
    l=ref.scalarList(4,1)

@raises(TypeError)
def testListIteration():
    l=ref.scalarList(4,1.)
    for i in l:
        eq_(i,1.)

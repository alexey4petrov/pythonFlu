from Foam.OpenFOAM import word
from nose.tools import ok_,eq_,raises

def testWordCreation():
    w=word("foo")
    eq_(len(w),3)

@raises(TypeError)
def testWordAddition():
    w1=word("foo")
    w2=word("foobar")
    w=w1+w2
    eq_(len(w),6)
    
def testWordSubscript():
    w=word("foo")
    eq_(w[1],'o')

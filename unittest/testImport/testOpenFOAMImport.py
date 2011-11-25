from nose.tools import ok_, raises

def testImport():
    ok_('Foam' not in dir())
    import Foam.OpenFOAM
    ok_('Foam' in dir())
    ok_('OpenFOAM' in dir(Foam))

def testRefFeature():
    from Foam import ref
    ok_(ref.word)

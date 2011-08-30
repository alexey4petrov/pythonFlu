from nose.tools import ok_

def testImport():
    ok_('Foam' not in dir())
    import Foam.OpenFOAM
    ok_('Foam' in dir())
    ok_('OpenFOAM' in dir(Foam))
    ok_('word' in dir(Foam.OpenFOAM))
    

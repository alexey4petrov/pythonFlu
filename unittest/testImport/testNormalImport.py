from nose.tools import ok_

def testImport():
    ok_('Foam' not in dir())
    import Foam
    ok_('Foam' in dir())
    

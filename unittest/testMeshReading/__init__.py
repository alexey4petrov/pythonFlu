from os import environ,path
import shutil

try:
    from subprocess import check_call,PIPE
except ImportError:
    from subprocess import call,PIPE
    
pitzDir=path.join("/tmp","pythonFluTestPitzDaily")

def teardown():
    #    print "Removing",pitzDir
    shutil.rmtree(pitzDir,ignore_errors=True)

def setup():
    teardown()
    #    print "Creating",pitzDir
    
    shutil.copytree(path.join(environ["FOAM_TUTORIALS"],
                              "incompressible",
                              "simpleFoam",
                              "pitzDaily"),
                    pitzDir)

    cmdLine=["blockMesh -case "+pitzDir]
    try:
        check_call(cmdLine,shell=True,stdout=PIPE)
    except NameError:
        call(cmdLine,shell=True,stdout=PIPE)

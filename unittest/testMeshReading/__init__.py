from os import environ,path
import shutil
from subprocess import check_call,PIPE

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
    
    check_call(["blockMesh -case "+pitzDir],shell=True,stdout=PIPE)

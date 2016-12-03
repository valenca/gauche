from subprocess import Popen,PIPE,STDOUT
from funcs.gravity import *

def runProcess(exe):
    p = Popen(exe.split(), stdout=PIPE, stderr=STDOUT)
    while(True):
        retcode = p.poll()
        line = p.stdout.read()
        yield line
        if(retcode is not None):
            break
 
def call(exe):
    print("CMD \'%s\':" % exe)
    ret = next(runProcess(exe)).decode('utf-8').strip("\n")
    print(ret.split("\n"))
    return ret


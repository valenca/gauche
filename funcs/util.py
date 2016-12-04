from subprocess import Popen,PIPE,STDOUT
from math import sqrt

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

def dist(x1, x2, y1, y2):
    return sqrt((x1-x2)**2+(y1-y2)**2)

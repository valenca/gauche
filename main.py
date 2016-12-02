#!/usr/bin/env python
 
from subprocess import Popen,PIPE,STDOUT
from sys import argv 
from math import floor
from time import sleep
from operator import sub

o = (1006, 1107)  #coords measured at the top left of the screen

GEO = {
        "video_top"   :[(68,  0, 32, 33), (80,  0, 20, 21), (50,  0, 50, 50)],
        "video_centre":[(10, 10, 80, 80), (25, 25, 50, 51), (33, 33, 32, 33)]
}[argv[1]]

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
                                                      
def relativeP(x):
    return (x[0] - o[0]) * 100 / d[0], (x[1] - o[1]) * 100 / d[1]

def absoluteP(x):
    return (x[0] * d[0] / 100) + o[0], (x[1] * d[1] / 100) + o[1]
                                                        
def relativeG(x):
    return x[0] * 100 / d[0], x[1] * 100 / d[1]
 
def absoluteG(x):
    return x[0] * d[0] / 100, x[1] * d[1] / 100

def closeEnough(x, y):
    for i in range(len(y)):
        c = max(map(abs, map(sub, x, y[i])))
        if c < 10:
            return i
    return -1

if __name__ == "__main__":

    d = call("xdotool getdisplaygeometry")
    
    d = list(map(int, d.split()))

    w = call("xdotool getwindowfocus")
    l = call("xdotool getwindowgeometry %s" % w)
    w, p, g = l.split("\n")

    w = int(w.split()[1])
    p = relativeP(tuple(map(int, p.split()[1].split(','))))
    g = relativeG(tuple(map(int, g.split()[1].split('x'))))
 
    k = tuple(map(int, map(floor, p + g)))

    print k

    t = closeEnough(k, GEO)

    if t == -1:
        print("gravity not found, defaulting to %s" % str(GEO[0]))
        k = GEO[0]
    else:
        print("gravity found!")
        k = GEO[(t + 1) % len(GEO)]

    p = absoluteP(k[:2])
    g = absoluteG(k[2:])
 

    l = call("xdotool windowsize %d %d %d --sync" % (w, g[0], g[1]))
    l = call("xdotool windowmove %d %d %d --sync" % (w, p[0], p[1]))
    sleep(0.02)
    l = call("xdotool mousemove --sync --window %s %d %d" % (w, g[0] // 2, g[1] // 2))


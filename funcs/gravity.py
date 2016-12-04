from math import floor
from time import sleep
from operator import sub

from funcs.util import *

def relativeP(x, d, o):
    return (x[0] - o[0]) * 100 / d[0], (x[1] - o[1]) * 100 / d[1]
         
def absoluteP(x, d, o):
    return (x[0] * d[0] / 100) + o[0], (x[1] * d[1] / 100) + o[1]
                   
def relativeG(x, d, o): 
    return x[0] * 100 / d[0], x[1] * 100 / d[1]

def absoluteG(x, d, o): 
    return x[0] * d[0] / 100, x[1] * d[1] / 100


def closeEnough(x, y):
    for i in range(len(y)):
        c = max(map(abs, map(sub, x, y[i])))
        if c < 10:
            return i
    return -1

def gravity(GEO, OFF):
    o = OFF

    d = call("xdotool getdisplaygeometry")
    d = list(map(int, d.split()))

    w = call("xdotool getwindowfocus")
    l = call("xdotool getwindowgeometry %s" % w)
    w, p, g = l.split("\n")

    w = int(w.split()[1])
    p = relativeP(tuple(map(int, p.split()[1].split(','))), d, o)
    g = relativeG(tuple(map(int, g.split()[1].split('x'))), d, o)
 
    k = tuple(map(int, map(round, p + g)))

    t = closeEnough(k, GEO)

    if t == -1:
        k = GEO[0]
        print("gravity not found, defaulting to %s" % str(k))
    else:
        k = GEO[(t + 1) % len(GEO)]
        print("gravity found, setting to %s" % str(k))

    p = absoluteP(k[:2], d, o)
    g = absoluteG(k[2:], d, o)
 

    l = call("xdotool windowsize %d %d %d --sync" % (w, g[0], g[1]))
    l = call("xdotool windowmove %d %d %d --sync" % (w, p[0], p[1]))
    sleep(0.02)
    l = call("xdotool mousemove %d %d" % (p[0] + g[0] / 2, p[1] + g[1] / 2 ))


#!/usr/bin/env python

#   For best performance remove window titles.
#   Install devilspie with the script: 
# 
#   (if (matches (application_name) ".*") (begin (undercorate)))
#
#   And run it on the background

from math import floor
from time import sleep
from operator import sub

from funcs.util import *

o = (1, 27)  #coords measured at the top left of the screen

def relativeP(x, d):
    return (x[0] - o[0]) * 100 / d[0], (x[1] - o[1]) * 100 / d[1]
         
def absoluteP(x, d):
    return (x[0] * d[0] / 100) + o[0], (x[1] * d[1] / 100) + o[1]
                   
def relativeG(x, d): 
    return x[0] * 100 / d[0], x[1] * 100 / d[1]

def absoluteG(x, d): 
    return x[0] * d[0] / 100, x[1] * d[1] / 100


def closeEnough(x, y):
    for i in range(len(y)):
        c = max(map(abs, map(sub, x, y[i])))
        if c < 10:
            return i
    return -1

def gravity(GEO):
    d = call("xdotool getdisplaygeometry")
    d = list(map(int, d.split()))

    w = call("xdotool getwindowfocus")
    l = call("xdotool getwindowgeometry %s" % w)
    w, p, g = l.split("\n")

    w = int(w.split()[1])
    p = relativeP(tuple(map(int, p.split()[1].split(','))), d)
    g = relativeG(tuple(map(int, g.split()[1].split('x'))), d)
 
    k = tuple(map(int, map(floor, p + g)))

    print(k)

    t = closeEnough(k, GEO)

    if t == -1:
        print("gravity not found, defaulting to %s" % str(GEO[0]))
        k = GEO[0]
    else:
        print("gravity found!")
        k = GEO[(t + 1) % len(GEO)]

    p = absoluteP(k[:2], d)
    g = absoluteG(k[2:], d)
 

    l = call("xdotool windowsize %d %d %d --sync" % (w, g[0], g[1]))
    l = call("xdotool windowmove %d %d %d --sync" % (w, p[0], p[1]))
    sleep(0.02)
    l = call("xdotool mousemove --sync --window %s %d %d" % (w, g[0] // 2, g[1] // 2))


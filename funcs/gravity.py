from math import floor
from time import sleep
from operator import sub,add

from funcs.util import *

def relativeP(x, display, offset):
    return (x[0] - offset[0]) * 100 / display[0], (x[1] - offset[1]) * 100 / display[1]
         
def absoluteP(x, display, offset):
    return (x[0] * display[0] / 100) + offset[0], (x[1] * display[1] / 100) + offset[1]
                   
def relativeG(x, display, offset): 
    return x[0] * 100 / display[0], x[1] * 100 / display[1]

def absoluteG(x, display, offset): 
    return x[0] * display[0] / 100, x[1] * display[1] / 100


def closeEnough(x, y):
    for i in range(len(y)):
        c = max(map(abs, map(sub, x, y[i])))
        if c < 10:
            return i
    return -1

def gravity(GEO):
    
    display,offset = getWorkingArea()
    window, pos, geo = call("xdotool getwindowgeometry %s" % call("xdotool getwindowfocus")).split("\n")
    
    window = int(window.split()[1])
    pos = relativeP(tuple(map(int, pos.split()[1].split(','))), display, offset)
    geo = relativeG(tuple(map(int, geo.split()[1].split('x'))), display, offset)
 
    grav = tuple(map(int, map(round, pos + geo)))

    tog = closeEnough(grav, GEO)

    if tog == -1:
        grav = GEO[0]
        print("gravity not found, defaulting to %s" % str(grav))
    else:
        grav = GEO[(tog + 1) % len(GEO)]
        print("gravity found, setting to %s" % str(grav))

    pos = absoluteP(grav[:2], display, offset)
    geo = absoluteG(grav[2:], display, offset)
 
    last = call("wmctrl -i -r %d -e 0,%d,%d,%d,%d" % (window, pos[0], pos[1], geo[0], geo[1]))
    last = call("xdotool mousemove %d %d" % (pos[0] + geo[0] / 2, pos[1] + geo[1] / 2 ))


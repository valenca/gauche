from operator import itemgetter
from itertools import groupby
from funcs.util import *


def travel(d):
    d = {
            "left"  : (1,  True),
            "right" : (1, False),
            "up"    : (2,  True),
            "down"  : (2, False)
            }[d]

    n = call("xdotool get_desktop")
    o = call("wmctrl -l").split("\n")

    o = [x.split() for x in o]

    l = [int(x[0],0) for x in o if x[1] == n]

    c = int(call("xdotool getwindowfocus"))

    if c in l:
        l.remove(c)

    c = [-1] + list(map(lambda x: int(x[2:]), call("xdotool getmouselocation").split()[:2]))
    
    a = []
    for w in l:
        o = call("xdotool getwindowgeometry %d" % w)
        o = o.split("\n")
        p = tuple(map(int, o[1].split()[1].split(",")))
        g = tuple(map(int, o[2].split()[1].split("x")))
        
        a.append([w, p[0]+(g[0]//2), p[1]+(g[1]//2)])
        
        if w == c:
            c = a[-1]

    for i in range(len(a)):
        a[i].append(dist(c[1],a[i][1],c[2],a[i][2]))
    
    a.sort(key=itemgetter(3))
   
    for i in range(len(a)):
        if abs(a[i][d[0]] - c[d[0]]) < 5: # Rounding threshold
            continue
        if (a[i][d[0]] > c[d[0]]) != d[1]:
            call("xdotool mousemove %d %d" % tuple(a[i][1:3]))
            break 



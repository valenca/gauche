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

    if c not in l:
        l.append(c)

    a = []
    for w in l:
        o = call("xdotool getwindowgeometry %d" % w)
        o = o.split("\n")
        p = tuple(map(int, o[1].split()[1].split(",")))
        g = tuple(map(int, o[2].split()[1].split("x")))
        
        a.append((w, p[0]+(g[0]//2), p[1]+(g[1]//2)))
    
        if w == c:
            c = a[-1]

    s=[]
    for k,v in groupby(sorted(a, key = itemgetter(d[0]), reverse=d[1]), itemgetter(d[0])):
        s.append((k, list(v)))
 
    for i in range(len(s)):
        if c[d[0]] == s[i][1][0][d[0]]:
            break

    if i + 1 < len(s):
        c = s[(i + 1) % len(s)][1][0]
    
    call("xdotool mousemove %d %d"% c[1:])

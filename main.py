#!/usr/bin/env python
 
from subprocess import *

d = (1600,900) #size of my monitor
o = (10,81)    #coords measured at the top left of the screen

def runProcess(exe):
    p = Popen(exe.split(" "), stdout=PIPE, stderr=STDOUT)
    while(True):
        retcode = p.poll() #returns None while subprocess is running
        line = p.stdout.read()
        yield line
        if(retcode is not None):
            break
                                            
def call(exe):
    print("CMD \'" + exe + "\':")
    ret = next(runProcess(exe)).decode('utf-8').strip("\n")
    print(ret.split("\n"))
    return ret
                                                      
def relativeP(x):
    return (x[0]-o[0])*100/d[0],(x[1]-o[1])*100/d[1]

def absoluteP(x):
    return (x[0]*d[0]/100)+o[0],(x[1]*d[1]/100)-o[1]
                                                        
def relativeG(x):
    return x[0]*100/d[0],x[1]*100/d[1]
 
def absoluteG(x):
   return x[0]*d[0]/100,x[1]*d[1]/100
        
if __name__ == "__main__":

    GEOS = [(68,0,32,33),(80,0,20,21),(50,0,50,50)]
 
    d = (1600,900-15)
 
    w = call("xdotool getwindowfocus")
    l = call("xdotool getwindowgeometry %s" % w)
    w,p,g = l.split("\n")

    w = int(w.split()[1])
    p = relativeP(tuple(map(int,p.split()[1].split(','))))
    g = relativeG(tuple(map(int,g.split()[1].split('x'))))
 
    k=p+g
 
    k=tuple(map(round,k))
 
    print(k)

    if k in GEOS:
         print("gravity found!")
         k = GEOS[(GEOS.index(k)+1) % len(GEOS)]
    else:
        print("gravity not found :(")
        k = GEOS[0]

    p = absoluteP(k[:2])
    g = absoluteG(k[2:])
 
    l = call("xdotool windowsize %d %d %d" % (w,g[0],g[1]))
    l = call("xdotool windowmove %d %d %d" % (w,p[0],p[1]))
    l = call("xdotool mousemove %d %d" % (-o[0]+p[0]+g[0]/2, 27+o[1]+p[1]+g[1]/2))



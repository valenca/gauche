#!/usr/bin/env python
 
from subprocess import *
from sys import argv 
from math import floor,ceil

d = (1600,900)  #size of my monitor
o = (  10, 80)  #coords measured at the top left of the screen

GEO = {
        "video_top"   :[(68, 0,32,33),(80, 0,20,21),(50, 0,50,50)],
        "video_centre":[(10,10,80,80),(25,25,50,51),(33,33,32,33)]
}[argv[1]]

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
    return (x[0]*d[0]/100)+o[0],(x[1]*d[1]/100)+o[1]
                                                        
def relativeG(x):
    return x[0]*100/d[0],x[1]*100/d[1]
 
def absoluteG(x):
   return x[0]*d[0]/100,x[1]*d[1]/100
        
if __name__ == "__main__":
 
    w = call("xdotool getwindowfocus")
    l = call("xdotool getwindowgeometry %s" % w)
    w,p,g = l.split("\n")

    w = int(w.split()[1])
    p = relativeP(tuple(map(int,p.split()[1].split(','))))
    g = relativeG(tuple(map(int,g.split()[1].split('x'))))
 
    k=p+g
 
    k=tuple(map(floor,k))
 
    print(k)

    if k in GEO:
         print("gravity found!")
         k = GEO[(GEO.index(k)+1) % len(GEO)]
    else:
        print("gravity not found :(")
        k = GEO[0]

    p = absoluteP(k[:2])
    g = absoluteG(k[2:])
 
    l = call("xdotool windowsize %d %d%% %d%%" % (w,k[2],k[3]))
    l = call("xdotool windowmove %d %d%% %d%%" % (w,k[0],k[1]))
    l = call("xdotool mousemove %d %d" % (-o[0]+p[0]+g[0]//2, 25-o[1]+p[1]+g[1]//2))



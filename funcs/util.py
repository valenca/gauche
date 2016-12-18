from subprocess import Popen,PIPE,STDOUT
from math import sqrt
from operator import add

DEBUG = True

def runProcess(exe):
    p = Popen(exe.split(), stdout=PIPE, stderr=STDOUT)
    while(True):
        retcode = p.poll()
        line = p.stdout.read()
        yield line
        if(retcode is not None):
            break

def call(exe):
    if(DEBUG):
        print("CMD \'%s\':" % exe)
        ret = next(runProcess(exe)).decode('utf-8').strip("\n")
        print(ret.split("\n"))
        return ret
    else:
        return next(runProcess(exe)).decode('utf-8').strip("\n")
        
def dist(x1, x2, y1, y2):
    return sqrt((x1-x2)**2+(y1-y2)**2)

def getWorkingArea():
    OFF,BAR,SCR = [[i for i in call("wmctrl -d").split("\n") if i[3] == '*'][0].split()[x] for x in (5,7,8)]

    SCR = tuple(map(int,SCR.split("x")))
    OFF = tuple(map(int,OFF.split(",")))
    BAR = tuple(map(int,BAR.split(",")))

    return SCR, tuple(map(add,OFF,BAR))

def getMousePosition():
    return list(map(lambda x: int(x[2:]), call("xdotool getmouselocation").split()[:2]))

def getCurrentWindow():
    return int(call("xdotool getwindowfocus"))

def getAllDesktopWindows():
    return [int(x[0],0) for x in [x.split() for x in call("wmctrl -l").split("\n")] if (x[1] == call("xdotool get_desktop") or x[3][:3] == "[*]")]
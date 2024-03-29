from subprocess import Popen,PIPE,STDOUT
from math import sqrt
from operator import add,sub

DEBUG = True

GAP = [
    [  0,  0,  0,  0],
    [380, 45, 45, 45],
    [  0,  0,  0,  0]
]

def call(EXE):
    OUT = Popen(EXE, stdout = PIPE, shell = True).stdout.read().decode("utf-8").strip()
    if DEBUG: print(EXE,"\n",OUT)
    return OUT

def dist(x1, x2, y1, y2):
    return sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

def getScreens():
    screens = [list(map(int, i.split())) for i in call("xrandr --current | grep -o '[0-9]\+x[0-9]\++[0-9]\++[0-9]\+' | sed -E s/'[x|+]'/'\ '/g").split("\n")]

    if 'GAP' in globals():
        for screen in range(len(screens)):
            gap = GAP[screen]
            screens[screen] = [
                screens[screen][0] - gap[0] - gap[1],
                screens[screen][1] - gap[2] - gap[3],
                screens[screen][2] + gap[0],
                screens[screen][3] + gap[2],
            ]

    return screens

def getWorkingArea():
    BAR = [(0, 25),(0,0),(0,0)]
    LST = getScreens()
    CUR = getCurrentScreen(LST)
    OUT = LST[CUR]

    return tuple(map(sub, OUT[:2], BAR[CUR])), tuple(map(add, OUT[2:], BAR[CUR]))

def getMousePosition():
    return list(map(lambda x: int(x[2:]), call("xdotool getmouselocation").split()[:2]))

def getCurrentScreen(SCR = getScreens(), MOU = getMousePosition()):
    for i in range(len(SCR)):
        if SCR[i][2] < MOU[0] < SCR[i][2]+SCR[i][0] and SCR[i][3] < MOU[1] < SCR[i][3]+SCR[i][1]:
            return i  

def getCurrentWindow():
    return "0x%08x" % int(call("xdotool getwindowfocus"))
    
def getCurrentDeskstop():
    return call("wmctrl -d | awk '$2 == \"*\" {print $1}'")

def getAllDesktopWindows(DSK = getCurrentDeskstop()):
    return call("wmctrl -l | grep -v 'Desktop$' | awk '$2 == %s || $2 == \'-1\' || /\\[\\*\\]/ {print $1}'" % DSK).split("\n")

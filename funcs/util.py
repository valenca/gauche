from subprocess import Popen,PIPE,STDOUT
from math import sqrt
from operator import add

DEBUG = True

def call(exe):
    return Popen(exe,stdout=PIPE,shell=True).stdout.read().decode("utf-8").strip()

def dist(x1, x2, y1, y2):
    return sqrt((x1-x2)**2+(y1-y2)**2)

def getWorkingArea():
    OFF,BAR = call("wmctrl -d | grep \\* | grep -o '[0-9]*,[0-9]*'").split("\n")
    SCR     = call("wmctrl -d | grep \\* | grep -o '[0-9]*x[0-9]*'").split("\n")[1]

    SCR = tuple(map(int,SCR.split("x")))
    OFF = tuple(map(int,OFF.split(",")))
    BAR = tuple(map(int,BAR.split(",")))

    return SCR, tuple(map(add,OFF,BAR))

def getMousePosition():
    return list(map(lambda x: int(x[2:]), call("xdotool getmouselocation").split()[:2]))

def getCurrentWindow():
    return int(call("xdotool getwindowfocus"))
    """
    a = "0x%08x" % int(call("xdotool getwindowfocus"))
    print(a)
    return a
    """

def getAllDesktopWindows():
    return [int(x[0],0) for x in [x.split() for x in call("wmctrl -l").split("\n")] if (x[1] == call("xdotool get_desktop") or x[3][:3] == "[*]")]
    """
    a=call("wmctrl -l | awk '$2 == 1 || /[\\*]/ {print $1}'").split("\n")
    print(a)
    return a
    """
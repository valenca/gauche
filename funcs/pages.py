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
        if c < 5:
            print("x: %s y: %s" % (x,y))
            return i
    return None

def pages(GEO_LIST):
    display, offset = getWorkingArea()

    window, pos, geo = call("xdotool getwindowgeometry %s" % call("xdotool getwindowfocus")).split("\n")
    
    window = int(window.split()[1])

    pos = relativeP(tuple(map(int, pos.split()[1].split(','))), display, offset)
    geo = relativeG(tuple(map(int, geo.split()[1].split('x'))), display, offset)
 
    grav = tuple(map(int, map(round, pos + geo)))

    for GEO in GEO_LIST:
        try:
            grav = GEO[(closeEnough(grav, GEO)) % len(GEO)]
            
            all_windows    = getAllDesktopWindows()
            current_window = getCurrentWindow()
            window_list    = []

            count = 1
            for window in all_windows:
                output = call("xdotool getwindowgeometry %s" % window).split("\n")


                num = int(output[0].split()[1])
                pos = relativeP(list(map(int, output[1].split()[1].split(","))), display, offset)
                geo = relativeG(list(map(int, output[2].split()[1].split("x"))), display, offset)

                if closeEnough(list(map(int, map(round, pos + geo))), GEO) != None:
                    grav = list(map(int, map(round, pos + geo)))

                    grav[0] = int((100 - (100 - grav[0]) * count))

                    pos = tuple(map(round,absoluteP(grav[:2], display, offset)))
                    geo = tuple(map(round,absoluteG(grav[2:], display, offset)))
                    
                    call("wmctrl -i -r %d -e 0,%d,%d,%d,%d" % (num, pos[0], pos[1], geo[0], geo[1]))
                    count += 0.51
        except TypeError:
            continue

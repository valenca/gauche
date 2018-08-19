from operator import itemgetter
from itertools import groupby

from funcs.util import *

def closeEnough(x,y):
    return abs(x - y) < 5

def travel(direction):
    direction = {   #AVPos  Sign  Horiz
            "left"  : (1,  True,  True),
            "right" : (1, False,  True),
            "up"    : (2,  True, False),
            "down"  : (2, False, False)
    }[direction]

    mouse  = [-1]  + getMousePosition()
    all_windows    = getAllDesktopWindows()
    current_window = getCurrentWindow()
    toggle         = False
    window_list    = []

    for window in all_windows:
        output = call("xdotool getwindowgeometry %s" % window).split("\n")

        pos = tuple(map(int, output[1].split()[1].split(",")))
        geo = tuple(map(int, output[2].split()[1].split("x")))
        
        window_list.append([window, pos[0] + (geo[0] // 2), pos[1] + (geo[1] // 2)])

        if window == current_window:
            current_window = window_list[-1]
            toggle = True

    for i in range(len(window_list)):
        window_list[i].append(dist(mouse[1], window_list[i][1], mouse[2], window_list[i][2]))

    window_list.sort(key = itemgetter(3))

    travel = []
    for i in range(len(window_list)):
        if closeEnough(window_list[i][direction[0]], mouse[direction[0]]): 
            continue
        if toggle and closeEnough(window_list[i][direction[0]], current_window[direction[0]]):
            continue
        if (window_list[i][direction[0]] > mouse[direction[0]]) != direction[1]:
            if (abs(window_list[i][1] - mouse[1]) > abs(window_list[i][2] - mouse[2])) == direction[2]:
                call("xdotool mousemove %d %d" % tuple(window_list[i][1:3]))
                return
            elif travel == []:
                travel = window_list[i]

    if travel != []:
        call("xdotool mousemove %d %d" % tuple(travel[1:3]))

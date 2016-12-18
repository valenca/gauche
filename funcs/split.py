from operator import sub,add

from funcs.util import *

def full(window, display, offset):
    return closeEnough(window[2], display[0]) and closeEnough(window[4], display[1]) and closeEnough(window[1],offset[0]) and closeEnough(window[3],offset[1])

def left(window, display, offset):
    return closeEnough(window[1], offset[0]) and closeEnough(window[3], offset[1]) and closeEnough(window[4], display[1])

def top(window, display, offset):
    return closeEnough(window[3], offset[1]) and closeEnough(window[1], offset[0]) and closeEnough(window[2], display[0])
           
def right(window, display, offset):
    return closeEnough(window[1] + window[2], display[0]) and closeEnough(window[3], offset[1]) and closeEnough(window[4], display[1])

def bottom(window, display, offset):
    return closeEnough(window[3] + window[4], display[1] + offset[1]) and closeEnough(window[1], offset[0]) and closeEnough(window[2], display[0])

def closeEnough(x, y):
    return abs(x-y) < 3

def split(DIM):
    display,offset = getWorkingArea()
    mouse = tuple(map(add,getMousePosition(),offset))

    all_windows = getAllDesktopWindows()

    window_list = []
    for window in all_windows:
        output = call("xdotool getwindowgeometry %d" % window).split("\n")
        pos = tuple(map(int, output[1].split()[1].split(",")))
        geo = tuple(map(int, output[2].split()[1].split("x")))
        
        window_list.append([window, pos[0], geo[0], pos[1], geo[1]])

    if DIM == "vertical":
        for window in window_list:
            # Check if window is in fullscreen:
            if full(window, display, offset):
                print("Window %d is fullscreen, ignoring" % window[0])
                continue
            # Check if window is aligned to the left:
            if left(window, display, offset):
                print("%d is left-aligned, adjusting width" % window[0])
                call("wmctrl -i -r %s -e 0,-1,-1,%d,-1" % (window[0], mouse[0]))
                continue 
            # Check if window is aligned to the right:
            if right(window, display, offset):
                print("%d is right-aligned, adjusting width" % window[0])
                call("wmctrl -i -r %s -e 0,%d,-1,%d,-1" % (window[0], mouse[0], display[0] - mouse[0]))
                continue
        return 
    elif DIM == "horizontal":
        for window in window_list:
            # Check if window is in fullscreen:
            print(window, display, offset)
            if full(window, display, offset):
                print("Window %d is fullscreen, ignoring" % window[0])
                continue
            # Check if window is aligned to the top:
            if top(window, display, offset):
                print("%d is top-aligned, adjusting height" % window[0])
                call("wmctrl -i -r %s -e 0,-1,-1,-1,%d" % (window[0], (mouse[1] - 2 * offset[1])))
                continue 
            # Check if window is aligned to the bottom:
            if bottom(window, display, offset):
                print("%d is bottom-aligned, adjusting height" % window[0])
                call("wmctrl -i -r %s -e 0,-1,%d,-1,%d" % (window[0], mouse[1] - offset[1], display[1] - (mouse[1] - 2 * offset[1])))
                continue
        return 
    raise(KeyError)
#!/usr/bin/env python

from sys import argv
from funcs.gravity import *
from funcs.travel import *
from funcs.util import *

GEO = {
        "video_top"   :[(68,  0, 32, 33), (80,  0, 20, 21), (50,  0, 50, 50)],
        "video_centre":[(10, 10, 80, 80), (25, 25, 50, 51), (33, 33, 32, 33)],
        "chat_bottom" :[(82, 93, 18,  7), (82, 55, 18, 45)]
}

if __name__ == "__main__":
    if argv[1] == "gravity":
        gravity(GEO[argv[2]])
        quit()
    if argv[1] == "travel":
        travel(argv[2])
        quit()

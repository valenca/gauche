#!/usr/bin/env python

#   For best performance remove window titles.
#   Install devilspie with the script: 
# 
#   (if (matches (application_name) ".*") (begin (undercorate)))
#
#   And run it on the background


from sys import argv
from funcs.gravity import *
from funcs.travel import *
from funcs.util import *

GEO = {
        "video_top"   :[(68,  0, 32, 33), (80,  0, 20, 21), (50,  0, 50, 50)],
        "video_centre":[(10, 10, 80, 80), (25, 25, 50, 51), (34, 34, 32, 32)],
        "chat_bottom" :[(82, 55, 18, 45), (82, 93, 18,  7)],

        "left"        :[(0 ,  0,100,100), ( 0,  0, 50,100), ( 0,  0, 67,100), ( 0,  0, 33,100)],
        "right"       :[(50,  0, 50,100), (67,  0, 33,100), (33,  0, 67,100)]
}

OFF = (0,25)

if __name__ == "__main__":
    if argv[1] == "gravity":
        gravity(GEO[argv[2]],OFF)
        quit()
    if argv[1] == "travel":
        travel(argv[2])
        quit()

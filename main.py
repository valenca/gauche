#!/usr/bin/env python
#   For best performance remove window titles.
#   Install devilspie with the script: 
# 
#   (if (matches (application_name) ".*") (begin (undercorate)))
#
#   And run it on the background

import re
from sys import argv
from operator import itemgetter

from gravity import *
from travel import *
from split import *
from stick import *
from util import *

GEO = {
        "video_top"   :[(68,  0, 32, 33), (80,  0, 20, 21), (50,  0, 50, 50)],
        "video_centre":[(10, 10, 80, 80), (25, 25, 50, 51), (34, 34, 32, 32)],
        "chat_bottom" :[(82, 55, 18, 45), (82, 93, 18,  7)],

        "left"        :[(0 ,  0,100,100), ( 0,  0, 50,100), ( 0,  0, 67,100), ( 0,  0, 33,100)],
        "right"       :[(50,  0, 50,100), (67,  0, 33,100), (33,  0, 67,100)],
        "column"      :[(92,  0,  8,100)]
}

if __name__ == "__main__":
    try:
        if argv[1] == "gravity":
            try:
                gravity(GEO[argv[2]])
            except IndexError:
                print("No gravity given. Must be one of these values:\n" + str(list(GEO.keys())))
            except KeyError:
                print("Gravity not supported. Must be one of these values:\n" + str(list(GEO.keys())))
            quit()

        if argv[1] == "travel":
            try:
                travel(argv[2])
            except IndexError:
                print("No travel direction given. Must be one of these values:\n" + str(["up","down","left","right"]))
            except KeyError:
                print("Travel direction not supported. Must be one of these values:\n" + str(["up","down","left","right"]))
            quit()

        if argv[1] == "split":
            try:
                split(argv[2])
            except IndexError:
                print("No direction given. Must be one of " + str(["horizontal","vertical"]) + ".")
            except KeyError:
                print("Invalid argument. Must be one of " + str(["horizontal","vertical"]) + ".")
            quit()

        if argv[1] == "stick":
            stick()
            quit()

        raise KeyError
    except IndexError:
        print("No function given. Must be one of " + str(["gravity", "travel", "split", "stick"]))
    except KeyError:
        print("Function not supported. Must be one of " + str(["gravity", "travel", "split", "stick"]))

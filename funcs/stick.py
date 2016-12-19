from funcs.util import *

def stick():
	window = getCurrentWindow()
	name = call("xdotool getwindowname %s" % window)
	if name[:3] == "[*]":
		call("wmctrl -i -r %s -N %s" % (window, name[3:]))
		call("wmctrl -i -r %s -b remove,sticky" % window)
	else:
		call("wmctrl -i -r %s -N %s" % (window, "[*]" + name))
		call("wmctrl -i -r %s -b add,sticky" % window)


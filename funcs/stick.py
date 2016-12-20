from funcs.util import *
from re import escape

def stick():
	window = getCurrentWindow()
	name = escape(call("xdotool getwindowname %s" % window))
	if name[:3] == "[*]":
		if DEBUG: print("Sticky window found: unsticking.")
		call("wmctrl -i -r %s -N %s" % (window, name[3:]))
		call("wmctrl -i -r %s -b remove,sticky" % window)
	else:
		if DEBUG: print("Non-Sticky window found: sticking.")
		call("wmctrl -i -r %s -N %s" % (window, "[*]" + name))
		call("wmctrl -i -r %s -b add,sticky" % window)


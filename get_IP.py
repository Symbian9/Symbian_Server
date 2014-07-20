# -*- coding: utf-8 -*-
"""
Small script to get the current IP address from a Nokia Symbian^1/S60-5th edition
mobile connected to an wi-fi lan.
Requires the socket_tasks.py library.

17/Jul/2014 Bernardo J.B. Schmitt - bernardo.jb.schmitt@gmail.com
"""

# Replace here with the path where the *.py files are saved.
#--------------------------------
file_path = "e:\\Python"
#--------------------------------

import sys
sys.path.append(file_path)

from socket_tasks import *
from appuifw import *

app.title = u"Get IP"
apo = sel_access_point()
apo.start()

note(u"Cell IP: "+apo.ip(), "info")

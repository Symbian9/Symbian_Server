# -*- coding: utf-8 -*-
"""
Creates a network server in a Nokia Symbian^1/S60-5th edition mobile connected
to an wi-fi lan, allowing the cell phone to be accessed remotely by another device.
Requires the socket_tasks.py library.

17/Jul/2014 Bernardo J.B. Schmitt - bernardo.jb.schmitt@gmail.com
"""

# Replace here with the path where the *.py files are saved and the desired TCP port.
#--------------------------------
file_path = "e:\\Python"
port = 27051
#--------------------------------


import sys
sys.path.append(file_path)

from appuifw import *
from socket_tasks import *
 
app.title = u"S60 server"
 
apo = sel_access_point()
apo.start()

sock_server = SymbServerObj(apo.ip(),port,file_path)

sock_server.listening()

while True:
    try:
        cmd = safe_recv(sock_server.client)
    except:
        sock_server.client.close()
        sock_server.close()
        break
    
    cmd = cmd.decode('latin-1')
    sep_cmd = cmd.split(' ')
    
    if sep_cmd[0].strip().lower() == 'cd':
        sock_server.cd(' '.join(sep_cmd[1:]))
        
    if sep_cmd[0].strip().lower() == 'cp':
        sock_server.cp(sep_cmd)
        
    if sep_cmd[0] == 'getSMS':
        sock_server.get_SMS()
    
    if sep_cmd[0].strip().lower() == 'ls':
        sock_server.ls()
           
    if sep_cmd[0].strip().lower() == 'exit':
        print 'Exiting'
        sock_server.client.close()
        sock_server.close()
        break 

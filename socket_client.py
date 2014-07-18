# -*- coding: utf-8 -*-
"""
Connect the current device to a network server created by a 
Nokia Symbian^1/S60-5th edition mobile in the same lan,
allowing the cellphone to be accessed remotely.
Requires the socket_tasks.py library.

17/Jul/2014 Bernardo J.B. Schmitt - bernardo.jb.schmitt@gmail.com
"""

# Replace here with the IP address and the TCP port from the server.
#--------------------------------
server_IP = '10.0.0.102'
server_port = 27051
#--------------------------------

from socket_tasks import *

sock_client = ClientObj(server_IP, server_port)

while True:
    
    try:
        cmd = raw_input(sock_client.dir+'$ ')
    except:
        sock_client.close()
        break
    safe_send(sock_client,cmd.decode('utf-8').encode('latin-1'))
    sep_cmd = cmd.split(' ')  
    
    if sep_cmd[0].strip().lower() == 'cd':
        sock_client.cd()
        
    if sep_cmd[0].strip().lower() == 'chdir':
        sock_client.chdir(sep_cmd)
            
    if sep_cmd[0].strip().lower() == 'cp':
        sock_client.cp(sep_cmd)
    
    if sep_cmd[0].strip().lower() == 'getcwd':
        sock_client.getcwd() 
        
    if sep_cmd[0] == 'getSMS':
        sock_client.get_SMS(sep_cmd)
    
    if sep_cmd[0].strip().lower() == 'ls':
        sock_client.ls()
        
    if sep_cmd[0].strip().lower() == 'exit':
        sock_client.close()
        break


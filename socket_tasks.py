# -*- coding: utf-8 -*-
"""
Library containing the tools required to create a network server and a client, 
allowing therefore a Nokia Symbian^1/S60-5th edition mobile to be accessed remotely by 
an UNIX-like terminal.

17/Jul/2014 Bernardo J.B. Schmitt - bernardo.jb.schmitt@gmail.com
"""

try:
    from appuifw import *
    import btsocket
    import inbox
except:
    pass

import getopt
import os
import socket
import time

#-----------------
#Creates a symbian server object.
#-----------------

class SymbServerObj(socket._socketobject):
    
    def __init__(self,IP,port,file_path):
        socket._socketobject.__init__(self,socket.AF_INET, socket.SOCK_STREAM)       
        self.bind((IP,port))
        self.listen(1)
        self.dir = file_path
        os.chdir(self.dir)
    
    def cd(self,directory):
        try:
            os.chdir(directory)
            self.dir = os.getcwd()
            self.client.sendall(self.dir)
        except:
            self.client.sendall('FAIL')
            
    def cp(self,sep_cmd):
        status = send_recv_parse(sep_cmd[1:],'cell')
        if status == 'SEND':
            send_file(self.client,sep_cmd[2]) 
        elif status == 'RECEIVE':
            recv_file(self.client,sep_cmd[4])

    def get_SMS(self):
        box = inbox.Inbox(inbox.EInbox)
        messages = box.sms_messages()
        SMS = []
        for id in messages:
            sender = "%s - " % box.address(id)
            date = time.strftime("%A, %d/%B/%Y - %H:%M:%S\n", time.localtime(box.time(id)))
            content = box.content(id)
            SMS.append((sender+date+content).encode('latin-1'))
        SMS = ',SEP,'.join(SMS)
        safe_send(self.client,SMS)    
    
    def listening(self):
        while True:
            (self.client, self.addr) = self.accept()
            note(u"Connected to %s:%d" % (self.addr[0],self.addr[1]),"info")
            self.client.sendall(self.dir)
            break
        
    def ls(self):
        dir_obj = dir_list()
        dir_obj = ',SEP,'.join(dir_obj)
        safe_send(self.client,dir_obj)
        
#-----------------
#Creates a network client object.
#-----------------        

class ClientObj(socket._socketobject):
    
    def __init__(self,IP,port):
        socket._socketobject.__init__(self,socket.AF_INET, socket.SOCK_STREAM)
        self.connect((IP, port))
        self.dir = self.recv(4096)
        
    def cd(self):
        new_dir = self.recv(4096)
        if new_dir == 'FAIL':
            print 'Directory not found!'
        else:
            self.dir = new_dir
            
    def chdir(self,sep_cmd):
        try:
            os.chdir(sep_cmd[1])
        except:
            print 'Directory not found!'         
            
    def cp(self,sep_cmd):
        status = send_recv_parse(sep_cmd[1:],'desktop')
        if status == 'SEND':
            send_file(self,sep_cmd[2])
        elif status == 'RECEIVE':
            recv_file(self,sep_cmd[4])
            
    def getcwd(self):
        print os.getcwd() 
            
    def get_SMS(self,sep_cmd):
        SMS = safe_recv(self)
        SMS = SMS.decode('latin-1')
        SMS = SMS.split(',SEP,')
        if len(sep_cmd)>0:
            options,not_opt = getopt.getopt(sep_cmd[1:],'f:s:v',
                                            ['filter=','save=','verbose'])
            for opt, arg in options:            
                if opt in ('-f', '--filter'):
                    names_index = split_SMS(SMS,arg.decode('utf-8'))
                    SMS = [SMS[i] for i in names_index]
                if opt in ('-s', '--save'):
                    file_id = open(arg, 'w')
                    write_list(SMS,file_id)
                    file_id.close()
                if opt in ('-v', '--verbose'):        
                    print_list(SMS)
                    
    def ls(self):
        dir_objects = safe_recv(self)
        dir_objects = dir_objects.split(',SEP,')
        print_list(dir_objects)                    

#-----------------
#Set of tools necessary to assure a safe file/commands transmission.  
#-----------------

def safe_recv(sock):
    dir_len = sock.recv(4096)
    sock.sendall('OK')
    objects=''
    while len(objects)<int(dir_len):
        buff = sock.recv(1024)
        objects += buff
    return objects
    
def safe_send(sock,objects):
    sock.sendall(str(len(objects)))
    status = sock.recv(4096)
    if status == 'OK':
        sock.sendall(objects)

def recv_file(sock,dir_name):
    file_name = safe_recv(sock).decode('latin-1')    
    if os.path.isdir(dir_name):
        status = 'OK'
    else:
        status = 'FAIL'
    sock.sendall(status)
    if status=='OK' and file_name!='FAIL':
        data = safe_recv(sock)
        file_id = open(dir_name+os.sep+file_name, 'wb')
        file_id.write(data)
        file_id.close()
    elif status=='FAIL':
        print 'Directory not valid!'

def send_file(sock,file_path):
    if os.path.exists(file_path):
        file_name = os.path.basename(file_path)
    else:
        file_name = 'FAIL'
        print 'File not found!'
    safe_send(sock,file_name.encode('latin-1'))
    status = sock.recv(4096)
    if status=='OK' and file_name!='FAIL':
        file_id = open(file_path, 'rb')
        data = file_id.read()
        safe_send(sock,data)
        file_id.close()
    elif status=='FAIL':
        print 'Directory not valid!'

# Function that parses whether the device is receaving or sending files.
def send_recv_parse(cmd,device):
    
    if len(cmd)==4:
        options,not_opt = getopt.getopt(cmd,'c:d:',['cell=','desktop='])
        if (options[0][0]==('-c' or '--cell') and
        options[1][0]==('-d' or '--desktop') and device=='cell') or \
        (options[0][0]==('-d' or '--desktop') and 
        options[1][0]==('-c' or '--cell') and device=='desktop'):
            status = 'SEND'
        else:
            status = 'RECEIVE'
        return status
    else:
        print 'Cannot copy, number of parameters incorrect!'
        return 'FAIL'

#-----------------
#Set of auxiliary functions.
#-----------------           
            
def dir_list():
     objects = os.listdir(os.getcwd())
     objects = sorted(objects, key=str.lower)
     return objects
     
def print_list(objects):
    for obj in objects:
         print obj
      
def sel_access_point():

    aps = btsocket.access_points()
    if not aps:
        note(u"No access points available","error")
        return None
    ap_labels = map(lambda x: x['name'], aps)
    item = popup_menu(ap_labels,u"Access points:")
    if item is None:
        return None
    apo = btsocket.access_point(aps[item]['iapid'])
    btsocket.set_default_access_point(apo)
    return apo
    
def split_SMS(SMS,name):
    index = [n for n in range(len(SMS)) if SMS[n].split('-',1)[0][:-1]==name]
    return index
    
def write_list(objects,f_id):
    for obj in objects:
        f_id.write((obj+'\n').encode('latin-1'))

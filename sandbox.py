# Referenced
# https://dev.to/narasimha1997/building-a-secure-sandboxed-environment-for-executing-untrusted-code-7e8
# https://www.endpoint.com/blog/2015/01/28/getting-realtime-output-using-python

import os
import threading
import subprocess
import requests
import json
import socket


# Finds an open port to use for a TCP connection
# From: https://stackoverflow.com/a/2838309/11039508
def findOpenPort():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("",0))
    s.listen(1)
    port = s.getsockname()[1]
    s.close()
    return port


# Runs a new Docker container for a sandbox and returns the port the container's HTTP
# client is listening on. Assumes that the image is built -- i.e., run build.sh before.
class Sandbox:
    # Initializes a sandbox by finding an open port and starting a docker container
    def __init__(self):
        while True:
            # Finds an open port
            self.port = findOpenPort()
            
            # Runs a sandbox docker container on open port
            # (May fail because of race conditions due to the found
            # open port already being used by another process)
            cmd = "bash ./sandbox/run.sh " + str(self.port)
            process = subprocess.Popen([cmd], shell=True, 
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
            
            
            # Handles extracting the container ID from the output and handling errors
            get_output = lambda : process.stdout.readline().strip().decode('utf-8')
            while True:
                err = process.stderr.readline()
                if process.poll() is not None:
                    # Process has finished running
                    break
                elif err != b'':
                    # Docker threw an error but is still running
                    # E.g., the port is in an excluded port range
                    # ----------------
                    # Removes the docker container so process can exit
                    os.system("docker rm " + get_output() + " >/dev/null 2>&1")

            if (process.poll() != 0):
                # Docker threw an error
                # E.g., the port is being used by another process
                # or the port is in an excluded port range
                # ----------------
                # Try again with a new port
                continue
            
            # Sandbox container successfully started
            self.container = get_output()
            break

    # Stops the currently running sandbox docker container
    def __del__(self):
        cmd = "bash ./sandbox/stop.sh " + self.container
        t = threading.Thread(target=os.system, args=(cmd,))
        t.start()

    # Executes a command in the running sandbox
    def exec(self, cmd):
        data = {
            'cmd':cmd
        }

        addr = 'http://localhost:' + str(self.port)
        r = requests.post(url=addr, data=data)
        
        return json.loads(r.text)


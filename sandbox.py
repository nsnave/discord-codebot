# Referenced
# https://dev.to/narasimha1997/building-a-secure-sandboxed-environment-for-executing-untrusted-code-7e8
# 

import os
import threading
import subprocess
import requests
import json

# Runs a new Docker container for a sandbox and returns the port the container's HTTP
# client is listening on. Assumes that the image is built -- i.e., run build.sh before.
class Sandbox:
    def __init__(self):
        # TODO: Find open port
        port = 8000
        
        cmd = "bash ./sandbox/run.sh " + str(port)
        self.container = subprocess.check_output(cmd, shell=True).decode('utf-8')
        self.port = port

    def stop(self):
        cmd = "bash ./sandbox/stop.sh " + self.container
        t = threading.Thread(target=os.system, args=(cmd,))
        t.start()

    def exec(self, cmd):
        data = {
            'cmd':cmd
        }

        addr = 'http://localhost:' + str(self.port)
        r = requests.post(url=addr, data=data)
        
        return json.loads(r.text)


class Test:
    def unpack(self, res):
        return res[0]

    def handle(self, res):
        return self.unpack(res)
        
class Test2(Test):
    def unpack(self, res):
        return res[1]

t = Test2()
print(t.handle([1, 2]))
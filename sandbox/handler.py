from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
import json
import subprocess
import time


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    '''
    def do_GET(self):

        path = self.path

        voter = path.split("voter=")[1]

        if voter not in tokens:
            token = vote_crypto.get_token()
            while token in tokens.values(): #used to ensure each voter has a different token
                token = vote_crypto.get_token()
            tokens[voter] = token
        
        token = tokens[voter]

        encrypted_token = vote_crypto.encrypt(voter_keys[voter]['public_key'], token)

        self.send_response(200)
        self.end_headers()
        self.wfile.write(encrypted_token.encode('utf-8'))
    '''

    # Handles HEAD requests, used for testing whether the server is running
    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()

    # Runs the command specified by the parameter 'cmd' 
    def do_POST(self):
        # Extracts command to run
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)

        query = body.decode()
        cmd = parse_qs(query)['cmd'][0]

        # Runs the command and processes the result
        result = subprocess.run([cmd], shell=True, 
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)

        resp = {
            'exit':result.returncode,
            'out':result.stdout.decode('utf-8'),
            'err':result.stderr.decode('utf-8')
        }
        
        # Returns the result
        self.send_response(200)
        self.end_headers()
        self.wfile.write(json.dumps(resp).encode('utf-8'))


# Starts running the command handler server in the sandbox
print("Serving...")
httpd = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
print(time.time())
httpd.serve_forever()




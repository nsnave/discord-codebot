from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
import json


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

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)

        query = body.decode()
        cmd = parse_qs(query)['cmd'][0]

        self.send_response(200)
        self.end_headers()

        resp = {
            'exit':0,
            'out':cmd,
            'err':'nope'
        }
        
        self.wfile.write(json.dumps(resp).encode('utf-8'))

    '''
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)

        #gets voter
        body = body.decode()
        splt = body.split("&")

        voter = splt[0].split('=')[1]

        #gets vote by decrypting ciphertext and verifying signature
        ciphertext, signed_token = vote_crypto.decode(splt[1].split('=')[1].replace("%7C", "|"))        
        success, vote = process(voter, ciphertext, signed_token)

        self.send_response(200)
        self.end_headers()

        if (success):
            print("Vote recorded for voter {}".format(voter))
            resp = 'Succesfully voted for \"{}\"\nThanks for voting!'.format(vote)
        else:
            print("Failed to record vote for {}".format(voter))
            resp = 'Invalid vote: {}'.format(vote)
            
        self.wfile.write(resp.encode('utf-8'))

        print("All Votes:")
        print(votes)
    '''

print("Serving...")
httpd = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
httpd.serve_forever()




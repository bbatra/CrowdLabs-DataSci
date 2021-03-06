#!/usr/bin/python
from http.server import BaseHTTPRequestHandler, HTTPServer
from os import curdir, sep
from ctypes import c_uint32
import cgi
from flask import request

# nlp = __import__(input('nlp'))
from nlp import *

PORT_NUMBER = 8080

# This class will handles any incoming request from
# the browser
class RequestHandler(BaseHTTPRequestHandler):

    # Handler for the GET requests
    def do_GET(self):
        if self.path == "/":
            self.path = "/index.html"

        try:
            # Check the file extension required and
            # set the right mime type

            sendReply = False
            if self.path.endswith(".html"):
                mimetype = 'text/html'
                sendReply = True
            if self.path.endswith(".jpg"):
                mimetype = 'image/jpg'
                sendReply = True
            if self.path.endswith(".gif"):
                mimetype = 'image/gif'
                sendReply = True
            if self.path.endswith(".js"):
                mimetype = 'application/javascript'
                sendReply = True
            if self.path.endswith(".css"):
                mimetype = 'text/css'
                sendReply = True

            if sendReply == True:
                # Open the static file requested and send it
                f = open(curdir + sep + self.path)
                self.send_response(200)
                self.send_header('Content-type', mimetype)
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
            return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    #USE THIS OJASH
    # Handler for the POST requests
    def do_POST(self):
        # form = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ= {
        #         'REQUEST_METHOD' : 'POST',
        #         'CONTENT_TYPE': self.headers['Content-Type']
        #     })

        if self.path == "/similarity":

            threshold = request.form['threshold']
            q1 = request.form['string1']
            q2 = request.form['string2']
            q2 = q2.split('%')
            print(q2)
            result = basic_paraphrase_recognizer(q1, q2, threshold)
            self.send_response(200)
            self.end_headers()
            print('result is')
            print(result)
            self.wfile.write(str(result).encode())
            return


try:
    # Create a web server and define the handler to manage the
    # incoming request
    server = HTTPServer(('', PORT_NUMBER), RequestHandler)
    ##print 'Started httpserver on port ', PORT_NUMBER

    # Wait forever for incoming htto requests
    server.serve_forever()

except KeyboardInterrupt:
    print('^C received, shutting down the web server')
    server.socket.close()


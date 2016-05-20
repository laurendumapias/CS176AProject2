#Http Server

import socket
import SocketServer
import sys

html_body = """<!DOCTYPE html>
<html>
<head>
 <title>names</title>
</head>
<body>
 <p>Lauren Dumapias, 7219199</p>
 <p>Vivek Patel, 7538499</p>
</body>
</html>"""

class HttpServer(object):

     def __init__(self):
         self.host = ' '
         self.port = 80
         self.address = (self.hostname, self.port)

         self.socket = socket.socket(socket.A_INET, socket.SOCK_STREAM)
         try:
             self.socket.bind((self.host, self.port))

         except Exception as e:
             print ("Could not bind to socket \n")
             self.port = 8080

             try:
                print("Binding to new port \n")
                self.socket.bind((self.host, self.port))

             except Exception as e:
                print ("ERROR, Failure to bind to socket \n")
                self.socket.shutddown9socket.SHUT_RDWR)
                sys.exit(1)









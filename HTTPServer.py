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

                self.listenForClients()

     def listenForClients(self):
           """ Main loop awaiting connections """
     while True:
         print ("Waiting for new Client")
         self.socket.listen(3) # maximum number of queued connections
         conn, addr = self.socket.accept()

         # conn - socket to client

         # addr - clients address
 
         print("Got connection from:", addr)

         data = conn.recv(1024) #receive data from client

         string = bytes.decode(data) #decode it to string

         #determine request method  (HEAD and GET are supported)

         request_method = string.split(' ')[0]
         print ("Method: ", request_method)
         print ("Request body: ", string)

         #if string[0:3] == 'GET':
         if (request_method == 'GET') | (request_method == 'HEAD'):
             #file_requested = string[4:]
             # split on space "GET /file.html" -into-> ('GET','file.html',...)
             file_requested = string.split(' ')
             file_requested = file_requested[1] # get 2nd element
 
             #Check for URL arguments. Disregard them
             file_requested = file_requested.split('?')[0]  # disregard anything after '?'
 
             if (file_requested == '/'):  # in case no file is specified by the browser
                 file_requested = '/index.html' # load index.html by default
 
             file_requested = self.www_dir + file_requested
             print ("Serving web page [",file_requested,"]")
 
             ## Load file content
             try:
                 file_handler = open(file_requested,'rb')
                 if (request_method == 'GET'):  #only read the file when GET
                     response_content = file_handler.read() # read file content
                 file_handler.close()
 
                 response_headers = self._gen_headers( 200)

except Exception as e: #in case file was not found, generate 404 page
                 print ("Warning, file not found. Serving response code 404\n", e)
                 response_headers = self._gen_headers( 404)
 
                 if (request_method == 'GET'):
                    response_content = b"<html><body><p>Error 404: File not found</p><p>Python HTTP server</p></body></html>"
             server_response =  response_headers.encode() # return headers for GET and HEAD
             if (request_method == 'GET'):
                 server_response +=  response_content  # return additional conten for GET only

             conn.send(server_response)
             print ("Closing connection with client")
             conn.close()
else:
             print("Unknown HTTP request method:", request_method)
 

                
#Code From Chris Coakley stupid_server.py 
class ThreadedHTTPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    # Ctrl-C will cleanly kill all spawned threads
    daemon_threads = True
    # much faster rebinding
    allow_reuse_address = True

if __name__ == '__main__':
    server = ThreadedHTTPServer((HOST, PORT), HTTPServer)
    # terminate with Ctrl-C
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        sys.exit(0)





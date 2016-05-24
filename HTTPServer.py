#Http Server

import socket
import SocketServer
import sys
import logging

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

HOST = ' '
PORT = 80

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# create formatter
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
# add formatter to ch
ch.setFormatter(formatter)
# add ch to logger
logger.addHandler(ch)

class HttpServer(SocketServer.BaseRequestHandler):
     def handle(self):
       while True:
         try:
            print "handling"
            data = self.request.recv(1024)
            while data[-2:] != "\n\n":
              data += self.request.recv(1024)
            logger.info(data)
            command = data.split(" ")[0].strip()
            if command != 'GET' and command != 'HEAD':
                self.request.send("501 Not Implemented")
                data = ""
                continue
            request = data.split("/")[3].strip()
            if request != 'names' and request != 'sort':
                self.request.send("401 Unauthorized")
                data = ""
                continue
            if request == 'names':
               if command == 'GET':
                self.getNames(data)
               if command == 'HEAD':
                self.headNames(data)
            if request == 'sort':
               if command == 'GET':
                self.getSort(data)
               if command == 'HEAD':
                self.headSort(data)
            data = ""
          except Exception as e:
              logger.exception(e)
              self.request.send("ERROR {}\n\n".format(e))

      def getNames(self, data):
          #parse the GET line
          self.request.send(html_body)

      def headNames(self, data):

      def getSort(self, data):
          numOfNumbers = len(data.split("/"))


      def headSort(self, data):
          #parse the HEAD line


 

                
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





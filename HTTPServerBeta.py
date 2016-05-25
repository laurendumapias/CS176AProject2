# stupid server

import socket
import logging
import sys
import threading
import SocketServer
import random
import time
import sys 

HOST = ''
PORT = 8080

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

HEADER_NAME = "HTTP/1.1 200 OK\r\n Content-Type: text/html\r\n Content-Length: "
HEADER_SORT = "HTTP/1.1 200 OK\r\n Content-Type: text/plain\r\n"

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
                logger.info(data)
                data = data.split('\n')[0]
                command = (data.split())[0]
                requestBlock = data.split()[1]
                if command != "GET" and command != "HEAD":
                    self.request.send("501 Not Implemented")
                    data = ""
                    self.request.close()
                    continue
                request = requestBlock.split('/')[1]
                print request
                if request != 'names' and request != 'sort':
                    self.request.send("404 Not Found")
                    data = ""
                    self.request.close()
                    continue
                if request == 'names':
                    if command == 'GET':
                        self.getNames(data)
                    if command == 'HEAD':
                        self.headNames(data)
                if request == 'sort':
                    if command == 'GET':
                        # print daemon_threads
                        self.getSort(requestBlock)
                    if command == 'HEAD':
                        self.headSort(requestBlock)
                data = ""
            except Exception as e:
                logger.exception(e)
                self.request.send("ERROR {}\n\n".format(e))

    def headNames(self, data):
        self.request.send('HTTP/1.1 200 OK\r\n')
        self.request.send("Content-Type: text/html\r\n")
        self.request.send("Content-Length: " + str(len(html_body)) + " \r\n")
        self.request.send("Date: " + str(time.strftime("%c")) + "\r\n\r\n")
        self.request.close()

    # Done!
    def getNames(self, data):
        self.request.send('HTTP/1.1 200 OK\r\n')
        self.request.send("Content-Type: text/html\r\n")
        self.request.send("Content-Length: " + str(len(html_body)) + " \r\n")
        self.request.send("Date: " + str(time.strftime("%c")) + "\r\n\r\n") 
        self.request.send(html_body)            
        self.request.close()

    # Done!
    def getSort(self, data):
        numOfNumbers = len(data.split('/')[1:])
        if numOfNumbers <= 0:
            self.request.send("404 Not Found")
            self.request.close()
            return
        numList = data.split('/')[2:]
        for item in numList:
            if(item.isdigit() == False or item < 0):
                self.request.send("404 Not Found")
                self.request.close()
                return
        numList = [int(x) for x in numList]
        numList.sort()
        response = "SORTED LIST: "
        for num in numList:
            response += str(num)
            response += ' '
        print '\n'
        self.request.send('HTTP/1.1 200 OK\r\n')
        self.request.send("Content-Type: text/plain\r\n")
        self.request.send("Content-Length: " + str(len(response)) + " \r\n")
        self.request.send("Date: " + str(time.strftime("%c")) + "\r\n\r\n") 
        self.request.send(response)            
        self.request.close()

    def headSort(self, data):
        numOfNumbers = len(data.split('/')[1:])
        print data
        if numOfNumbers <= 0:
            print "Num of nums is negative"
            self.request.send("404 Not Found")
            self.request.close()
            return
        numList = data.split('/')[2:]
        for item in numList:
            if(item.isdigit() == False or item < 0):
                print "NOT A DIGIT"
                self.request.send("404 Not Found")
                self.request.close()
                return
        numList = [int(x) for x in numList]
        numList.sort()
        response = "SORTED LIST: "
        for num in numList:
            response += str(num)
            response += ' '
        print '\n'
        print "Response sending..."
        self.request.send('HTTP/1.1 200 OK\r\n')
        self.request.send("Content-Type: text/plain\r\n")
        self.request.send("Content-Length: " + str(len(response)) + " \r\n")
        self.request.send("Date: " + str(time.strftime("%c")) + "\r\n\r\n")       
        self.request.close()

        # parse the HEAD line

        # Code From Chris Coakley stupid_server.py

class ThreadedStupidServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    # Ctrl-C will cleanly kill all spawned threads
    daemon_threads = True
    # much faster rebinding
    allow_reuse_address = True

if __name__ == '__main__':
    server = ThreadedStupidServer((HOST, int(sys.argv[1])), HttpServer)
    # terminate with Ctrl-C
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        sys.exit(0)
# Python http server using select()
#
# This was built using the following resources:
# A select() tutorial
# http://pymotw.com/2/select/
# A non-blocking read from stdin example
# http://repolinux.wordpress.com/2012/10/09/non-blocking-read-from-stdin-in-python/

import select
import socket
import logging
import sys
import threading
import SocketServer
import random
import Queue

HOST = ''
PORT = 8080

HEADER = "HTTP/1.1 200 OK\n Date: Wed, 11 Apr 2012 21:29:04 GMT\n Server: Python/6.6.6 (custom)\n Content-Type: text/plain\n"

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
        self.socket = socket.socket()
        self.socket.setblocking(0)
        self.hostname = socket.gethostname()
        self.port = 8880
        self.address = (self.hostname, self.port)
        print self.address
        self.run()

    def close(self, s):
        if s in self.outputs:
            self.outputs.remove(s)
        self.inputs.remove(s)
        s.close()
        # remove the message queue
        del self.message_queues[s]
        del self.message_entireties[s]
        
    def run(self):
        self.socket.bind(self.address)
        self.socket.listen(5)
        self.inputs = [self.socket]
        self.outputs = []
        self.message_queues = {}
        self.message_entireties = {}
        while True:
            try:
                print "handling"
                data = self.request.recv(1024)
                data = data.split('\n')[0]
                command = (data.split())[0]
                requestBlock = data.split()[1]
                if command != 'GET' and command != 'HEAD':
                    self.request.send("501 Not Implemented")
                    data = ""
                    continue
                request = requestBlock.split('/')[0].strip()
                if request != 'names' and request != 'sort':
                    self.request.send("404 Not Found")
                    data = ""
                    continue
                if request == 'names':
                    if command == 'GET':
                        self.getNames(data)
                    if command == 'HEAD':
                        self.headNames(data)
                if request == 'sort':
                    if command == 'GET':
                        print daemon_threads
                        self.getSort(requestBlock)
                    if command == 'HEAD':
                        self.headSort(data)
                data = ""
            except Exception as e:
                logger.exception(e)
                self.request.send("ERROR {}\n\n".format(e))

        def headNames(self, data):
            return

        def getSort(self, data):
            numOfNumbers = len(data.split('/')[1:])
            if numOfNumbers <= 0:
                self.request.send("404 Not Found")
                return
            numList = data.split('/')[1:]
            numList = [int(x) for x in numList]
            numList.sort()
            responseString = "SORTED LIST " + numList + "\n"
            self.request.send(self.response(responseString))

        def headSort(self, data):

            return
            # parse the HEAD line

            # Code From Chris Coakley stupid_server.py

    def response(self, data):
        line = "\r\n"
        header = "HTTP/1.0 200 OK" + line + "Content-Type: text/plain" + line + data + line
        return header

class ThreadedStupidServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    # Ctrl-C will cleanly kill all spawned threads
    daemon_threads = True
    # much faster rebinding
    allow_reuse_address = True

if __name__ == '__main__':
    server = ThreadedStupidServer((HOST, PORT), HttpServer)
    # terminate with Ctrl-C
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        sys.exit(0)
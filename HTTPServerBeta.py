# stupid server

import socket
import logging
import sys
import threading
import SocketServer
import random

HOST = ''
PORT = 8080

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
            self.request.send("HTTP/1.0 200 OK" + "Content-Type: text/plain" + data + html_body)

        def headSort(self, data):

            return
            # parse the HEAD line

            # Code From Chris Coakley stupid_server.py

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
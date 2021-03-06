# Http Server

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
PORT = 8080

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# create formatter
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
# add formatter to ch
ch.setFormatter(formatter)
# add ch to logger
logger.addHandler(ch)


class HTTPServer(SocketServer.BaseRequestHandler):

    def handle(self):
        while True:
            try:
                print "handling"
                data = self.request.recv(1024)
                while data[-2:] != "\n\n":
                    data += self.request.recv(1024)
                logger.info(data)
                data = data[:-4]
                command = data.split(" ")[0].strip()
                if command != 'GET' and command != 'HEAD':
                    self.request.send("501 Not Implemented")
                    data = ""
                    continue
                request = data.split("/")[3].strip()
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
                        self.getSort(data)
                    if command == 'HEAD':
                        self.headSort(data)
                data = ""
            except Exception as e:
                logger.exception(e)
                self.request.send("ERROR {}\n\n".format(e))

    def getNames(self, data):
        response = "Content-Type = text/html \n Content-Length = "
        sys.getsizeof(string)
        self.request.send(html_body)

    def headNames(self, data):

        def getSort(self, data):
            numOfNumbers = len(data.split("/"))
            if numOfNumbers < 4:
                self.request.send("404 Not Found")
                return
            for i in (4, numOfNumbers):
                if data.split("/")[i].isDigit == False or data.split("/")[i] < 0:
                    self.request.send("404 Not Found")
                    return
            self.request.send(data.split("/").sort(key=float))

        def headSort(self, data):

            return
            # parse the HEAD line

            # Code From Chris Coakley stupid_server.py


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

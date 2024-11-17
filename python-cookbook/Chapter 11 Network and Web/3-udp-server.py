from socketserver import BaseRequestHandler, UDPServer
import time

"""
Simple UDP time Server
"""


class TimeHandler(BaseRequestHandler):
    def handle(self):
        print("Got connection from: ", self.client_address)

        msg, sock = self.request
        print("Message ", msg)
        resp = time.ctime()

        sock.sendto(resp.encode("ascii"), self.client_address)


serv = UDPServer(("", 20000), TimeHandler)
serv.serve_forever()

"""
Client interactionn
"""

from socket import socket, AF_INET, SOCK_DGRAM

client_sock = socket(AF_INET, SOCK_DGRAM)
client_sock.sendto(b"Hello from client", ("localhost", 20000))

client_sock.recvfrom(8192)


"""
The UDPServer class is single threaded,
which means that only one request can be serviced at a time.

if you want concurrent operation,
instantiate a ForkingUDPServer or ThreadingUDPServer object instead:
"""


from socketserver import ThreadingUDPServer

t_serv = ThreadingUDPServer(("", 20001), TimeHandler)
t_serv.serve_forever()


"""
Implementing UDP server using sockets
"""


from socket import socket, AF_INET, SOCK_DGRAM


def time_server(address):
    sock = socket(AF_INET, SOCK_DGRAM)
    sock.bind(address)

    while True:
        msg, addr = sock.recvfrom(8192)
        print(f"Got message from {addr}")

        resp = time.ctime()
        sock.sendto(resp.encode("ascii"), addr)


time_server(("", 20002))

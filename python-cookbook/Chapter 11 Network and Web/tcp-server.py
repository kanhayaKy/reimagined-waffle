from socketserver import (
    BaseRequestHandler,
    TCPServer,
    ThreadingTCPServer,
    StreamRequestHandler,
)


class EchoHandler(BaseRequestHandler):
    def handle(self):
        print("Got connection from ", self.client_address)

        while True:
            msg = self.request.recv(8192)

            if not msg:
                break

            self.request.send(msg)


# if __name__ == "__main__":
#     server = ThreadingTCPServer(("", 20000), EchoHandler)
#     server.serve_forever()


"""
One issue with forking and threaded servers is that they spawn a new process or thread
on each client connection. There is no upper bound on the number of allowed clients,
so a malicious hacker could potentially launch a large number of simultaneous con‐
nections in an effort to make your server explode.

Solution : use a threaded pool of servers
"""

if __name__ == "__main__":
    TCPServer.allow_reuse_address = (
        True  # Allow server to rebind to previously used port number
    )

    from threading import Thread

    N_WORKERS = 16
    serv = TCPServer(("", 20000), EchoHandler)

    for n in range(N_WORKERS):
        t = Thread(target=serv.serve_forever)
        t.damon = True
        t.start()

    serv.serve_forever()

"""
The StreamRequestHandler class is actually a bit more flexible,
and supports some features that can be enabled through the specification
of additional class variables.
"""


class StreamEchoHandler(StreamRequestHandler):
    # Optional settings (defaults shown)
    timeout = 5 # Timeout on all socket operations
    rbufsize = -1 # Read buffer size
    wbufsize = 0 # Write buffer size
    disable_nagle_algorithm = False  # Sets TCP_NODELAY socket option

    def handle(self):
        print("Got connection from :", self.client_address)

        try:
            for line in self.rfile:
                self.wfile.write(line)
        except socket.timeout:
            print("Timed out!")



"""
Implementing socket server
"""


from socket import socket, AF_INET, SOCK_STREAM

def handler(address, client_sock):
    print(f'Got connection from {address}')

    while True:
        msg = client_sock.recv(8192)
        if not msg:
            break

        client_sock.sendall(msg)
    client_sock.close()


def echo_server(address, backlog=5):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind(address)
    sock.listen(backlog)

    while True:
        client_sock, client_addr = sock.accept()


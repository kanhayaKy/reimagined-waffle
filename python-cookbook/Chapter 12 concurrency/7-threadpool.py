"""
Notes:

1. Avoid writing programs that allow unlimited growth in the number of threads
2. By using a pre-initialized thread pool, you can carefully put an upper limit on the amount of supported concurrency.
3. you only want to use thread pools for I/O-bound processing.
"""

"""
Creating a pool of workers
"""


from socket import AF_INET, SOCK_STREAM, socket
from concurrent.futures import ThreadPoolExecutor


def echo_client(sock, client_addr):
    """
    Handle a client connection
    """

    print("Got connection from ", client_addr)

    while True:
        msg = sock.recv(65536)
        if not msg:
            break

        sock.sendall(msg)

    print("Client closed connection")
    sock.close()


def echo_server(addr):
    pool = ThreadPoolExecutor(128)
    sock = socket(AF_INET, SOCK_STREAM)

    sock.bind(addr)
    sock.listen(5)

    print("Started server at ", sock.getsockname())

    while True:
        client_sock, client_addr = sock.accept()
        pool.submit(echo_client, client_sock, client_addr)


# echo_server(('', 18000))


"""
Creating manual threadpool using queue
"""

from queue import Queue
from threading import Thread


def echo_client_man(q):
    sock, client_addr = q.get()

    print("Got connection from ", client_addr)
    while True:
        msg = sock.recv(65536)
        if not msg:
            break
        sock.sendall(msg)
    print("Client closed connection")


def echo_server_man(addr, nworkers):
    q = Queue()

    for n in range(nworkers):
        t = Thread(target=echo_client_man, args=(q,))
        t.daemon = True
        t.start()

    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind(addr)
    sock.listen(5)

    print("Starting manual echo server ", sock.getsockname())
    while True:
        client_sock, client_addr = sock.accept()
        q.put((client_sock, client_addr))


echo_server_man(("", 15000), 50)


"""
Advantage of threadpool : Easier to receive results

"""

from concurrent.furtures import ThreadPoolExecutor
import request


def fetch_url(url):
    resp = request.get(url)
    data = resp.text()

    return data


pool = ThreadPoolExecutor(10)

a = pool.submit(fetch_url, "http://www.python.org")
b = pool.submit(fetch_url, "http://www.pypy.org")

x = a.result()  # This line is blocked until 'a' is executed by the pool
y = b.result()


"""
Sample Runner code
"""


def client_send_req(message):
    sock = socket()
    sock.connect(("", 15000))
    sock.sendall(message.encode("ascii"))
    data = sock.recv(1696)
    print("Received from server ", data.decode())
    sock.close()


from threading import Thread

for i in range(10):
    message = f"hello for the {i}th time"
    t = Thread(target=client_send_req, args=(message,))
    t.daemon = True
    t.start()

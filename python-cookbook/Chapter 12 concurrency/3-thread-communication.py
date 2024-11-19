# Problem : You have multiple threads in your program and you want to safely communicate or exchange data between them.

"""
Solution : Using Queue
Queue instances already have all of the required locking,
so they can be safely shared by as many threads as you wish

When using queues, it can be somewhat tricky to coordinate the shutdown of the pro‐
ducer and consumer. A common solution to this problem is to rely on a special sentinel
value, which when placed in the queue, causes consumers to terminate.
"""

from queue import Queue
from threading import Thread


_sentinel = object()

def producer(out_q):
    """
    Produces data
    """

    n_worker = 10
    while n_worker > 0:
        print("Producing worker - ", n_worker)
        out_q.put(n_worker)
        n_worker -= 1

    out_q.put(_sentinel)


def consumer(in_q):
    """
    Consumes the data
    """

    while True:
        data = in_q.get()

        if data is _sentinel:
            in_q.put(data)
            break

        print("Consuming worker - ", data)


# Create the shared queue and launch both threads
q = Queue()
t1 = Thread(target=consumer, args=(q,))
t2 = Thread(target=producer, args=(q,))
t1.start()
t2.start()
# Wait for all produced items to be consumed
q.join()

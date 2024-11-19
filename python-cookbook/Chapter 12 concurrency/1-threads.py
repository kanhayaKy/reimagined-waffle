# Starting and stopping threads

import time

def countdown(n):
    while n > 0:
        print('T-minus', n)
        n -= 1
        time.sleep(5)


from threading import Thread

th = Thread(target=countdown, args(10,))
th.start()


if th.is_alive():
    print("Thread is Running")
else:
    print("Thread has finished")


# You can also request to join with a thread, which waits for it to terminate:
th.join()

# For long-running threads or background tasks that run forever,
# Daemonic threads can’t be joined.
# However, they are destroyed automatically when the main thread terminates.

th = Thread(target=countdown, args=(4,), daemon=True)
th.start()



"""
Due to a global interpreter lock (GIL), Python threads are restricted to an execution
model that only allows one thread to execute in the interpreter at any given time. For
this reason, Python threads should generally not be used for computationally intensive
tasks where you are trying to achieve parallelism on multiple CPUs. They are much
better suited for I/O handling and handling concurrent execution in code that performs
blocking operations (e.g., waiting for I/O, waiting for results from a database, etc.).
"""

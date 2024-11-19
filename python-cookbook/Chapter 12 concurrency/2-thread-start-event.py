# You’ve launched a thread, but want to know when it actually starts running.

from threading import Thread, Event, Semaphore
import time

def countdown(n, started_event):
    print("Starting countdown")
    started_event.set()

    while n > 0:
        print('T-minus', n)
        n -= 1
        time.sleep(5)


# Create an event
started_event = Event()

print("Launching countdown thread")
th = Thread(target=countdown, args=(10, started_event))
th.start()

# Wait for the thread to start
started_event.wait()
print("Countdown in running!")


""""
A critical feature of Event objects is that they wake all waiting threads. If you are writing
a program where you only want to wake up a single waiting thread, it is probably better
to use a Semaphore or Condition object instead
"""

def worker(n, semaph):
    semaph.acquire()

    print("Working.. ", n)


semaph = Semaphore(0)

n_workers = 10

for i in range(n_workers):
    t = Thread(target=worker, args=(i, semaph))
    t.start()


for i in range(n_workers):
    print("Releasing semaphore attempt -", i)
    semaph.release()



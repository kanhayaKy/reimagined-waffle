# Your program uses threads and you want to lock critical sections of code to avoid race conditions

"""
A Lock guarantees mutual exclusion when used with the with statement—that is, only
one thread is allowed to execute the block of statements under the with statement at a
time. The with statement acquires the lock for the duration of the indented statements
and releases the lock when control flow exits the indented block.
"""

import threading

class SharedCounter:
    def __init__(self, init_value):
        self._value = init_value
        self._value_lock = threading.Lock()


    def incr(self, delta=1):
        with self._value_lock:
            self._value += delta


    def decr(self, delta=1):
        with self._value_lock:
            self._value -= delta

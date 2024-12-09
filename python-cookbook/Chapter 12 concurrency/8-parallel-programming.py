'''
You have a program that performs a lot of CPU-intensive work, and you want to make
it run faster by having it take advantage of multiple CPUs.

'''


# Typical usage of a ProcessPoolExecutor is as follows:

from concurrent.futures import ProcessPoolExecutor

with ProcessPoolExecutor() as pool:
    # Do some work
    pass


'''
Notes:
1. ProcessPoolExecutor creates N independent running python interpreters
    where N is the number of available CPUs detected on the system
2. ProcessPoolExecutor(N) : To change the number of processes
3. Pool wait until last statement of 'with' block is executed
4. Program waits until all submitted work has been processed
5. Work to be submitted to a pool must be defined in functions.
    There are two methods for submission a) pool.map() b) pool.submit()
'''

def work(x):
    result = x%2
    return result

data = [n for n in range(1000)]

# Non parallel code
results = map(work, data)

# Parallel code
with ProcessPoolExecutor() as pool:
    results = pool.map(work, data)


# Manual submission
with ProcessPoolExecutor() as pool:
    future_result = pool.submit(work, 100)
    result = future_result.result() # Blocks until the result is computed and returned by the pool.


# Manual submission alt
def when_done(r):
    print('Got: ', r.result())

with ProcessPoolExecutor() as pool:
    for num in data:
        future_result = pool.submit(work, 100)
        future_result.add_done_callback(when_done)

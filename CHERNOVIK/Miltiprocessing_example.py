import multiprocessing
import time
import os
import time
import datetime


def worker(args):
    result = args[0]
    for x in range(10000):
        for y in range(1000):
            result = result + x * y
    print('result ', result)
    return result



if __name__ == '__main__':
    timer = time.time()

    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    print('pool result ', pool.map(worker, [(0,), (1,), (2,), (3,), (4,), (5,), (6,), (7,)]))
    print(time.time()-timer)
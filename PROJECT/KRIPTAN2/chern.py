from PROJECT.SBOR.my_lib import *
# from datetime import datetime
# import ntplib
# from time import ctime
# c = ntplib.NTPClient()
# response = c.request('pool.ntp.org')
# t= ctime(response.tx_time)
# print(t)
import os

from time import time
import numpy as np
from numba import njit

# Pure Python version:
@njit
def mean_distance_from_zero(arr):
    total = 0
    for i in range(len(arr)):
        total += abs(arr[i])
    return total / len(arr)

# A fast, JITed version:
# mean_distance_from_zero_numba = njit(
#     mean_distance_from_zero
# )

arr = np.array(range(100), dtype=np.float64)
# arr=[1,2,3,4,5,6,7,8,9,10]
# arr=list(range(100))
print(arr)

start = time()

for i in range(3):
    start = time()
    mean_distance_from_zero(arr)
    print("Elapsed Numba:   ", time() - start)
	

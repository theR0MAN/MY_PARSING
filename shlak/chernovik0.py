import os
from platform import system
import multiprocessing
val = multiprocessing.Value('d', 10)
a=val.value
print(a)
val.value = val.value - 1
# a = val.value
print(a)

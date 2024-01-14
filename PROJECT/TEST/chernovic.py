from statistics import mean
import numpy as np
import random


import time
inp_lst = []
for i in range (1000000):
	inp_lst.append(random.randint(0,100000))

timer=time.time()
avg = mean(inp_lst)
print(time.time()-timer)
timer=time.time()
# avgs = sorted(inp_lst)
inp_lst.sort(reverse=True)
print(time.time()-timer)


timer=time.time()
avg2 = np.mean(inp_lst)
print(time.time()-timer)







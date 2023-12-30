import time
from my_lib import *

# возвращает из редис словарь биржа инструмент -стакан


dct=myload('G:\\DATA_SBOR\\KRIPTA\\ASYMBOLS_INFO\\log.roman')




while True:
	time.sleep(1)
	timer = time.time()
	a= mycontget(dct)
	for ex in a:
		print(ex,len(a[ex]),a[ex])
	print(time.time()-timer)
import time
from my_lib import *
# dct=myload('G:\\DATA_SBOR\\KRIPTA\\ASYMBOLS_INFO\\log.roman')

dct=myredget('conainer')
print(len(dct),dct)
for ex in dct:
	print(ex,len(dct[ex]),dct[ex])

# #
while True:
	time.sleep(1)
	timer = time.time()
	a= mycontget(dct)
	for ex in a:
		print(ex, len(a[ex]), a[ex])
		for sym in a[ex]:
			if a[ex][sym]==None:
				print(a,ex,sym,' NONE')

		# for stk in a[ex]:
		# 	if stk==None:
		# 		print(ex, len(a[ex]), a[ex])

		# print(ex,len(a[ex]),a[ex])
	# print(time.time()-timer)
import time

from PROJECT.my_lib import *


dct=myload('G:\\DATA_SBOR\\KRIPTA\\ASYMBOLS_INFO\\log.roman')

r=redis.Redis(db=1)
def myredget(key):
	if r.exists(key):
		return pickle.loads(r.get(key))
	else:
		return None

for ex in dct:
	print(ex, dct[ex])

while True:
	time.sleep(1)
	timer = time.time()
	for ex in dct:
		for sym in dct[ex]:
			s=myredget(sym + '*' + ex )
			# print(sym + '*' + ex, myredget(sym + '*' + ex))
	print(time.time()-timer)


import time

import redis
import pickle

# возвращает из редис словарь биржа инструмент -стакан

r = redis.Redis(db=1)
x= redis.Redis(db=1)



def myredput(ex,key, data):
	ex.set(key, pickle.dumps(data))

def myredget(ex,key):
	if ex.exists(key):
		return pickle.loads(r.get(key))
	else:
		return None



myredput(r,'i', 15)
myredput(x,'i', 20)

print(myredget(r,'i'))
print(myredget(x,'i'))

time.sleep(20)
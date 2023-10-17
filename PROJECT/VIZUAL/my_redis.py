from statistics import mean
import time
import redis



# redis_client=redis.Redis(host='localhost',port=6379,db=0)
# client=redis.Redis()
#
# print(client.set('test',10) )
#
# x=client.get('test')
#
# print(x)
# z=int(x)+12
# print(z)
#
# client.close()



with redis.Redis() as client:
	client.set('count',1)
	while True:
		client.incrby('count',10)
		time.sleep(1)

		c=client.get('count')
		print(c)
		print(int(c))


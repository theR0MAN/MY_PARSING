from threading import Thread
import time

def count(txt):
	for x in range(5):
		time.sleep(1)
		print(x,txt)

def count2():
	for x in range(5):
		time.sleep(1)
		print('hty  ',x)

def ts1():
	Thread(target=count, args=('first',)).start()


def ts2():
	Thread(target=count2).start()



print('пошла жара')

ts1()
ts2()
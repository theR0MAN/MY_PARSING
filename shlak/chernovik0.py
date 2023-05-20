from multiprocessing import Process ,freeze_support
import  time
from threading import Thread

def disp(name):
	for x in range (5) :
		time.sleep(1)
		print(name,"  ",x)


def startt(name):
	print("__name__ ==  ",__name__)
	# if __name__ == '__main__':
	freeze_support()
	Process(target=disp,args=(name,)).start()



# startt("first")
# startt("second")



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


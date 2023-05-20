# from chernovik9 import *

from multiprocessing import Process
import time



def count(txt):
	for x in range(5):
		time.sleep(1)
		print(x, '   ', txt)


def proc():
	if __name__ == '__main__':
		Process(target=count, args=('first1',)).start()
		Process(target=count, args=('first2',)).start()
		Process(target=count, args=('first4',)).start()
		Process(target=count, args=('first5',)).start()
		Process(target=count, args=('first6',)).start()
		Process(target=count, args=('first7',)).start()
		Process(target=count, args=('first8',)).start()
		Process(target=count, args=('first9',)).start()
		Process(target=count, args=('first10',)).start()


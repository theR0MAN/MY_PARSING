# from chernovik0 import *
import time

#
# ts1()
# ts2()
#
# print(' dont wait')

from multiprocessing import Process


def count(txt):
	for x in range(5):
		time.sleep(1)
		print(x, '   ', txt)


def loop_b():
	while 1:
		print("b")


if __name__ == '__main__':
	Process(target=count, args=('first1',)).start()
	Process(target=count, args=('first2',)).start()
	Process(target=count, args=('first3',)).start()
	Process(target=count, args=('first4',)).start()
	Process(target=count, args=('first5',)).start()
	Process(target=count, args=('first6',)).start()
	Process(target=count, args=('first7',)).start()
	Process(target=count, args=('first8',)).start()
	Process(target=count, args=('first9',)).start()
	Process(target=count, args=('first10',)).start()
	Process(target=count, args=('first11',)).start()
	Process(target=count, args=('first12',)).start()
	Process(target=count, args=('first13',)).start()
	Process(target=count, args=('first14',)).start()
	Process(target=count, args=('first15',)).start()
	Process(target=count, args=('first16',)).start()
	Process(target=count, args=('first17',)).start()
	Process(target=count, args=('first18',)).start()
	Process(target=count, args=('first19',)).start()
	Process(target=count, args=('first20',)).start()


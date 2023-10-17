
from multiprocessing import Process,Queue
from  queue import Empty
from time import sleep


def worker (q):
	cnt=0
	while cnt<3:
		sleep(.1)
		q.put(cnt)
		cnt+=1
	print(' W1 end')


def worker2 (q):
	cnt=0
	while cnt<3:
		sleep(.1)
		cnt+=1
	print(' W2 end')




if __name__ == '__main__':
	q=Queue()
	p=	Process(target=worker,args=(q,))
	p.start()
	p.join()

	while not q.empty():
		print(q.get())
		p = Process(target=worker2, args=( q,))
		p.start()
		p.join()


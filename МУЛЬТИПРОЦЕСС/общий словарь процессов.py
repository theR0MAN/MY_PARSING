from multiprocessing import Process, Manager
import  time
# SyncManager



def f(d, key, zn):
	d[key] = zn
	d[key*20] = zn*2


if __name__ == '__main__':
	manager = Manager()
	d = manager.dict()
	d[0] = 1
	d[1] = 2

	p1 = Process(target=f, args=(d, 3, 7))
	p2 = Process(target=f, args=(d, 6, 8))
	print(d)
	p1.start()
	time.sleep(1)
	print(d)

	p2.start()
	print(d)
	p1.join()
	p2.join()

	p1.close()
	p2.close()

	print(d)

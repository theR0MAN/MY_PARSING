from multiprocessing import Pool,Process
import time


def F(x):
	z = x**4000000
	return x


if __name__ == '__main__':

	l = [10, 9, 8, 7, 6, 5, 4, 3]

	timer = time.time()
	z = list(map(F, l))
	print(time.time() - timer)

	timer = time.time()
	p = Process(target=F, args=(10, ))
	print('work0')
	p.start()
	
	print(time.time() - timer)
	print('work')

	p.join()
	p.close()
	print(time.time() - timer)
	print('End program')
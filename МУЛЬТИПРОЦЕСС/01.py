from multiprocessing import Pool,Process,Queue
import time


def F(x):
	z = x[0] ** 2000000
	return dict([(x[0],x[1])])


if __name__ == '__main__':

	l = [[1,2], [3,4], [5,6], [7,8],[9,10]]

	timer = time.time()
	z = list(map(F, l))
	print(z)
	print(time.time() - timer)

	timer = time.time()
	with Pool(processes=8) as pool:
		results = pool.map(F, l)
	print(results)
	print(time.time() - timer)

	print('End program')
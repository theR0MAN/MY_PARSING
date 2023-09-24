from multiprocessing import Pool,Process
import time


def F(x):
	z = x ** 4000000
	return x


if __name__ == '__main__':

	l = [10, 9, 8, 7, 6, 5, 4, 3]

	timer = time.time()
	z = list(map(F, l))
	print(time.time() - timer)

	timer = time.time()
	with Pool(processes=8) as pool:
		results = pool.map(F, l)
		print(results)


	print(time.time() - timer)
	print('End program')


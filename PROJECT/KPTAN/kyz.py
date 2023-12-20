from multiprocessing import Process

import time




def exp (num):
	start = time.time()
	for i in range (70):
		time.sleep(0.01)
		# a=1000000*1000000**100
	stop = time.time()
	print(num,'   ',stop - start)





if __name__ == "__main__":
	for n in range(70):
		Process(name='worker ' + str(n), target=exp, args=(n,)).start()
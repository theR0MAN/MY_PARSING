from MAIN.DATA import moexsbor
from multiprocessing import Process


if __name__ == '__main__':
	process1 = Process(target=moexsbor)
	process1.start()
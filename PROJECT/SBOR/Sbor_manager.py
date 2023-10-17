from Sbor_write_lib import Compress
from Sbor_moex_mt5 import moexsbor
from multiprocessing import Process,Queue
from time import sleep


if __name__ == '__main__':
	Process(target=Compress).start()


	Process(target=moexsbor).start()


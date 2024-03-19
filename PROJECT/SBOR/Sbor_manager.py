from Sbor_write_lib import Compress
from Sbor_moex_mt52 import moexsbor
from sbor_forex import forexsbor
from PROJECT.KRIPTAN2.my_kriptosbor  import mykriptosbor
from multiprocessing import Process,Queue
# from time import sleep
QE = Queue()

if __name__ == '__main__':
	Process(target=Compress,args=(QE,)).start()
	# Process(target=moexsbor,args=(QE,)).start()
	# Process(target=forexsbor,args=(QE,)).start()
	Process(target=mykriptosbor, args=(QE,)).start()


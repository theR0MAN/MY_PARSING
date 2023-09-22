from Sbor_moex_mt5 import moexsbor
from multiprocessing import Process


if __name__ == '__main__':
	Process(target=moexsbor).start()
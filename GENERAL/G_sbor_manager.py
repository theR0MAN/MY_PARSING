from G_MT5_moex_sbor import moexsbor
from multiprocessing import Process


if __name__ == '__main__':
	Process(target=moexsbor).start()

	
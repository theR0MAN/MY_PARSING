import datetime
import time

from  Sbor_write_lib import Histwrite2
from my_lib import *
# from multiprocessing import Process,Queue
# QE = Queue()

def kriptosbor(QE):
	time.sleep(300)
	putpath = 'G:\\DATA_SBOR\\KRIPTA'
	dct = myload('G:\\DATA_SBOR\\KRIPTA\\ASYMBOLS_INFO\\log.roman')
	print(' запуск kriptosbor')
	Sbor=dict()
	for ex in dct:
		Sbor[ex] =Histwrite2(putpath, ex, QE)
		print(ex,len (dct[ex]))
	tm0 = time.time()
	dat = datetime.datetime.utcfromtimestamp(time.time())
	day0 = dat.day
	while True:
		time.sleep(0.01)
		tm = time.time()
		if tm0 + 1 <= tm:

			tm0 = tm
			dat = datetime.datetime.utcfromtimestamp(time.time())
			day=dat.day
			mnt=dat.minute
			if day0!=day and mnt>10:
				dct = myload('G:\\DATA_SBOR\\KRIPTA\\ASYMBOLS_INFO\\log.roman')
				day0 = day
				print('day0!=day and mnt>5 MANAGER')
			a = mycontget(dct)
			for ex in a:
				# print(ex)
				for sym in a[ex]:
					stk=a[ex][sym]
					Ask = stk['asks'][0][0]
					Bid = stk['bids'][0][0]
					zaderzka=stk['zad']
					timestamp = stk['timestamp']
					askbid = [Ask, Bid, timestamp, zaderzka]
					Sbor[ex].putter(sym , askbid, stk)


# kriptosbor(QE)
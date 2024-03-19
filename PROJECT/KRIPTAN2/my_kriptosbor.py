import datetime
import time
from  PROJECT.SBOR.Sbor_write_lib import Histwrite2
from PROJECT.SBOR.my_lib import *


def mykriptosbor(QE):
	time.sleep(60)
	putpath = 'G:\\NEWKRIPT'
	dct = myredget('conainer')
	print(' запуск kriptosbor')
	Sbor=dict()
	for ex in dct:
		Sbor[ex] =Histwrite2(putpath, ex, QE)
		print(ex,len (dct[ex]))
	tm0 = time.time()
	while True:
		time.sleep(0.01)
		tm = time.time()
		if tm0 + 1 <= tm:
			tm0 = tm
			a = mycontget(dct)
			for ex in a:
				for sym in a[ex]:
					stk=a[ex][sym]
					Sbor[ex].kriptoputter(sym, stk)

import  ccxt
import ccxt.pro 
import os ,datetime
import time
from PROJECT.my_lib import *
errors=[]

myexs={}
exch = ccxt.pro.exchanges
for ex in exch:
	print(ex)
	try:
		birza = getattr (ccxt, ex) ()
		markets =  birza.load_markets()
		myexs[ex]=markets
	except:
		errors.append(ex)
		print(ex, 'ERROR')


print(errors)
dat = datetime.datetime.utcfromtimestamp(int(time.time()))
year = dat.year
day = dat.day
putpath = 'G:\\DATA_SBOR'
pth = putpath + '\\ASYMBOLS_INFO'
if not os.path.exists(pth):
	os.mkdir(pth)
pth = pth + '\\' + str(dat.year)
if not os.path.exists(pth):
	os.mkdir(pth)
pth = pth + '\\' + str(dat.month)
if not os.path.exists(pth):
	os.mkdir(pth)
infoname = pth + '\\' + str(dat.day) + '-' + 'Kriptoinf.roman'
if not os.path.exists(infoname):
	myput(infoname,myexs)


import  asyncio
import time
import os
import datetime
import ccxt.pro as ccxt
from PROJECT.SBOR.my_lib import *



def markload(flaghard=False):
	print(' старт функции markload с параметром flaghard=',flaghard)
	loadset = set()
	async def lm(ex):
		birza = getattr(ccxt, ex)()
		try:
			markets = await birza.load_markets(True)
			loadset.add(ex)
			myexs[ex] = markets
			await birza.close()
		except Exception:
			await birza.close()

	myexs = dict()
	dat = datetime.datetime.utcfromtimestamp(int(time.time()))
	pth = 'G:\\SYMBOLS_INFO\\KRIPTASYMBOLS_INFO'
	if not os.path.exists(pth):
		os.mkdir(pth)
	pth = pth + '\\' + str(dat.year)
	if not os.path.exists(pth):
		os.mkdir(pth)
	pth = pth + '\\' + str(dat.month)
	if not os.path.exists(pth):
		os.mkdir(pth)
	infoname = pth + '\\' + str(dat.day) + '.roman'
	if not os.path.exists(infoname) or flaghard:
		async def main():
			print('идет загрузка рынков')
			for i in range(5):
				tasks = []
				for ex in ccxt.exchanges:
					if ex not in loadset:
						tasks.append(lm(ex))
						# print('попытка',i, "  загрузка маркета ", ex)
				if tasks != []:
					await  asyncio.gather(*tasks)
					time.sleep(2)
				else:
					break
			notload=[]
			for ex in ccxt.exchanges:
				if ex not in loadset:
					notload.append(ex)
			print('загрузились рынки - ',loadset)
			print('Не загрузились рынки - ', notload)

		asyncio.run(main())
		print('запись в файл ', infoname)
		myput(infoname, myexs)

	else:
		print(" файл  существует - загружаем ", infoname)
		myexs = myload(infoname)
		z=list(myexs)
		print('  полученные  рынки -',z)
	print(' завершение работы markload')
	return myexs


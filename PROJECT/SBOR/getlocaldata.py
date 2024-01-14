import  asyncio
import time
import os
import datetime
import ccxt.pro as ccxt
from my_lib import *


# minpovtinst=25  #  убрать инструменты, которые повторяются меньше чем на minpovtinst рынках
# minkinstbirz=40   # убрать биржи, на которых оставшихся инструментов меньше  minkinstbirz
# topsyms=50# оставить в итоге символы из топа в количестве не более  topsyms
# flaghard   -всегда грузить рынки вне зависимости от наличия файла
# all,onlyfut, -список бирж, обязательныx для загрузки , если пусто - то грузить макс
# all- все
# onlyfut-только фьючи

def rez_dict(minkinstbirz,topsyms,all,onlyfut,flaghard=False):
	minpovtinst=len(all)+len(onlyfut) -1
	loadset = set()
	def markload():
		async def lm(ex):
			birza = getattr(ccxt, ex)()
			try:
				markets = await birza.load_markets()
				loadset.add(ex)
				myexs[ex] = markets
				# print(ex)
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
			print('запись в файл ',infoname)
			async def main():
				for i in range(4):
					tasks = []
					nessex=all+onlyfut
					for ex in nessex:
						if ex not in loadset:
							tasks.append(lm(ex))
							print(i, " GO LAST", ex)
					if tasks != []:
						await  asyncio.gather(*tasks)
						time.sleep(2)
					else:
						break

			asyncio.run(main())
			myput(infoname,myexs)

		else:
			print ("LOAD ",infoname)
			myexs=myload(infoname)
		return myexs
	a=markload()
	def take_dat(data):
		def func_sort (a,spi):
			rez=[]
			for kr in a:
				for insr in spi:
					z = insr.partition('/')[0]
					if z== kr:
						rez.append(insr)
			return  rez
		setopt=set()
		couninst=dict()
		rezdat=dict()
		for ex in data:
			rezdat[ex]=[]
			for sym in data[ex]:
				if '/USDT' in sym and ('-C'  in sym or'-P'  in sym) and data[ex][sym]['active'] == True:
					setopt.add(ex)
				if '/USDT' in sym and '-C'not in sym and '-P'not in sym and data[ex][sym]['active']==True:
					rezdat[ex].append(sym)
					a=sym.partition('/')[0]
					if a in couninst:
						couninst[a]+=1
					else:
						couninst[a]=1
		symset=set()
		couninstrez=dict()
		for sym in couninst:
			if couninst[sym]>=minpovtinst:
				couninstrez [sym]= couninst[sym]
				symset.add(sym)
		couninstrez=mysortdict(couninstrez)
		#
		count=0
		couninstreztopset=set()
		for sym in couninstrez:
			count+=1
			if  count>topsyms:
				break
			else:
				couninstreztopset.add(sym)
		rezdat=dict()
		for ex in data:
			rezdat[ex]=[]
			for sym in data[ex]:
				if '/USDT' in sym and '-C'not in sym and '-P'not in sym and data[ex][sym]['active']==True:
					a=sym.partition('/')[0]
					if a in couninstreztopset:
						rezdat[ex].append(sym)
			if len(rezdat[ex])<minkinstbirz:
				del rezdat[ex]
		rb=dict()
		for ex in rezdat:
			rb[ex]=len(rezdat[ex])
		rb=mysortdict(rb)
		itog=dict()
		for ex in rb:
			itog[ex] =func_sort (couninstrez,rezdat[ex])
		countfut=dict()
		for ex in itog:
			countfut[ex]=0
			for sym in itog[ex]:
				if ":USDT" in sym:
					countfut[ex]+=1
			if countfut[ex]==0:
				del countfut[ex]
		countfut=mysortdict(countfut)
		countspot=dict()
		for ex in itog:
			countspot[ex]=0
			for sym in itog[ex]:
				if ":USDT" not in sym:
					countspot[ex]+=1
				else:
					del countspot[ex]
					break
			if ex in countspot:
				if countspot[ex] == 0:
					del countspot[ex]
		countspot=mysortdict(countspot)
		print('kvo birz ',len(data))
		# рейтинг символов
		print(len(couninstrez),couninstrez)
		# рейтинг бирж
		print('all exc',len(rb),rb)
		# рейтинг бирж по фьючам
		print('futures ',len(countfut),countfut)
		# рейтинг бирж onlyspot
		print('onlyspot',len(countspot),countspot)
		print("option markets  ",setopt)
		return itog
	itog=take_dat(a)

	putpath2 = 'G:\\SYMBOLS_INFO\\KRIPTASYMBOLS_INFO\\log.roman'
	A = dict()
	for ex in all:
		if ex in itog:
			A[ex] = itog[ex]

	for ex in onlyfut:
		if ex in itog:
			A[ex] = []
			for sym in itog[ex]:
				if ":USDT" in sym:
					A[ex].append(sym)
	myput(putpath2,A)

	aa = myload(putpath2)
	for ex in aa:
		print(ex,aa[ex])
	return itog


# all0 = ('bingx', 'whitebit','bitfinex2',)
# onlyfut0 = ('bybit', 'binance', 'huobi', 'binanceusdm',)
# MY=rez_dict(20,50,all0,onlyfut0,True)

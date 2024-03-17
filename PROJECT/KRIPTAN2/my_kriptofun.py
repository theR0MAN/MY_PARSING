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
# allbases  False - только по базам USDT
def myinfo(flaghard=False,allbases=True):
	''' возвращает список баз символов с убыванием популярности '''
	print(' старт функции myinfo flaghard=', flaghard," allbases=",allbases)


	a = markload(flaghard)
	myhas=dict()
	for exch in a:
		myhas[exch]=dict()
		myhas[exch]['spot']=0
		myhas[exch]['swap'] = 0
		myhas[exch]['future'] = 0
		myhas[exch]['option'] = 0
		exchange = getattr(ccxt, exch)()
		if exchange.has['watchOrderBookForSymbols']:
			myhas[exch]['watchOrderBookForSymbols']=True
		else:
			myhas[exch]['watchOrderBookForSymbols'] = False

		for sym in a[exch]:
			if a[exch][sym]['active'] == True:
				if a[exch][sym]['type'] == 'spot':
					myhas[exch]['spot']+=1
				elif a[exch][sym]['type'] == 'swap':
					myhas[exch]['swap']+=1
				elif a[exch][sym]['type'] == 'future':
					myhas[exch]['future']+=1
				elif a[exch][sym]['type'] == 'option':
					myhas[exch]['option']+=1

	# print(' подробно по маркетам :')
	# for exch in myhas:
	# 	print(exch,myhas[exch])

	print(' биржи с watchOrderBookForSymbols:')
	for exch in myhas:
		if myhas[exch]['watchOrderBookForSymbols']==True:
			print(exch,myhas[exch])
	print(' биржи с option:')
	for exch in myhas:
		if myhas[exch]['option']>0:
			print(exch,myhas[exch])
	print(' биржи с future:')
	for exch in myhas:
		if myhas[exch]['future']>0:
			print(exch,myhas[exch])
	print(' биржи с swap:')
	for exch in myhas:
		if myhas[exch]['swap']>0:
			print(exch,myhas[exch])
	print(' биржи с spot:')
	for exch in myhas:
		if myhas[exch]['spot']>0:
			print(exch,myhas[exch])


	baseset = set()
	filtr1 = dict()
	for exch in a:
		myhas[exch]=dict()
		filtr1[exch] = []
		for sym in a[exch]:
			if a[exch][sym]['active'] == True:
				if a[exch][sym]['type'] == 'spot' and (a[exch][sym]['quote'] == 'USDT'or allbases):
					baseset.add(a[exch][sym]['base'])
					filtr1[exch].append(sym)
				if a[exch][sym]['type'] == 'swap' and (a[exch][sym]['quote'] == 'USDT' and a[exch][sym]['settle'] == 'USDT' or allbases):
					baseset.add(a[exch][sym]['base'])
					filtr1[exch].append(sym)

	# рейтинг баз символов
	rsyms = dict()
	for sym in baseset:
		rsyms[sym] = dict()
		rsyms[sym] = 0

	for exch in filtr1:
		for sym in filtr1[exch]:
			base = sym.partition('/')[0]
			rsyms[base] += 1


	rsyms = mysortdict(rsyms)
	print(" рейтинг символов   по всем рынкам", rsyms)

	rz=[]
	for key in rsyms:
		if rsyms[key]>10:
			rz.append(key)
	print(len(rz),rz)



	print(' завершение работы myinfo')
	return a,rz
# minsyms - удаляем рынок (спот или своп) при количестве инструментов меньше этого параметра
# obrezsyms - сделано если пересечений слишком много и пк не тянет - режет топ символов до  obrezsyms
def myfiltr(myexchanges,minsyms,obrezsyms,flaghard=False):
	print(f' старт функции myfiltr  minsyms = {minsyms} flaghard= {flaghard}  myexchanges={myexchanges}')
	a,raiting=myinfo()

	rezset = set()
	b=dict()
	b['spot']=dict()
	b['swap']=dict()
	myhas = dict()
	myhas['spot']=dict()
	myhas['swap']=dict()
	#  оставим только мои биржи и фильтруем по базе USDT
	for exch in myexchanges:
		b['spot'] [exch]= []
		b['swap'] [exch]= []
		myhas['spot'][exch] = set()
		myhas['swap'][exch] = set()
		for sym in a[exch]:
			if a[exch][sym]['active'] == True:
				if a[exch][sym]['type'] == 'spot'and a[exch][sym]['quote'] == 'USDT':
					b['spot'][exch].append(sym)
					base = sym.partition('/')[0]
					myhas['spot'][exch].add(base )
					rezset.add(base)
				elif a[exch][sym]['type'] == 'swap'and a[exch][sym]['quote'] == 'USDT' and a[exch][sym]['settle'] == 'USDT':
					b['swap'][exch].append(sym)
					base=sym.partition('/')[0]
					myhas['swap'][exch].add(base)
					rezset.add(base)

	print(' удаление маркетов с к-вом символов меньше ',minsyms)
	for type in b:
		for ex in b[type]:
			if len(b[type][ex]) < minsyms:
				del myhas[type][ex]
				print('myhas del',type,ex, len(b[type][ex]))


	# работа с множествами  myhas
	print( ' рейтинг бирж исходя из количества пересечений с общим множеством символов')
	for type in myhas:
		for ex in myhas[type]:
			print(type,ex,len(rezset&myhas[type][ex]))

	print('было инструментов до пересечения множеств ',len(rezset))
	for type in myhas:
		for ex in myhas[type]:
			rezset=rezset&myhas[type][ex]
	print('осталось инструментов после пересечения множеств ',len(rezset),rezset)
	rz=[]
	cnt=0
	for bz in raiting:
		if bz in rezset:
			rz.append(bz)
			cnt+=1
		if cnt>=obrezsyms:
			print(' количество символов обрезано до ',cnt)
			break

	print('сортировка множества согласно рейтингу',len(rz),rz)

	def myfars(a):
		b = []
		ln = len(a)
		if int(ln / 2) == ln / 2:
			tp = 1
		else:
			tp = 2

		for i in range(int(ln / 2)):
			b.append(a[i])
			b.append(a[ln - 1 - i])
		if tp == 2:
			b.append(a[int(ln / 2)])
		return b

	rz=myfars(rz)
	# это нужно для кайфа по распределению нагрузки по ядрам
	print(' спайка -первое+последнее к центру,',rz)

	print(' получение итогового словоря словаря инструментов по рынкам по множеству')
	c=dict ()
	c['spot']=dict()
	c['swap']=dict()

	for type in b:
		for ex in b[type]:
			if ex in myhas[type]:
				c[type][ex]=[]
				for baza in rz:
					for sym in b[type][ex]:
						base = sym.partition('/')[0]
						if base ==baza:
							c[type][ex].append(sym)
							break
	for type in c:
		for ex in c[type] :
			print(ex,type,len(c[type][ex]),c[type][ex])

	print(' завершение работы myfiltr')
	return c

def getdepth(ex):
	#  глубины стаканов
	exchdepth = {}
	exchdepth['kucoinfutures'] = 20
	exchdepth['kraken'] = 10
	exchdepth['kucoin'] = 20
	exchdepth['bitfinex2'] = 25
	exchdepth['bitmex'] = None
	exchdepth['bitopro'] = None  # 5
	exchdepth['bitfinex'] = 25
	exchdepth['bingx'] = 20
	exchdepth['poloniexfutures'] = 5
	exchdepth['huobi'] = 20
	exchdepth['binanceusdm'] = 5
	exchdepth['binance'] = 5
	exchdepth['coinex'] = None
	exchdepth['bitrue'] = None
	exchdepth['bybit'] = 1  # 50
	exchdepth['others'] = 1
	if ex in exchdepth:
		depth = exchdepth[ex]
	else:
		depth = exchdepth['others']
	return depth

def getcorutine(kyader,kcorut,minsyms,obrezsyms,myexchanges,flaghard):
	'''

	:param kyader: на какое количество ядер расчитать нагрузку
	:param kcorut:  на это число дробится каждый маркет (своп, спот)
	:param minsyms:  если в маркете символов меньше этого числа, то он игнорируется
	:param obrezsyms:  если пересечений слишком много и пк не тянет - режет топ символов до  obrezsyms
	:param myexchanges: список бирж
	:param flaghard:  жестко загружать рынки вне зависимости от существования файла
	:return: корутины по ядрам
	'''
	print(' старт функции getcorutine')
	c = myfiltr(myexchanges,minsyms,obrezsyms,flaghard)


	corutins = {}
	corutins['swap'] = {}
	corutins['spot'] = {}

	corutins['swap']['bitmex'] = 10
	corutins['spot']['bybit'] = 10

	c2=dict()
	for type in c:
		c2[type] = dict()
		for ex in c[type]:
			c2[type][ex]=[]
			buf = []
			count = 0
			ln=len(c[type][ex])
			kvo =int(ln/kcorut)
			if ex in corutins[type]:
				kvo= min(kvo,corutins[type][ex])
				print(ex,type, corutins[type][ex],kvo)

			for sym in c[type][ex]:
				buf.append(sym)
				count += 1
				if count >= kvo:
					c2[type][ex].append(buf)
					buf = []
					count = 0
			if count > 0:
				c2[type][ex].append(buf)


	mycores=dict()
	for i in range(kyader):
		mycores[str(i+1)] =[]

	i=0
	for type in c2:
		for ex in c2[type]:
			exchange = getattr(ccxt, ex)()
			if(kyader ==kcorut):# будет ровней
				i = 0
			for corutine in c2[type][ex]:
				i+=1
				if i>kyader:
					i=1
				md = dict()
				md['exchange']=ex
				md['type'] = type
				if exchange.has['watchOrderBookForSymbols']:
					md['metod']='watchOrderBookForSymbols'
				else:
					md['metod'] = 'watchOrderBook'
				md['symbols'] = corutine
				mycores[str(i)].append(md)
	print('полученные корутины -')
	for core in mycores:
		print(core, len(mycores[core]), mycores[core])
	myput('corutines',mycores)
	return mycores
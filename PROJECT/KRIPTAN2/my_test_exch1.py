from  my_filter_instrs import  *
import time
import ccxt.pro as ccxt
import traceback
import asyncio


def getdepth(ex):
	if ex in exchdepth:
		depth = exchdepth[ex]
	else:
		depth = exchdepth['others']
	return depth

def getcor(type,ex):
	if ex in corutins[type]:
		cor = corutins[type][ex]
	else:
		cor = corutins[type]['others']
	return cor

flaghard=False
topsyms=50 #  ВЫБИРАЕМ первые  topsyms из списка самых популярных (по количеству баз  вкл спот и своп) символах на всех биржах
mininstr= int(topsyms/2)    # минимальное количество инструментов из topsyms на бирже, если меньше - биржа не включается в список на тест
testtime=60 #длительность теста

a=takefiltrinstrs(flaghard,topsyms,mininstr)

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
exchdepth['bybit']=1#50
exchdepth['others']=5

# разделение на корутины по к-ву элтов     # bitmex    bybit     ['swap']
corutins = {}
corutins['swap'] = {}
corutins['spot'] = {}

corutins['swap']['bitmex'] = 10
corutins['spot']['bybit'] = 10
corutins['swap']['others'] = max(int(topsyms/2)+1,10)
corutins['spot']['others'] = max(int(topsyms/2)+1,10)
# -------------------------------------------
# -------------------------------------------



testdict=dict()
testdict['spot']=dict()
testdict['swap']=dict()

#
# for ex in a['watchOrderBookForSymbols']:
# 	if a['watchOrderBookForSymbols'][ex]['swap']!=[]:
# 		testdict['swap'][ex]=a['watchOrderBookForSymbols'][ex]['swap']#[:30]
# 	if a['watchOrderBookForSymbols'][ex]['spot']!=[]:
# 		testdict['spot'][ex]=a['watchOrderBookForSymbols'][ex]['spot']#[:30]

for ex in a['watchOrderBookForSymbols']:
	if a['watchOrderBookForSymbols'][ex]['swap']!=[]:
		testdict['swap'][ex]=[]
		kvo= getcor('swap',ex)
		buf=[]
		count=0
		for sym in a['watchOrderBookForSymbols'][ex]['swap'][:2]:
			buf.append(sym )
			count+=1
			if count>=kvo:
				testdict['swap'][ex].append(buf)
				buf = []
				count = 0
		if count>0:
			testdict['swap'][ex].append(buf)

	if a['watchOrderBookForSymbols'][ex]['spot']!=[]:
		testdict['spot'][ex]=[]
		kvo= getcor('spot',ex)
		buf=[]
		count=0
		for sym in a['watchOrderBookForSymbols'][ex]['spot'][:2]:
			buf.append(sym )
			count+=1
			if count>=kvo:
				testdict['spot'][ex].append(buf)
				buf = []
				count = 0
		if count>0:
			testdict['spot'][ex].append(buf)


for ex in testdict['swap']:
	print(ex,'swap',testdict['swap'][ex])
for ex in testdict['spot']:
	print(ex,'spot',testdict['spot'][ex])

# quit()
	#
	# if a['watchOrderBookForSymbols'][ex]['spot']!=[]:
	# 	testdict['spot'][ex]=[]

rezdict=dict()
rezdict['spot']=dict()
rezdict['swap']=dict()


# mistakedict=dict()

for type in testdict:
	for ex in testdict[type]:
		rezdict[type][ex]=dict()
		rezdict[type][ex]['working']=False
		# rezdict[type][ex]['laststakan'] = None
		rezdict[type][ex]['misakes']= 0
		rezdict[type][ex]['zadtmstmp'] = [] #задержка по таймштампу
		rezdict[type][ex]['zadzapros'] = []  # задержка по запросу
		print(ex,type, len(testdict[type][ex]), testdict[type][ex])


# quit()


# 'timestamp': None, 'datetime': None,
# 'timestamp': 1709925130014, 'datetime': '2024-03-08T19:12:10.014Z', 'nonce': 44073107468, 'symbol': 'BTC/USDT'
timerall=time.time()
async def example(ex, symbols,type):
	global timer
	birza = getattr(ccxt, ex)()
	while True:
		if time.time() - timer > testtime:
			break
		# await  asyncio.sleep(0.001)
		try:
			rezdict[type][ex]['startzapros']=time.time()
			orderbook = await asyncio.wait_for(birza.watch_order_book_for_symbols(symbols,getdepth(ex)), 50)
			rezdict[type][ex]['zadzapros'].append(time.time() - rezdict[type][ex]['startzapros'] )
			# rezdict[type][ex]['laststakan'] = orderbook
			if len(orderbook['asks'])>0:
				rezdict[type][ex]['working'] =True

			if orderbook['timestamp']!=None:
				rezdict[type][ex]['zadtmstmp'].append(time.time()-orderbook['timestamp']/1000)


		except Exception:
			# traceback.print_exc()
			await birza.close()
			rezdict[type][ex]['misakes']+=1
			if rezdict[type][ex]['misakes']>5:
				print(' отвалилась биржа ',ex)
				# rezdict[type][ex]['misakes']='break'
				traceback.print_exc()
				await birza.close()
				break


async def main():
	global timer
	timer = time.time()
	for type in testdict:
		for ex in testdict[type]:
			# if ex =='binance':
			for buf in testdict[type][ex]:
				print(ex,type, buf)
				asyncio.create_task(example(ex, buf,type))

	print('stop 0')
	await  asyncio.sleep(testtime)
	print('stop 1')
	print(time.time()-timer)
	myput('watchOrderBookForSymbols',rezdict)


	for type in rezdict:
		# mediana =None
		# sredn=None

		for ex in rezdict[type]:
			# print(type, ex, a[type][ex]['zadtmstmp'][:50])
			ln = len(rezdict[type][ex]['zadtmstmp'])
			if ln > 3:
				mediana=sorted(rezdict[type][ex]['zadtmstmp'])[int(ln / 2)]
				sredn=sum(rezdict[type][ex]['zadtmstmp']) / ln
				# print(type, ex, ln, mediana, '  ',sredn )
				print(f'{type, ex}  zadmedianatmstmp {mediana}    zadsredntmstmp {sredn} ')

			ln = len(rezdict[type][ex]['zadzapros'])
			if ln > 3:
				mediana=sorted(rezdict[type][ex]['zadzapros'])[int(ln / 2)]
				sredn=sum(rezdict[type][ex]['zadzapros']) / ln
				print(f'{type, ex}  zadmedianazapros {mediana}    zadsrednzapros {sredn} ')




asyncio.run(main())

#
for type in  rezdict:
	for ex in rezdict[type]:
		print(type,ex,rezdict[type][ex]['working'],len(a['watchOrderBookForSymbols'][ex][type]),a['watchOrderBookForSymbols'][ex][type])
		# if rezdict[type][ex]['working']==False:
		# 	del(a['watchOrderBookForSymbols'][ex][type])
		# 	print('delete ',type,ex)




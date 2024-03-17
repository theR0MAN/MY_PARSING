from  my_filter_instrs import  *
import time
import ccxt.pro as ccxt
import traceback
import asyncio
from multiprocessing import Process



# quit()
def mymachine1(a,exchanges):
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

	def getcor(type,ex):
		if ex in corutins[type]:
			cor = corutins[type][ex]
		else:
			cor = 'other'
		return cor




	# разделение на корутины по к-ву элтов     # bitmex    bybit     ['swap']
	corutins = {}
	corutins['swap'] = {}
	corutins['spot'] = {}

	corutins['swap']['bitmex'] = 10
	corutins['spot']['bybit'] = 10
	# corutins['swap']['kucoin'] = 10


	# -------------------------------------------
	# -------------------------------------------

	testdict=dict()
	testdict['spot']=dict()
	testdict['swap']=dict()

	for ex in a['watchOrderBookForSymbols']:
		if a['watchOrderBookForSymbols'][ex]['swap']!=[]:
			if ex in exchanges:
				print(ex,'swap',len(a['watchOrderBookForSymbols'][ex]['swap']),a['watchOrderBookForSymbols'][ex]['swap'])
				testdict['swap'][ex]=[]
				kvo= getcor('swap',ex)
				if kvo=='other':
					kvo = max(int(len(a['watchOrderBookForSymbols'][ex]['swap']) / 2) + 1, 10)

				buf=[]
				count=0
				for sym in a['watchOrderBookForSymbols'][ex]['swap']:
					buf.append(sym )
					count+=1
					if count>=kvo:
						testdict['swap'][ex].append(buf)
						buf = []
						count = 0
				if count>0:
					testdict['swap'][ex].append(buf)

		if a['watchOrderBookForSymbols'][ex]['spot']!=[]:
			if ex in exchanges:
				print(ex, 'spot', len(a['watchOrderBookForSymbols'][ex]['spot']), a['watchOrderBookForSymbols'][ex]['spot'])
				testdict['spot'][ex]=[]
				kvo= getcor('spot',ex)
				if kvo == 'other':
					kvo = max(int(len(a['watchOrderBookForSymbols'][ex]['spot']) / 2) + 1, 10)
				buf=[]
				count=0
				for sym in a['watchOrderBookForSymbols'][ex]['spot']:
					buf.append(sym )
					count+=1
					if count>=kvo:
						testdict['spot'][ex].append(buf)
						buf = []
						count = 0
				if count>0:
					testdict['spot'][ex].append(buf)


	# for ex in testdict['swap']:
	# 	print(ex,'swap',len(testdict['swap'][ex]),testdict['swap'][ex])
	# for ex in testdict['spot']:
	# 	print(ex,'spot',len(testdict['spot'][ex]),testdict['spot'][ex])


	# quit()
	rezdict=dict()
	rezdict['spot']=dict()
	rezdict['swap']=dict()


	for type in testdict:
		for ex in testdict[type]:
			rezdict[type][ex]=dict()
			rezdict[type][ex]['misakes']= 0


	async def example(ex, symbols,type):
		# global timer
		depth=getdepth(ex)
		birza = getattr(ccxt, ex)()
		while True:
			# await  asyncio.sleep(0.001)
			try:

				rezdict[type][ex]['startzapros']=time.time()
				stk = await asyncio.wait_for(birza.watch_order_book_for_symbols(symbols,depth), 60)
				tme=time.time()
				symb=stk['symbol']
				dc = dict()
				if len(stk['asks']) > 0 and len(stk['bids']) > 0:
					try:
						Ask = stk['asks'][0][0]
						Bid = stk['bids'][0][0]
						if Ask > 0 and Bid > 0 and Ask > Bid:
							dc['asks'] = stk['asks']
							dc['bids'] = stk['bids']
							dc['mytime'] = time.time()
							dc['all'] = True
							dc['zad'] = tme- rezdict[type][ex]['startzapros']
							if stk['timestamp'] != None:
								dc['timestamp'] = stk['timestamp'] / 1000
								if tme - stk['timestamp'] / 1000 > 0:
									print(tme- stk['timestamp'] / 1000, dc['zad'], symb + '*' + ex)
							else:
								dc['timestamp'] = None
							# myredput(symb + '*' + ex, dc)
					except Exception:
						print(ex, " какая то херь в криптомашине1 с", symb)
						traceback.print_exc()



			except Exception:
				await birza.close()
				rezdict[type][ex]['misakes']+=1
				if rezdict[type][ex]['misakes']>5:
					print(' отвалилась биржа ',ex,type)
					traceback.print_exc()
					await birza.close()
					break


	async def main():
		# global timer
		# timer = time.time()
		for type in testdict:
			for ex in testdict[type]:
				for buf in testdict[type][ex]:
					asyncio.create_task(example(ex, buf,type))
					print(' пуск корутины',ex, buf,type)
		await  asyncio.sleep(600)
		print('stop 1')
	# **********************************
	asyncio.run(main())
	print('end')


# mymachine1(a,['binance','bybit','binanceusdm'])

if __name__ == "__main__":
	flaghard = False
	topsyms = 50 # ВЫБИРАЕМ первые  topsyms из списка самых популярных (по количеству баз  вкл спот и своп) символах на всех биржах
	mininstr = int(topsyms / 2)  # минимальное количество инструментов из topsyms на бирже, если меньше - биржа не включается в список на тест
	if not os.path.exists('a'):
		print('получаем а')
		a = takefiltrinstrs(flaghard, topsyms, mininstr)
		myput('a',a)
	else:
		print('загружаем а')
		a=myload('a')
	# , ['kucoin'], ['bitget'], ['okx']
	# ['binance', 'bybit']     ['bitmex','binanceusdm']   ['bitget']    ['okx']   ['kucoin']
	# cores = [['cryptocom', 'bitmex', 'bitget' ], ['okx', 'kucoin', 'kucoinfutures'], ['binance', 'bybit', 'binanceusdm']]
	# cores = [['cryptocom', 'binanceusdm'] , [ 'binance'] , ['bitget']  , ['okx'] , ['kucoin', 'bitmex'] ,['bybit']]
	# cores = [['binance'],['bitmex','cryptocom'], ['bybit']]
	# cores = [['bitget']]

	cores = [['bybit']]
	# ['cryptocom', 'binanceusdm',  'bitmex'], ['binance', 'bybit'], ['kucoinfutures'], ['okx'], ['kucoin']

	dat = datetime.datetime.utcfromtimestamp(time.time())
	day00 = dat.day
	name= 'worker'
	for core in cores:
		for ex in core:
			name=name+'-'+ex
		print(name)
		Process(name=name, target=mymachine1, args=(a,core,)).start()
	print('ZAEBUBA')


	# while True:
	# 	time.sleep(10)
	# 	dat = datetime.datetime.utcfromtimestamp(time.time())
	# 	day = dat.day
	# 	mnt = dat.minute
	# 	if day00 != day:  # and mnt>1
	# 		day00 = day
	# 		rez_dict(20, 50, all, onlyfut, True)
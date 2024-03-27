from  my_filter_instrs import  *
import time
import ccxt.pro as ccxt
import traceback
import asyncio
from multiprocessing import Process
from my_kriptofun import *



# quit()
def mymachine1(core):

	async def poll(exch,type, symb):
		exname = '*' + exch + '&' + type
		depth = getdepth(exch)
		global count
		exchange = getattr(ccxt, exch)()
		tm0 = time.time()
		# await asyncio.sleep(1)#stsl
		# print("START ",exch,symb)
		while True:
			await asyncio.sleep(0.01)
			tm = time.time()
			if tm0 + 0 <= tm:
				tm0 = tm
				try:
					# timer = time.time()
					stk=await asyncio.wait_for(exchange.watch_order_book(symb, depth),1200)
					tme = time.time()
					dc=dict()
					if len(stk['asks']) >0 and len(stk['bids']) >0 :
						try:
							Ask = stk['asks'][0][0]
							Bid = stk['bids'][0][0]
							if Ask > 0 and Bid > 0 and Ask >Bid:
								# print(exch, symb, stk['timestamp'])
								dc['asks']=stk['asks'][0]
								dc['bids'] = stk['bids'][0]
								# dc['mytime'] = round(tme,3)
								if stk['timestamp'] != None:
									dc['timestamp'] = stk['timestamp'] / 1000
									if tme - stk['timestamp'] / 1000 > 7:
										print(tme - stk['timestamp'] / 1000, symb + exname)
								else:
									dc['timestamp'] = None
								myredput(symb+exname,dc)
						except Exception:
							print(exch," какая то херь в криптомашине с",symb )
							traceback.print_exc()


				except Exception:
					await  exchange.close()
					await asyncio.sleep(1)


	async def example(ex,type, symbols):
		exname='*' + ex+'&'+type
		depth=getdepth(ex)
		birza = getattr(ccxt, ex)()
		while True:
			# await  asyncio.sleep(0.003)
			try:
				# rezdict[type][ex]['startzapros']=time.time()
				stk = await asyncio.wait_for(birza.watch_order_book_for_symbols(symbols,depth), 60)
				tme=time.time()
				symb=stk['symbol']
				dc = dict()
				if len(stk['asks']) > 0 and len(stk['bids']) > 0:
					try:
						Ask = stk['asks'][0][0]
						Bid = stk['bids'][0][0]
						if Ask > 0 and Bid > 0 and Ask > Bid:
							dc['asks'] = stk['asks'][0]
							dc['bids'] = stk['bids'][0]
							# dc['mytime'] = round(tme,3)
							# dc['zad'] = tme- rezdict[type][ex]['startzapros']
							if stk['timestamp'] != None:
								dc['timestamp'] = stk['timestamp'] / 1000
								if tme - stk['timestamp'] / 1000 > 7:
									dat = datetime.datetime.utcfromtimestamp(time.time())
									day = dat.day
									hour = dat.hour
									mnt = dat.minute
									print(f" day {day} hour{hour}  mnt {mnt} задержка по таймстампу {tme - stk['timestamp'] / 1000, symb + exname}  ")
							else:
								dc['timestamp'] = None
							# print(symb + '*' + ex,dc)
							myredput(symb + exname, dc)
					except Exception:
						print(ex, " какая то херь в криптомашине1 с", symb)
						traceback.print_exc()



			except Exception:
				await birza.close()
				# rezdict[type][ex]['misakes']+=1
				# if rezdict[type][ex]['misakes']>5:
				# 	print(' отвалилась биржа ',ex,type)
				# 	traceback.print_exc()
				# 	await birza.close()
				# 	break


	async def main():

		#  запуск корутин
		for corutine in core:
			if corutine['metod']=='watchOrderBookForSymbols':
				print(corutine['exchange'],corutine['type'],corutine['metod'],corutine['symbols'])
				asyncio.create_task(example(corutine['exchange'], corutine['type'], corutine['symbols']))
				print(' пуск корутины',corutine['exchange'], corutine['symbols'],corutine['type'])

			elif corutine['metod']=='watchOrderBook':
				for sym in corutine['symbols']:
					asyncio.create_task(poll(corutine['exchange'], corutine['type'], sym))

		await  asyncio.sleep(31100000) # а пока подождем с годик

		# # может вкрутим обновления корутин, пока не пуду пускать гэзэ
		# dat = datetime.datetime.utcfromtimestamp(time.time())
		# day00 = dat.day
		# while True:
		# 	await  asyncio.sleep(10)
		# 	dat = datetime.datetime.utcfromtimestamp(time.time())
		# 	day = dat.day
		# 	# mnt = dat.minute
		# 	if day00 != day:  # and mnt>1
		# 		day00 = day
		# 		print(' новый день скоро встретит ночь за окном')
		# # print('stop 1')
	# **********************************
	asyncio.run(main())
	print('end')




# quit()
if __name__ == "__main__":
	kyader = 6
	kcorut = 12
	minsyms = 50
	obrezsyms = 200
	flaghard = False
	# myexchanges = ['binance', 'bybit', 'bitget', 'okx', 'kucoin', 'bitmex', 'cryptocom', 'binanceusdm', 'huobi']  #'kucoinfutures'
	# myexchanges = ['binance','bybit', 'bitget', 'bitmex', 'cryptocom','binanceusdm',  'okx', 'huobi'  ]
	# myexchanges = ['binance', 'bybit', 'bitget',  'okx', 'huobi']
	# myexchanges = ['bybit',]
	# myexchanges = ['binance&swap', 'bitget&swap', 'bybit&swap', 'huobi&swap', 'okx&swap',]
	myexchanges = ['binance&swap']
	# myexchanges = ['huobi']


	mycores =getcorutine(kyader,kcorut,minsyms,obrezsyms,myexchanges,flaghard)
	# mycores = myload('corutines')
	# quit()
	dat = datetime.datetime.utcfromtimestamp(time.time())
	day00 = dat.day

	# quit()
	for core in mycores:
		print(' process',core )
		Process(target=mymachine1, args=(mycores[core],)).start()
	print('ZAEBUBA')

	#
	# while True:
	# 	time.sleep(10)
	# 	dat = datetime.datetime.utcfromtimestamp(time.time())
	# 	day = dat.day
	# 	# mnt = dat.minute
	# 	if day00 != day:  # and mnt>1
	# 		day00 = day
	# 		print(' новый день скоро встретит ночь за окном')



from  my_filter_instrs import  *
import time
import ccxt.pro as ccxt
import traceback
import asyncio
from multiprocessing import Process
from my_kriptofun import *



# quit()
def mymachine1(core):

	async def poll(exch, symb):
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
								dc['mytime'] = tme
								dc['watchall'] = False
								if stk['timestamp'] != None:
									dc['timestamp'] = stk['timestamp'] / 1000
									if tme - stk['timestamp'] / 1000 > 5:
										print(tme - stk['timestamp'] / 1000, symb + '*' + exch)
								else:
									dc['timestamp'] = None
								myredput(symb+'*'+exch,dc)
						except Exception:
							print(exch," какая то херь в криптомашине с",symb )
							traceback.print_exc()


				except Exception:
					await  exchange.close()
					await asyncio.sleep(1)


	async def example(ex, symbols):
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

							dc['mytime'] = time.time()
							dc['watchall'] = True
							# dc['zad'] = tme- rezdict[type][ex]['startzapros']
							if stk['timestamp'] != None:
								dc['timestamp'] = stk['timestamp'] / 1000
								if tme - stk['timestamp'] / 1000 > 5:
									print(tme- stk['timestamp'] / 1000,  symb + '*' + ex)
							else:
								dc['timestamp'] = None
							# print(symb + '*' + ex,dc)
							myredput(symb + '*' + ex, dc)
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
		for corutine in core:
			if corutine['metod']=='watchOrderBookForSymbols':
				print(corutine['exchange'],corutine['type'],corutine['metod'],corutine['symbols'])
				asyncio.create_task(example(corutine['exchange'], corutine['symbols']))
				print(' пуск корутины',corutine['exchange'], corutine['symbols'],corutine['type'])
			elif corutine['metod']=='watchOrderBook':
				if corutine['type']=='swap':
					for sym in corutine['symbols']:
						asyncio.create_task(poll(corutine['exchange'], sym))

		await  asyncio.sleep(600)
		print('stop 1')
	# **********************************
	asyncio.run(main())
	print('end')



# kyader = 1
# kcorut = 5
# minsyms = 50
# obrezsyms=50
# # myexchanges = ['binance', 'bybit', 'bitget', 'okx', 'kucoin', 'bitmex', 'cryptocom', 'binanceusdm', 'huobi']  #'kucoinfutures', 'huobi'
# myexchanges = [ 'bybit']
# flaghard = False
#
# # mycores =getcorutine(kyader,kcorut,minsyms,obrezsyms,myexchanges,flaghard)
# mycores = myload('corutines')
# for core in mycores:
# 	mymachine1(core)
# 	print(core, len(mycores[core]), mycores[core])
# 	# for corutine in mycores[core]:
# 	# 	print(corutine['exchange'],corutine['type'],corutine['symbols'])

# quit()
if __name__ == "__main__":
	kyader = 6
	kcorut = 4
	minsyms = 50
	obrezsyms = 30
	flaghard = False
	# myexchanges = ['binance', 'bybit', 'bitget', 'okx', 'kucoin', 'bitmex', 'cryptocom', 'binanceusdm', 'huobi']  #'kucoinfutures'
	myexchanges = ['binance','bybit', 'bitget', 'bitmex', 'cryptocom','binanceusdm',  'okx', 'huobi'  ]
	# myexchanges = ['bybit']
	# myexchanges = ['huobi']


	mycores =getcorutine(kyader,kcorut,minsyms,obrezsyms,myexchanges,flaghard)
	# mycores = myload('corutines')
#

	dat = datetime.datetime.utcfromtimestamp(time.time())
	day00 = dat.day
	name= 'worker'
	for core in mycores:
		# print(' process')
		Process(target=mymachine1, args=(mycores[core],)).start()
	print('ZAEBUBA')


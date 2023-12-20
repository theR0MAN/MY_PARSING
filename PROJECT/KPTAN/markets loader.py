import ccxt.pro as ccxt
from PROJECT.my_lib import *
import time
import datetime
import asyncio
import traceback

ask0 = {}
bid0 = {}
count = 0

data=myload('Frez')


async def loader(birza,ex):
	try:
		await asyncio.wait_for(birza.load_markets(),300)
		print('load market ', birza,'   ',ex)
	except Exception:
		print('ERROR load market ', birza,'   ',ex)
		traceback.print_exc()



async def main():
	countex=0
	countsyms=0
	tasksload = []
	tasks = []
	birzas=dict()
	for ex in data:
		if ex in ['bybit'] :  #ex in ['binance','bybit','gate','kraken']
			birzas[ex] = getattr(ccxt, ex)()
			tasksload.append(loader(birzas[ex],ex))

	# markets = await self.fetch_markets(params)
	print('start load tasks')
	await asyncio.gather(*tasksload)
	print('STOP load tasks')
	print('start MAIN tasks')
	await asyncio.gather(*tasks)
	print('STOP MAIN tasks')



asyncio.run(main())

import  asyncio
import ccxt.pro as ccxt
import traceback
from PROJECT.my_lib import *
errors=[]
myexs=dict()

def markload():
	async def lm(ex):
		birza = getattr(ccxt, ex)()
		try:
			markets = await birza.load_markets()
			myexs[ex]=markets
			print(ex)
			await birza.close()
		except Exception:
			await birza.close()
			errors.append(ex)
			print('ERROR load market ', birza,'   ',ex)
			# traceback.print_exc()


	async def main():
		tasks=[]
		exch = ccxt.exchanges
		for ex in exch:
			tasks.append(lm(ex))
		await  asyncio.gather(*tasks)

		tasks=[]
		print(errors)
		for ex in errors:
			tasks.append(lm(ex))
		errors.append('NEXT')
		await  asyncio.gather(*tasks)

	asyncio.run(main())
	myput('Kriptoinf.roman',myexs)
	print(errors)
	print('finish')

markload()
# ['bitpanda', 'alpaca', 'bittrex', 'coinbase', 'binanceus', 'phemex']

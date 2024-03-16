import  asyncio
import time
import os
import datetime
import ccxt.pro as ccxt
from PROJECT.SBOR.my_lib import *
import traceback

import asyncio

rezdictspot=dict()
rezdictswap=dict()
# 'timestamp': None, 'datetime': None,
# 'timestamp': 1709925130014, 'datetime': '2024-03-08T19:12:10.014Z', 'nonce': 44073107468, 'symbol': 'BTC/USDT'
async def example(exch,symbols):
    global timer
    birza =  getattr(ccxt, exch)()
    while True:
        await  asyncio.sleep(0.001)
        try:
            orderbook = await asyncio.wait_for(birza.watch_order_book_for_symbols(symbols),50)
            print(exch,orderbook['symbol'], orderbook)


            # break
            if time.time() - timer>20:
                break
        except Exception:
            print('mistake')
            traceback.print_exc()
            await birza.close()
 


async def main():

    global timer
    timer=time.time()

    asyncio.create_task(example('bybit',['BTC/USDT']))
    asyncio.create_task(example('binance',['BTC/USDT']))
    print('stop 0')
    await  asyncio.sleep(20)
    print('stop 1')



asyncio.run(main())



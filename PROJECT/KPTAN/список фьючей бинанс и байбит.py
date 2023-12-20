
from PROJECT.my_lib import *


data= myload('Kriptoinf.roman')

symset1=set()
symset2=set()
symset=set()

# for ex in data:
# 	print(ex)
# quit()

for sym in data['bybit']:
	if '/USDT:USDT' in sym and '-C'not in sym and '-P'not in sym and data['bybit'][sym]['active']==True:
		symset1.add(sym.partition('/')[0])
for sym in data['binance']:
	if '/USDT:USDT' in sym and '-C'not in sym and '-P'not in sym and data['binance'][sym]['active']==True:
		symset2.add(sym.partition('/')[0])
# print(len(symset1), symset1)
# print(len(symset2), symset2)#,syyms
symset= symset1&symset2
print(len(symset), symset)
# quit()
rezdat=dict()
for ex in data:
	rezdat[ex]={}
	rezdat[ex]['futures']=[]
	rezdat[ex]['spot'] = []
	for sym in data[ex]:
		if '/USDT' in sym and '-C'not in sym and '-P'not in sym and data[ex][sym]['active']==True:
			a=sym.partition('/')[0]
			if a in symset:
				if ":USDT" in sym:
					rezdat[ex]['futures'].append(sym)
				else:
					rezdat[ex]['spot'].append(sym)

	if len(rezdat[ex]['futures'])+len(rezdat[ex]['spot'])<10:
		print( ' DEL  ',ex)
		del rezdat[ex]

for ex in rezdat:
	print( ex,'   ',len(rezdat[ex]['spot']),'   ',len(rezdat[ex]['futures']),'   ',len(data[ex]) )

myput('Frez',rezdat)
#
# bequant     58     21     233
# bitget     201     191     913
# bitcoincom     207     26     1585
# bitopro     12     0     38
# bitmex     9     47     189
# bitfinex2     63     43     455
# bitmart     179     138     1369
# ascendex     104     54     896
# blockchaincom     18     0     162
# coinbaseprime     36     0     608
# cryptocom     133     0     652
# coinbasepro     36     0     608
# coinex     0     120     1195
# hitbtc     207     26     1585
# bitfinex     63     0     454
# poloniex     137     0     703
# hollaex     31     0     35
# upbit     12     0     302
# okx     146     150     1950
# wazirx     175     0     696
# probit     99     0     900
# kucoinfutures     0     212     253
# poloniexfutures     0     12     13
# binance     218     236     2751
# whitebit     142     34     379
# bingx     219     191     839
# bybit     130     232     1791
# kraken     21     0     671
# binanceusdm     0     236     293
# mexc     70     222     2453
# phemex     155     210     808
# bitrue     206     0     1602
# htx     179     103     1750
# kucoin     195     0     1243
# huobi     179     103     1750
# gate     223     233     4505
# gateio     223     233     4505
#
# Process finished with exit code 0


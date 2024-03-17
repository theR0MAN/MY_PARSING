# from  my_filter_instrs import  *
from my_kriptofun import *

kyader=1
kcorut=5
minsyms=50
obrezsyms=30
myexchanges=['binance','bybit','bitget','okx','kucoin','bitmex','cryptocom', 'binanceusdm', 'huobi']
# myexchanges=['bybit']
flaghard=False

mycores =getcorutine(kyader,kcorut,minsyms,obrezsyms,myexchanges,flaghard)
# mycores=myload('corutines')

# for core in mycores:
# 	for corutin in mycores [core]:
# 		if corutin ['exchange'] =='binance':
# 			print(corutin)


for core in mycores:
	print(core,mycores[core])



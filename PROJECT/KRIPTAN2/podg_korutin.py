# подготовка корутин и распределения по ядрам
from  my_info_exch import  *
from  my_filter0 import  *



def getcorutine(kyader,kcorut,minsyms,myexchanges,flaghard):
	print(' старт функции getcorutine')
	c = myfiltr(myexchanges,minsyms,flaghard)


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
			kvo =int(ln/kcorut)+1 #+1 чтобы хвост убрать лишний -единичную корутину
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

	# for type in c:
	# 	for ex in c[type]:
	# 		print(ex,type,c[type][ex])
	# for type in c2:
	# 	for ex in c2[type]:
	# 		print(ex,type,c2[type][ex])

	#
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






kyader=5
kcorut=5
minsyms=50
myexchanges=['binance','bybit','bitget','okx','kucoin','bitmex','cryptocom', 'binanceusdm', 'huobi']
flaghard=False

mycores =getcorutine(kyader,kcorut,minsyms,myexchanges,flaghard)

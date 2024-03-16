from  my_load_markets  import  *

# minsyms - удаляем рынок (спот или своп) при количестве инструментов меньше этого параметра
def myfiltr(myexchanges,minsyms,flaghard=False):
	print(f' старт функции myfiltr  minsyms = {minsyms} flaghard= {flaghard}  myexchanges={myexchanges}')

	a = markload(flaghard)
	rezset = set()
	b=dict()
	b['spot']=dict()
	b['swap']=dict()
	myhas = dict()
	myhas['spot']=dict()
	myhas['swap']=dict()
	#  оставим только мои биржи и фильтруем по базе USDT
	for exch in myexchanges:
		b['spot'] [exch]= []
		b['swap'] [exch]= []
		myhas['spot'][exch] = set()
		myhas['swap'][exch] = set()
		for sym in a[exch]:
			if a[exch][sym]['active'] == True:
				if a[exch][sym]['type'] == 'spot'and a[exch][sym]['quote'] == 'USDT':
					b['spot'][exch].append(sym)
					base = sym.partition('/')[0]
					myhas['spot'][exch].add(base )
					rezset.add(base)
				elif a[exch][sym]['type'] == 'swap'and a[exch][sym]['quote'] == 'USDT' and a[exch][sym]['settle'] == 'USDT':
					b['swap'][exch].append(sym)
					base=sym.partition('/')[0]
					myhas['swap'][exch].add(base)
					rezset.add(base)

	print(' удаление маркетов с к-вом символов меньше ',minsyms)
	for type in b:
		for ex in b[type]:
			if len(b[type][ex]) < minsyms:
				del myhas[type][ex]
				print('myhas del',type,ex, len(b[type][ex]))


	# работа с множествами  myhas
	print('было инструментов до пересечения множеств ',len(rezset))
	for type in myhas:
		for ex in myhas[type]:
			rezset=rezset&myhas[type][ex]
	print('осталось инструментов после пересечения множеств ',len(rezset),rezset)

	print(' получение итогового словоря словаря инструментов по рынкам по множеству')
	c=dict ()
	c['spot']=dict()
	c['swap']=dict()
	for type in b:
		for ex in b[type]:
			if ex in myhas[type]:
				c[type][ex]=[]
				for sym in b[type][ex]:
					base = sym.partition('/')[0]
					if base in rezset:
						c[type][ex].append(sym)
	for type in c:
		for ex in c[type] :
			print(ex,type,len(c[type][ex]),c[type][ex])




	# for ex in b:
	# 	if len (b[ex]['spot'])< minsyms:
	# 		del myhas[ex]['spot']
	# 		print(' del spot', ex,len (b[ex]['spot']))
	# 	if len (b[ex]['swap'])< minsyms:
	# 		del myhas[ex]['swap']
	# 		print(' del swap', ex,len (b[ex]['swap']))



	quit()

	for exch in a:
		print(exch,len(a[exch]))

	myhas=dict()
	for exch in a:
		myhas[exch]=dict()
		myhas[exch]['spot']=set()
		myhas[exch]['swap'] =set()

		for sym in a[exch]:
			if a[exch][sym]['active'] == True:
				if a[exch][sym]['type'] == 'spot'and a[exch][sym]['quote'] == 'USDT':
					myhas[exch]['spot'].add(sym.partition('/')[0])
				elif a[exch][sym]['type'] == 'swap'and a[exch][sym]['quote'] == 'USDT' and a[exch][sym]['settle'] == 'USDT':
					myhas[exch]['swap'].add(sym.partition('/')[0])

	# for base in myhas:



	baseset = set()
	filtr1 = dict()
	for exch in a:
		myhas[exch]=dict()
		filtr1[exch] = []
		for sym in a[exch]:
			if a[exch][sym]['active'] == True:
				if a[exch][sym]['type'] == 'spot' and a[exch][sym]['quote'] == 'USDT':
					baseset.add(a[exch][sym]['base'])
					filtr1[exch].append(sym)
				if a[exch][sym]['type'] == 'swap' and a[exch][sym]['quote'] == 'USDT' and a[exch][sym]['settle'] == 'USDT':
					baseset.add(a[exch][sym]['base'])
					filtr1[exch].append(sym)

	# рейтинг баз символов
	rsyms = dict()
	for sym in baseset:
		rsyms[sym] = dict()
		rsyms[sym] = 0

	for exch in filtr1:
		for sym in filtr1[exch]:
			base = sym.partition('/')[0]
			rsyms[base] += 1

	rsyms = mysortdict(rsyms)
	print(" рейтинг символов  c  базой USDT по всем рынкам",rsyms)


	print(' завершение работы myfiltr')
# [['cryptocom', 'binanceusdm'] , [ 'binance'] , ['bitget']  , ['okx'] , ['kucoin', 'bitmex'] ,['bybit']]        'bingx'
myexchanges=['binance','bybit','bitget','okx','kucoin','bitmex','cryptocom', 'binanceusdm', 'huobi']
myfiltr(myexchanges,50,flaghard=False)
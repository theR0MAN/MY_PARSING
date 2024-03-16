from  my_load_markets  import  *

def takefiltrinstrs(flaghard,topsyms,mininstr):
	print(' старт функции takefiltrinstrs с параметром flaghard=', flaghard,' topsyms=', topsyms, ' mininstr=', mininstr)


	a = markload(flaghard)
	baseset = set()
	filtr1 = dict()
	for exch in a:
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
	print(" рейтинг символов ",rsyms)


	ct = 0
	bazalist = []
	for base in rsyms:
		bazalist.append(base)
		ct += 1
		if ct >= topsyms:
			break

	filtr2 = dict()
	for exch in filtr1:
		filtr2[exch] = []

	for baza in bazalist:
		for exch in filtr1:
			for sym in filtr1[exch]:
				base = sym.partition('/')[0]
				if baza == base:
					filtr2[exch].append(sym)

	# удалим  биржи c к-вом инстр меньше mininstr
	todel = []
	for exch in filtr2:
		if len(filtr2[exch]) < mininstr:
			todel.append(exch)
	for dl in todel:
		del filtr2[dl]


	# поделим на своп и спот
	filtr3 = dict()
	filtr3['watchOrderBookForSymbols']=dict()
	filtr3['watchOrderBook']=dict()
	for exch in filtr2:
		exchange = getattr(ccxt, exch)()
		if exchange.has['watchOrderBookForSymbols']:
			filtr3['watchOrderBookForSymbols'][exch] = dict()
			filtr3['watchOrderBookForSymbols'][exch]['spot'] = []
			filtr3['watchOrderBookForSymbols'][exch]['swap'] = []
			for sym in filtr2[exch]:
				if ':' in sym:
					filtr3['watchOrderBookForSymbols'][exch]['swap'].append(sym)
				else:
					filtr3['watchOrderBookForSymbols'][exch]['spot'].append(sym)
		else:
			filtr3['watchOrderBook'][exch] = dict()
			filtr3['watchOrderBook'][exch]['spot'] = []
			filtr3['watchOrderBook'][exch]['swap'] = []
			for sym in filtr2[exch]:
				if ':' in sym:
					filtr3['watchOrderBook'][exch]['swap'].append(sym)
				else:
					filtr3['watchOrderBook'][exch]['spot'].append(sym)

	# for watch in filtr3:
	# 	print(watch, len(filtr3[watch]))
	# 	for ex in filtr3[watch]:
	# 		print((f"{watch}  {ex}  spot { len(filtr3[watch][ex]['spot'])}  swap { len(filtr3[watch][ex]['swap'])} "))
	print(' завершение работы takefiltrinstrs')
	return filtr3


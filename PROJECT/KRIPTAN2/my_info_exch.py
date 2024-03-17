from  my_load_markets  import  *

# allbases  False - только по базам USDT
def myinfo(flaghard=False,allbases=True):
	''' возвращает список баз символов с убыванием популярности '''
	print(' старт функции myinfo flaghard=', flaghard," allbases=",allbases)


	a = markload(flaghard)
	myhas=dict()
	for exch in a:
		myhas[exch]=dict()
		myhas[exch]['spot']=0
		myhas[exch]['swap'] = 0
		myhas[exch]['future'] = 0
		myhas[exch]['option'] = 0
		exchange = getattr(ccxt, exch)()
		if exchange.has['watchOrderBookForSymbols']:
			myhas[exch]['watchOrderBookForSymbols']=True
		else:
			myhas[exch]['watchOrderBookForSymbols'] = False

		for sym in a[exch]:
			if a[exch][sym]['active'] == True:
				if a[exch][sym]['type'] == 'spot':
					myhas[exch]['spot']+=1
				elif a[exch][sym]['type'] == 'swap':
					myhas[exch]['swap']+=1
				elif a[exch][sym]['type'] == 'future':
					myhas[exch]['future']+=1
				elif a[exch][sym]['type'] == 'option':
					myhas[exch]['option']+=1

	# print(' подробно по маркетам :')
	# for exch in myhas:
	# 	print(exch,myhas[exch])

	print(' биржи с watchOrderBookForSymbols:')
	for exch in myhas:
		if myhas[exch]['watchOrderBookForSymbols']==True:
			print(exch,myhas[exch])
	print(' биржи с option:')
	for exch in myhas:
		if myhas[exch]['option']>0:
			print(exch,myhas[exch])
	print(' биржи с future:')
	for exch in myhas:
		if myhas[exch]['future']>0:
			print(exch,myhas[exch])
	print(' биржи с swap:')
	for exch in myhas:
		if myhas[exch]['swap']>0:
			print(exch,myhas[exch])
	print(' биржи с spot:')
	for exch in myhas:
		if myhas[exch]['spot']>0:
			print(exch,myhas[exch])


	baseset = set()
	filtr1 = dict()
	for exch in a:
		myhas[exch]=dict()
		filtr1[exch] = []
		for sym in a[exch]:
			if a[exch][sym]['active'] == True:
				if a[exch][sym]['type'] == 'spot' and (a[exch][sym]['quote'] == 'USDT'or allbases):
					baseset.add(a[exch][sym]['base'])
					filtr1[exch].append(sym)
				if a[exch][sym]['type'] == 'swap' and (a[exch][sym]['quote'] == 'USDT' and a[exch][sym]['settle'] == 'USDT' or allbases):
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
	print(" рейтинг символов   по всем рынкам", rsyms)

	rz=[]
	for key in rsyms:
		if rsyms[key]>10:
			rz.append(key)
	print(len(rz),rz)



	print(' завершение работы myinfo')
	return a,rz


# myinfo()


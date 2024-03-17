from  my_load_markets  import  *
from  my_info_exch import  *
# minsyms - удаляем рынок (спот или своп) при количестве инструментов меньше этого параметра
def myfiltr(myexchanges,minsyms,flaghard=False):
	print(f' старт функции myfiltr  minsyms = {minsyms} flaghard= {flaghard}  myexchanges={myexchanges}')
	a,raiting=myinfo()

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
	print( ' рейтинг бирж исходя из количества пересечений с общим множеством символов')
	for type in myhas:
		for ex in myhas[type]:
			print(type,ex,len(rezset&myhas[type][ex]))

	print('было инструментов до пересечения множеств ',len(rezset))
	for type in myhas:
		for ex in myhas[type]:
			rezset=rezset&myhas[type][ex]
	print('осталось инструментов после пересечения множеств ',len(rezset),rezset)
	rz=[]
	for bz in raiting:
		if bz in rezset:
			rz.append(bz)
	print('сортировка множества согласно рейтингу',len(rz),rz)

	def myfars(a):
		b = []
		ln = len(a)
		if int(ln / 2) == ln / 2:
			tp = 1
		else:
			tp = 2

		for i in range(int(ln / 2)):
			b.append(a[i])
			b.append(a[ln - 1 - i])
		if tp == 2:
			b.append(a[int(ln / 2)])
		return b

	rz=myfars(rz)
	# это нужно для кайфа по распределению нагрузки по ядрам
	print(' спайка -первое+последнее к центру,',rz)

	print(' получение итогового словоря словаря инструментов по рынкам по множеству')
	c=dict ()
	c['spot']=dict()
	c['swap']=dict()

	for type in b:
		for ex in b[type]:
			if ex in myhas[type]:
				c[type][ex]=[]
				for baza in rz:
					for sym in b[type][ex]:
						base = sym.partition('/')[0]
						if base ==baza:
							c[type][ex].append(sym)
							break
	for type in c:
		for ex in c[type] :
			print(ex,type,len(c[type][ex]),c[type][ex])

	print(' завершение работы myfiltr')
	return c

	# quit()

# [['cryptocom', 'binanceusdm'] , [ 'binance'] , ['bitget']  , ['okx'] , ['kucoin', 'bitmex'] ,['bybit']]        'bingx'
myexchanges=['binance','bybit','bitget','okx','kucoin','bitmex','cryptocom', 'binanceusdm', 'huobi']
myfiltr(myexchanges,50,flaghard=False)
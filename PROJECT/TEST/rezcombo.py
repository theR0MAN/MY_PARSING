# избавимся от buyvih sellvih
import copy

from PROJECT.SBOR.my_lib import *
import plotly.express as px
from PROJECT.VIZUAL.Viz_lib import get_color
import time

# структура time отписывается каждый час для вывода эквити

# ['data']['500@2@1@1']

# [time] ['asks'] [symbol] =double
# 	   ['bids'] [symbol] =double
# 	   ['data']  [progon] [symbol] list( list (Ask,Bid,Askf,bidf, dict('buy': [list(symbols)] ,'buyvih':[...],'sell':[...],'sellvih': [...])) )
zaderzka = True
showequity = True
showfixprofit = False
comis = 0
timer = time.time()
bigstruct = myload('SPbigstruct')


eqprofrezixes=list(range(1, len(bigstruct)+1))
print('unpack time ', time.time() - timer)

eqprofrez = dict()
fixprof = dict()
nakprofrez= dict()
nakprofrezf = dict()
ksdelok=dict()
prosadka=dict()


if not showequity and not showfixprofit:
	print(' ERROR!  not showequity and  not showfixprofit  ')
	quit()
# print(c)
# quit()
timer = time.time()
firstkey = next(iter(bigstruct))
symbols=[]

for sym1 in bigstruct[firstkey]['asks']:
	symbols.append(sym1)
for id in bigstruct[firstkey]['data']:
	nakprofrez[id] = dict()
	prosadka[id]  = dict()
	nakprofrezf[id] = dict()
	ksdelok[id] =dict()
	eqprofrez[id] = dict()
	fixprof[id] = dict()
	for sym1 in symbols:
		nakprofrez[id][sym1] = dict()
		nakprofrezf[id][sym1] = dict()
		prosadka[id][sym1] = dict()
		ksdelok[id][sym1] = dict()
		eqprofrez[id][sym1] = dict()
		fixprof[id][sym1] = dict()
		
		for sym2 in symbols:
			if sym1 != sym2:
				# print(sym1, sym2)
				maxpros=0
				maxeq=0
				prosadka[id][sym1][sym2] = 0
				nakprofrez[id][sym1] [sym2] = 0
				nakprofrezf[id][sym1] [sym2] = 0
				ksdelok[id][sym1] [sym2] = 0
				eqprofrez[id][sym1][sym2] = []
				fixprof[id][sym1][sym2] = []

				flagsell = True
				flagbuy = True
				flagsellvih = False
				flagbuyvih = False

				# a=bigstruct[stime]['data']['500@2@1@1'][sym1]
				for stime in bigstruct:
					a = bigstruct[stime]['data'][id][sym1]
					dAsk = bigstruct[stime]['asks'][sym1]
					dBid = bigstruct[stime]['bids'][sym1]

					for sigmas in a:

						# покупка
						if 'buy' in sigmas[4] and  sym2 in sigmas[4]['buy'] and flagbuy:
							Ask = sigmas[0]
							Askf = sigmas[2]
							flagbuy = False
							flagsell = True
							flagbuyvih=True
							buyopenprice = Ask
							buyopenpricef = Askf

							if flagsellvih:
								nakprofrez[id][sym1][sym2] += 100 * (sellopenprice - Ask) / sellopenprice - comis
								nakprofrezf[id][sym1][sym2] += 100 * (sellopenpricef - Askf) / sellopenpricef - comis
								ksdelok[id][sym1][sym2] += 1

						# продажа
						if 'sell' in sigmas[4] and  sym2 in sigmas[4]['sell']  and flagsell:
							Bid = sigmas[1]
							Bidf = sigmas[3]
							flagsell = False
							flagbuy = True
							flagsellvih=True
							sellopenprice = Bid
							sellopenpricef = Bidf

							if flagbuyvih:
								nakprofrez[id][sym1][sym2] += 100 * (Bid - buyopenprice) / buyopenprice - comis
								nakprofrezf[id][sym1][sym2] += 100 * (Bidf - buyopenpricef) / buyopenpricef - comis
								ksdelok[id][sym1][sym2] += 1



					if zaderzka:
						if flagsell and flagbuyvih:  # pos == 'buy'
							Reqprofrez = (nakprofrezf[id][sym1][sym2] + 100 * (dBid - buyopenpricef) / buyopenpricef)
						elif flagbuy and flagsellvih:  # pos == 'sell'
							Reqprofrez = (nakprofrezf[id][sym1][sym2] + 100 * (sellopenpricef - dAsk) / sellopenpricef - comis)
						else:
							Reqprofrez = (nakprofrezf[id][sym1][sym2])
					else:
						if flagsell and flagbuyvih:  # pos == 'buy'
							Reqprofrez = (nakprofrez[id][sym1][sym2] + 100 * (dBid - buyopenprice) / buyopenprice - comis)
						elif flagbuy and flagsellvih:  # pos == 'sell'
							Reqprofrez = (nakprofrez[id][sym1][sym2] + 100 * (sellopenprice - dAsk) / sellopenprice - comis)
						else:
							Reqprofrez = (nakprofrez[id][sym1][sym2])


					#  добавим
					eqprofrez[id][sym1][sym2].append(Reqprofrez)
					fixprof[id][sym1][sym2].append(nakprofrezf[id][sym1][sym2]) if zaderzka else fixprof[id][sym1][sym2].append(nakprofrez[id][sym1][sym2])
					maxeq= max (Reqprofrez,maxeq)
					maxpros = max (maxpros,maxeq-Reqprofrez)
				prosadka[id][sym1][sym2]=maxpros




print('count time ', time.time() - timer)
All= True
minsdelok=2
minpofitfactor=0
minprofit=-110
itog=dict()
for sym1 in symbols:
	for id in bigstruct[firstkey]['data']:
		color = get_color()
		fig = px.line(title=f"  {id} {sym1}")
		massym=[]
		for sym2 in symbols:
			sh = False
			if sym1 != sym2:
				ksd=ksdelok[id][sym1][sym2]
				eq=eqprofrez[id][sym1][sym2][-1]
				pros=prosadka[id][sym1][sym2]
				pf = eq /pros if pros>0 else 0

				if  ksd>minsdelok and minpofitfactor> pf and   eq>minprofit:
					sh=True
					if id not in itog:
						itog [id]=dict()
					if sym1 not in itog [id]:
						itog[id][sym1]=[]
					itog[id][sym1].append(sym2)


					massym.append(sym2)
					if showequity:
						clr = color()
						fig.add_scatter(x=eqprofrezixes, y=eqprofrez[id][sym1][sym2], line_color=clr, name=sym2 + f'eq  sd={ksd}  prof={eq} pros {pros}')
					if showfixprofit:
						clr = color()
						fig.add_scatter(x=eqprofrezixes, y=fixprof[id][sym1][sym2], line_color=clr, name=sym2 + f'prof sd={ksd}  prof={eq} pros {pros}')
		if sh and len (massym)>1:
			fig.show()
			# pass
		else:
			print(f' non data {id} {sym1} ')

itog2=copy.deepcopy(itog)
for id in itog:
	for sym in itog[id]:
		if len (itog[id][sym])<2:
			del(itog2[id][sym])
			pass
		else:
			print (id,sym,itog[id][sym] )
print(itog2)
myput('itog2',itog2)
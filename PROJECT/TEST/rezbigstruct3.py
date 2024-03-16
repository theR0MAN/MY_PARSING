# избавимся от buyvih sellvih
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
showequity = False
showfixprofit = True
comis = 0.03
timer = time.time()
bigstruct = myload('bigstruct3')
print('unpack time ', time.time() - timer)

eqprofrez = dict()
eqprofrezixes = dict()
fixprof = dict()

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
	for sym1 in symbols:
		for sym2 in symbols:
			if sym1 != sym2:
				print(sym1, sym2)

				nakprofrez = 0
				nakprofrezf = 0
				ksdelok = 0
				eqprofrez[sym2] = []
				eqprofrezixes[sym2] = []
				eqcountprofrezixes = 0
				fixprof[sym2] = []
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
								nakprofrez += 100 * (sellopenprice - Ask) / sellopenprice - comis
								nakprofrezf += 100 * (sellopenpricef - Askf) / sellopenpricef - comis
								ksdelok += 1

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
								nakprofrez += 100 * (Bid - buyopenprice) / buyopenprice - comis
								nakprofrezf += 100 * (Bidf - buyopenpricef) / buyopenpricef - comis
								ksdelok += 1



					if zaderzka:
						if flagsell and flagbuyvih:  # pos == 'buy'
							Reqprofrez = (nakprofrezf + 100 * (dBid - buyopenpricef) / buyopenpricef)
						elif flagbuy and flagsellvih:  # pos == 'sell'
							Reqprofrez = (nakprofrezf + 100 * (sellopenpricef - dAsk) / sellopenpricef - comis)
						else:
							Reqprofrez = (nakprofrezf)
					else:
						if flagsell and flagbuyvih:  # pos == 'buy'
							Reqprofrez = (nakprofrez + 100 * (dBid - buyopenprice) / buyopenprice - comis)
						elif flagbuy and flagsellvih:  # pos == 'sell'
							Reqprofrez = (nakprofrez + 100 * (sellopenprice - dAsk) / sellopenprice - comis)
						else:
							Reqprofrez = (nakprofrez)


					#  добавим
					eqcountprofrezixes += 1
					eqprofrezixes[sym2].append(eqcountprofrezixes)
					eqprofrez[sym2].append(Reqprofrez)
					fixprof[sym2].append(nakprofrezf) if zaderzka else fixprof[sym2].append(nakprofrez)

# print('count time ', time.time() - timer)
		color = get_color()
		fig = px.line(title=f"  {id} {sym1}")
		for sym2 in symbols:
			if sym1 != sym2:
				if showequity:
					clr = color()
					fig.add_scatter(x=eqprofrezixes[sym2], y=eqprofrez[sym2], line_color=clr, name=sym2 + '   eqprofrez')
				if showfixprofit:
					clr = color()
					fig.add_scatter(x=eqprofrezixes[sym2], y=fixprof[sym2], line_color=clr, name=sym2 + ' fixprof')
		fig.show()

# проверить основной файл 2ММ1-1 сигнал - это новое сочетание символов - нужно сравнивать множества
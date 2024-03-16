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
comis = 0.03
timer = time.time()
bigstruct = myload('bigstruct')
print('unpack time ', time.time() - timer)


eqprofrez = dict()
eqprofrezixes= dict()
fixprof =dict()

if not showequity and not showfixprofit:
	print(' ERROR!  not showequity and  not showfixprofit  ')
	quit()
# print(c)
# quit()
timer = time.time()
firstkey = next(iter(bigstruct))
for sym1 in bigstruct[firstkey]['data']['500@2@1@1']:
	for sym2 in bigstruct[firstkey]['data']['500@2@1@1']:
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
			sigbuy = False
			sigsell = False
			sigbuyvih = False
			sigsellvih = False
			pos = None
			# a=bigstruct[stime]['data']['500@2@1@1'][sym1]
			for stime in bigstruct:
				a = bigstruct[stime]['data']['500@2@1@1'][sym1]
				dAsk = bigstruct[stime]['asks'][sym1]
				dBid = bigstruct[stime]['bids'][sym1]

				for sigmas in a:
					Ask = sigmas[0]
					Bid = sigmas[1]
					Askf = sigmas[2]
					Bidf = sigmas[3]

					if sym2 in sigmas[4]['buy']:
						sigbuy = True
					else:
						sigbuy = False
					if sym2 in sigmas[4]['buyvih']:
						sigbuyvih = True
					else:
						sigbuyvih = False
					if sym2 in sigmas[4]['sell']:
						sigsell = True
					else:
						sigsell = False
					if sym2 in sigmas[4]['sellvih']:
						sigsellvih = True
					else:
						sigsellvih = False

					# закрытие покупки продажей
					if sigbuyvih and flagbuyvih:  # Bidsp>SoAsk
						pos = None
						flagbuyvih = False
						flagbuy = True
						flagsell = True

						nakprofrez += 100 * (Bid - buyopenprice) / buyopenprice - comis
						nakprofrezf += 100 * (Bidf - buyopenpricef) / buyopenpricef - comis
						ksdelok += 1
					# закрытие продажи  покупкой
					if sigsellvih and flagsellvih:
						pos = None
						flagsellvih = False
						flagsell = True
						flagbuy = True

						nakprofrez += 100 * (sellopenprice - Ask) / sellopenprice - comis
						nakprofrezf += 100 * (sellopenpricef - Askf) / sellopenpricef - comis
						ksdelok += 1

					# покупка
					if sigbuy and flagbuy:
						pos = 'buy'
						flagbuy = False
						flagsell = False
						flagbuyvih = True
						buyopenprice = Ask
						buyopenpricef = Askf

					# продажа
					if sigsell and flagsell:
						pos = 'sell'
						flagsell = False
						flagbuy = False
						flagsellvih = True
						sellopenprice = Bid
						sellopenpricef = Bidf

				if pos == 'buy':
					if zaderzka:
						Reqprofrez = (nakprofrezf + 100 * (dBid - buyopenpricef) / buyopenpricef)
					else:
						Reqprofrez = (nakprofrez + 100 * (dBid - buyopenprice) / buyopenprice - comis)
				elif pos == 'sell':
					if zaderzka:
						Reqprofrez = (nakprofrezf + 100 * (sellopenpricef - dAsk) / sellopenpricef - comis)
					else:
						Reqprofrez = (nakprofrez + 100 * (sellopenprice - dAsk) / sellopenprice - comis)
				else:
					if zaderzka:
						Reqprofrez = (nakprofrezf)
					else:
						Reqprofrez = (nakprofrez)
	
				#  добавим
				eqcountprofrezixes += 1
				eqprofrezixes[sym2].append(eqcountprofrezixes)
				eqprofrez[sym2].append(Reqprofrez)
				fixprof[sym2].append(nakprofrez)
	print('unpack time ', time.time() - timer)
	color = get_color()
	fig = px.line(title=f" eq {sym1}")
	for sym2 in bigstruct[firstkey]['data']['500@2@1@1']:
		if sym1 != sym2:
			if showequity:
				clr = color()
				fig.add_scatter(x=eqprofrezixes[sym2], y=eqprofrez[sym2], line_color=clr, name=sym2 + '   eqprofrez')
			if showfixprofit:
				clr = color()
				fig.add_scatter(x=eqprofrezixes[sym2], y=fixprof[sym2], line_color=clr, name=sym2+' fixprof')
	fig.show()

# проверить основной файл 2ММ1-1 сигнал - это новое сочетание символов, а не сделка. - нужно сравнивать множества
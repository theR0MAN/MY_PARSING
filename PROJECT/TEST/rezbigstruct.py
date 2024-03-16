from PROJECT.SBOR.my_lib import *
import plotly.express as px
from PROJECT.VIZUAL.Viz_lib import get_color
import time
# структура time отписывается каждый час для вывода эквити

# ['data']['500@2@1@1']

# [time] ['asks'] [symbol] =double
# 	   ['bids'] [symbol] =double
# 	   ['data']  [progon] [symbol] list( list (Ask,Bid,Askf,bidf, dict('buy': [list(symbols)] ,'buyvih':[...],'sell':[...],'sellvih': [...])) )

comis=0.03

profrez = []
profrezf = []
profrezixes = []
profcomis = []
nakprofrez = 0
nakprofrezf = 0
ksdelok = 0
countprofrezixes = 0

eqprofrez = []
eqprofrezf = []
eqprofrezixes = []
eqprofcomis = []
eqcountprofrezixes = 0

fixprof = []

Ask = None
Bid = None
Askf = None
Bidf = None

flagsell = True
flagbuy = True
flagsellvih = False
flagbuyvih = False

sigbuy=False
sigsell=False
sigbuyvih=False
sigsellvih=False

pos = None
sym1='NGG4*FRTS2'
sym2='NGH4*FRTS2'

timer=time.time()
bigstruct= myload('bigstruct')
print('unpack time ',time.time()-timer)

timer=time.time()
for stime in bigstruct:
	# print(stime,bigstruct[stime]['data'])
	a=bigstruct[stime]['data']['500@2@1@1'][sym1]
	dAsk=bigstruct[stime]['asks'][sym1]
	dBid = bigstruct[stime]['bids'][sym1]
	for sigmas in a:
		Ask=sigmas[0]
		Bid= sigmas[1]
		Askf=sigmas[2]
		Bidf= sigmas[3]

		if sym2 in sigmas[4]['buy']:
			# print('buy')
			sigbuy=True
		else:
			sigbuy = False

		if sym2 in sigmas[4]['buyvih']:
			# print('buyvih')
			sigbuyvih=True
		else:
			sigbuyvih = False

		if sym2 in sigmas[4]['sell']:
			# print('sell')
			sigsell=True
		else:
			sigsell=False

		if sym2 in sigmas[4]['sellvih']:
			# print('sellvih')
			sigsellvih=True
		else:
			sigsellvih=False

		# закрытие покупки продажей
		if sigbuyvih  and flagbuyvih:  # Bidsp>SoAsk
			pos = None
			flagbuyvih = False
			flagbuy = True
			flagsell = True

			nakprofrez += 100 * (Bid - buyopenprice) / buyopenprice
			nakprofrezf += 100 * (Bidf - buyopenpricef) / buyopenpricef

			profrez.append(nakprofrez)
			profrezf.append(nakprofrezf)

			countprofrezixes += 1
			profrezixes.append(countprofrezixes)

			ksdelok += 1

			profcomis.append(ksdelok * comis)
		# print('ok')
		# закрытие продажи  покупкой
		if sigsellvih and flagsellvih:
			pos = None
			flagsellvih = False
			flagsell = True
			flagbuy = True

			nakprofrez += 100 * (sellopenprice - Ask) / sellopenprice
			nakprofrezf += 100 * (sellopenpricef - Askf) / sellopenpricef


			profrez.append(nakprofrez)
			profrezf.append(nakprofrezf)


			countprofrezixes += 1
			profrezixes.append(countprofrezixes)
			ksdelok += 1
			profcomis.append(ksdelok * comis)
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
		Reqprofrez = (nakprofrez + 100 * (dBid- buyopenprice) / buyopenprice)
		# Reqprofrezf = (nakprofrezf + 100 * (dBid - buyopenpricef) / buyopenpricef)
	elif pos == 'sell':
		Reqprofrez = (nakprofrez + 100 * (sellopenprice - dAsk) / sellopenprice)

	else:
		Reqprofrez = (nakprofrez)



	#  добавим
	eqcountprofrezixes += 1
	eqprofrezixes.append(eqcountprofrezixes)
	eqprofrez.append(Reqprofrez)
	eqprofcomis.append(ksdelok * comis)

	fixprof.append(nakprofrez)



print('count time ',time.time()-timer)


color = get_color()
fig = px.line(title=f" REZ ")
clr = color()
fig.add_scatter(x=profrezixes, y=profrez, line_color=clr, name=" - " + ' profrez')
clr = color()
fig.add_scatter(x=profrezixes, y=profrezf, line_color=clr, name=" - " + ' profrezf')
clr = color()
fig.add_scatter(x=profrezixes, y=profcomis, line_color=clr, name='comis')
fig.show()

color = get_color()
fig = px.line(title=f" eq ")

clr = color()
fig.add_scatter(x=eqprofrezixes, y=eqprofrez, line_color=clr, name=" - " + ' eqprofrezf')
clr = color()
fig.add_scatter(x=eqprofrezixes, y=fixprof, line_color=clr, name=' fixprof')
clr = color()
fig.add_scatter(x=eqprofrezixes, y=eqprofcomis, line_color=clr, name=' eqprofcomis')

fig.show()
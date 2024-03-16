
from PROJECT.SBOR.my_lib import *
import plotly.express as px
from PROJECT.VIZUAL.Viz_lib import get_color
import time

# itog2=myload('itog2')
#
# for id in itog2:
# 	for sym in itog2[id]:
# 		print (id,sym,itog2[id][sym] )

zaderzka = True
showequity = True
showfixprofit = False
comis = 0.0
timer = time.time()
bigstruct = myload('BRbigstruct')

eqprofrezixes = list(range(1, len(bigstruct) + 1))
print('unpack time ', time.time() - timer)

eqprofrez = dict()
fixprof = dict()
nakprofrez = dict()
nakprofrezf = dict()
ksdelok = dict()
prosadka = dict()

if not showequity and not showfixprofit:
	print(' ERROR!  not showequity and  not showfixprofit  ')
	quit()
# print(c)
# quit()
timer = time.time()
firstkey = next(iter(bigstruct))
symbols = []

# for sym1 in bigstruct[firstkey]['asks']:
# 	symbols.append(sym1)
id= '500@2@1.5'
nakprofrez[id] = dict()
prosadka[id] = dict()
nakprofrezf[id] = dict()
ksdelok[id] = dict()
eqprofrez[id] = dict()
fixprof[id] = dict()
sym1='BRH4*FRTS2'
nakprofrez[id][sym1] = dict()
nakprofrezf[id][sym1] = dict()
prosadka[id][sym1] = dict()
ksdelok[id][sym1] = dict()
eqprofrez[id][sym1] = dict()
fixprof[id][sym1] = dict()

sym2set={'Мазут*RAW', 'Бензин*RAW'} #,'Мазут*RAW'
sym2=str(sym2set)


# print(sym1, sym2)
maxpros = 0
maxeq = 0
prosadka[id][sym1][sym2] = 0
nakprofrez[id][sym1][sym2] = 0
nakprofrezf[id][sym1][sym2] = 0
ksdelok[id][sym1][sym2] = 0
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
		if 'buy' in sigmas[4] and sym2set.issubset(sigmas[4]['buy']) and flagbuy:
			print( sym2set, sigmas[4]['buy'])
			Ask = sigmas[0]
			Askf = sigmas[2]
			flagbuy = False
			flagsell = True
			flagbuyvih = True
			buyopenprice = Ask
			buyopenpricef = Askf

			if flagsellvih:
				nakprofrez[id][sym1][sym2] += 100 * (sellopenprice - Ask) / sellopenprice - comis
				nakprofrezf[id][sym1][sym2] += 100 * (sellopenpricef - Askf) / sellopenpricef - comis
				ksdelok[id][sym1][sym2] += 1

		# продажа
		if 'sell' in sigmas[4] and sym2set.issubset(sigmas[4]['sell']) and flagsell:
			print( sym2set,sigmas[4]['sell'])
			Bid = sigmas[1]
			Bidf = sigmas[3]
			flagsell = False
			flagbuy = True
			flagsellvih = True
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
	maxeq = max(Reqprofrez, maxeq)
	maxpros = max(maxpros, maxeq - Reqprofrez)
prosadka[id][sym1][sym2] = maxpros

print('count time ', time.time() - timer)
# All = True
# minsdelok = 3
# minpofitfactor = 1
# minprofit = 0
# itog = dict()

color = get_color()
fig = px.line(title=f"  {id} {sym1}  {sym2}")

if showequity:
	clr = color()
	fig.add_scatter(x=eqprofrezixes, y=eqprofrez[id][sym1][sym2], line_color=clr, name=sym2 + f'eq ')
if showfixprofit:
	clr = color()
	fig.add_scatter(x=eqprofrezixes, y=fixprof[id][sym1][sym2], line_color=clr, name=sym2 + f'prof ')

fig.show()

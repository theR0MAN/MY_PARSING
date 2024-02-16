from PROJECT.SBOR.my_lib import *
import plotly.express as px
from PROJECT.VIZUAL.Viz_lib import get_color
import time

profrez1 = []
profrez2 = []
profrezall = []
profrez1f = []
profrez2f = []
profrezallf = []
profrezixes = []
profcomis = []
nakprofrez1 = 0
nakprofrez2 = 0
nakprofrez1f = 0
nakprofrez2f = 0
ksdelok = 0
countprofrezixes = 0

eqprofrez1 = []
eqprofrez2 = []
eqprofrezall = []
eqprofrez1f = []
eqprofrez2f = []
eqprofrezallf = []
eqprofrezixes = []
eqcountprofrezixes = 0
eqprofcomis = []

comis = 0.03
Ask1 = None
Bid1 = None
Ask2 = None
Bid2 = None
Ask1f = None
Bid1f = None
Ask2f = None
Bid2f = None
flagsell = True
flagbuy = True
flagsellvih = False
flagbuyvih = False
pos= None


eAsk1 = None
eBid1 = None
eAsk2 = None
eBid2 = None
eAsk1f = None
eBid1f = None
eAsk2f = None
eBid2f = None
meAsk1 = []
meBid1 = []
meAsk2 = []
meBid2 = []
meAsk1f = []
meBid1f = []
meAsk2f = []
meBid2f = []


EQmas = myload('rez')

for eq in EQmas:
	print(eq)

# REZ.append(['buyvih', [Ask1, Bid1], [Ask2, Bid2], [Ask1f, Bid1f], [Ask2f, Bid2f]])
# # EQ.append([tme, [[Ask1, Bid1],   [Ask2, Bid2], [Ask1f, Bid1f], [Ask2f, Bid2f]],    ['buyvih', [Ask1, Bid1], [Ask2, Bid2], [Ask1f, Bid1f], [Ask2f, Bid2f]]])

# # REZ = []
#
timer = time.time()
for eq in EQmas:


	# meAsk1.append(eAsk1)
	# meBid1.append(eBid1)
	# meAsk2.append(eAsk2)
	# meBid2.append(eBid2)
	# meAsk1f.append(eAsk1f)
	# meBid1f.append(eBid1f)
	# meAsk2f.append(eAsk2f)
	# meBid2f.append(eBid2f)

	for rez in eq[2]:

		Ask1 = rez[1][0]
		Bid1 = rez[1][1]
		Ask2 = rez[2][0]
		Bid2 = rez[2][1]
		Ask1f = rez[3][0]
		Bid1f = rez[3][1]
		Ask2f = rez[4][0]
		Bid2f = rez[4][1]

		pos=rez[0]
	# закрытие покупки продажей
		if  rez[0]=='buyvih' and flagbuyvih :  # Bidsp>SoAsk
			flagbuyvih = False
			flagbuy = True
			flagsell = True

			nakprofrez1 += 100 * (Bid1- buyopenprice1)
			nakprofrez2 += 100 * (sellopenprice2 - Ask2)
			nakprofrez1f += 100 * ( Bid1f - buyopenprice1f)
			nakprofrez2f += 100 * (sellopenprice2f - Ask2f)

			profrez1.append(nakprofrez1)
			profrez2.append(nakprofrez2)
			profrez1f.append(nakprofrez1f)
			profrez2f.append(nakprofrez2f)
			profrezall.append(nakprofrez1 + nakprofrez2)
			profrezallf.append(nakprofrez1f + nakprofrez2f)

			countprofrezixes += 1
			profrezixes.append(countprofrezixes)

			ksdelok += 1
			# profrezixes.append(ksdelok)
			profcomis.append(ksdelok * comis)
			# print('ok')
		# закрытие продажи  покупкой
		if  rez[0]=='sellvih' and flagsellvih :
			flagsellvih = False
			flagsell = True
			flagbuy = True

			nakprofrez1 += 100 * (sellopenprice1 - Ask1)
			nakprofrez2 += 100 * (Bid2 - buyopenprice2)
			nakprofrez1f += 100 * (sellopenprice1f - Ask1f)
			nakprofrez2f += 100 * (Bid2f - buyopenprice2f)

			profrez1.append(nakprofrez1)
			profrez2.append(nakprofrez2)
			profrez1f.append(nakprofrez1f)
			profrez2f.append(nakprofrez2f)
			profrezall.append(nakprofrez1 + nakprofrez2)
			profrezallf.append(nakprofrez1f + nakprofrez2f)

			countprofrezixes += 1
			profrezixes.append(countprofrezixes)
			ksdelok += 1
			# profrezixes.append(ksdelok)
			profcomis.append(ksdelok*comis)
			# print('ok')
		# покупка
		if  rez[0]=='buy' and flagbuy:
			flagbuy = False
			flagsell = False
			flagbuyvih = True
			first=True
			buyopenprice1 = Ask1
			sellopenprice2 = Bid2
			buyopenprice1f = Ask1f
			sellopenprice2f = Bid2f
			# print('ok')
		# продажа
		if  rez[0]=='sell' and flagsell:
			flagsell = False
			flagbuy=False
			flagsellvih = True
			sellopenprice1 = Bid1
			buyopenprice2 = Ask2
			sellopenprice1f = Bid1f
			buyopenprice2f = Ask2f

	if pos != None:

		eAsk1 = eq[1][0][0]
		eBid1 = eq[1][0][1]
		eAsk2 = eq[1][1][0]
		eBid2 = eq[1][1][1]
		eAsk1f = eq[1][2][0]
		eBid1f = eq[1][2][1]
		eAsk2f = eq[1][3][0]
		eBid2f = eq[1][3][1]

		if pos == 'buy':
			Reqprofrez1 = (nakprofrez1 + 100 * (eBid1 - buyopenprice1))
			Reqprofrez2 = (nakprofrez2 + 100 * (sellopenprice2 - eAsk2))

			Reqprofrez1f = (nakprofrez1f + 100 * (eBid1f - buyopenprice1f))
			Reqprofrez2f = (nakprofrez2f + 100 * (sellopenprice2f - eAsk2f))



		elif pos == 'sell':
			Reqprofrez1 = (nakprofrez1 + 100 * (sellopenprice1 - eAsk1))
			Reqprofrez2 = (nakprofrez2 + 100 * (eBid2 - buyopenprice2))

			Reqprofrez1f = (nakprofrez1f + 100 * (sellopenprice1f - eAsk1f))
			Reqprofrez2f = (nakprofrez2f + 100 * (eBid2f - buyopenprice2f))




		else:
			Reqprofrez1 = (nakprofrez1)
			Reqprofrez2 = (nakprofrez2)
			Reqprofrez1f = (nakprofrez1f)
			Reqprofrez2f = (nakprofrez2f)
	else:
		Reqprofrez1 = (nakprofrez1)
		Reqprofrez2 = (nakprofrez2)
		Reqprofrez1f = (nakprofrez1f)
		Reqprofrez2f = (nakprofrez2f)

	#  добавим
	eqcountprofrezixes += 1
	eqprofrezixes.append(eqcountprofrezixes)

	eqprofrez1.append(Reqprofrez1)
	eqprofrez2.append(Reqprofrez2)

	eqprofrez1f.append(Reqprofrez1f)
	eqprofrez2f.append(Reqprofrez2f)

	eqprofrezall.append(Reqprofrez1 + Reqprofrez2)
	eqprofrezallf.append(Reqprofrez1f + Reqprofrez2f)

	eqprofcomis.append(ksdelok * comis)

print(' time= ', time.time() - timer)
color = get_color()
fig = px.line(title=f" REZ ")
clr = color()
fig.add_scatter(x=profrezixes, y=profrez1, line_color=clr, name=" - " + ' profrez1')
clr = color()
fig.add_scatter(x=profrezixes, y=profrez2, line_color=clr, name=" - " + ' profrez2')
clr = color()
fig.add_scatter(x=profrezixes, y=profrezall, line_color=clr, name=' profrezall')
clr = color()
fig.add_scatter(x=profrezixes, y=profrez1f, line_color=clr, name=" - " + ' profrez1f')
clr = color()
fig.add_scatter(x=profrezixes, y=profrez2f, line_color=clr, name=" - " + ' profrez2f')
clr = color()
fig.add_scatter(x=profrezixes, y=profrezallf, line_color=clr, name=' profrezallf')
clr = color()
fig.add_scatter(x=profrezixes, y=profcomis, line_color=clr, name='comis')
fig.show()

color = get_color()
fig = px.line( title=f" REZ eq ")
clr = color()
fig.add_scatter(x=eqprofrezixes, y=eqprofrez1, line_color=clr, name=" - " + ' eqprofrez1')
clr = color()
fig.add_scatter(x=eqprofrezixes, y=eqprofrez2, line_color=clr, name= " - " + ' eqprofrez2')
clr = color()
fig.add_scatter(x=eqprofrezixes, y=eqprofrez1f, line_color=clr, name= " - " + ' eqprofrez1f')
clr = color()
fig.add_scatter(x=eqprofrezixes, y=eqprofrez2f, line_color=clr, name= " - " + ' eqprofrez2f')
clr = color()
fig.add_scatter(x=eqprofrezixes, y=eqprofrezall, line_color=clr, name=' eqprofrezall')
clr = color()
fig.add_scatter(x=eqprofrezixes, y=eqprofrezallf, line_color=clr, name=' eqprofrezallf')

clr = color()
fig.add_scatter(x=eqprofrezixes, y=eqprofcomis, line_color=clr, name=' eqprofcomis')
fig.show()


# color = get_color()
# fig = px.line( title=f" ME")
# clr = color()
# fig.add_scatter(x=eqprofrezixes, y=meAsk1, line_color=clr, name=" - " + ' meAsk1')
# fig.add_scatter(x=eqprofrezixes, y=meBid1, line_color=clr, name= " - " + ' meBid1')
# clr = color()
# fig.add_scatter(x=eqprofrezixes, y=meAsk2, line_color=clr, name=" - " + ' meAsk2')
# fig.add_scatter(x=eqprofrezixes, y=meBid2, line_color=clr, name= " - " + ' meBid2')
#
# clr = color()
# fig.add_scatter(x=eqprofrezixes, y=meAsk1f, line_color=clr, name=" - " + ' meAsk1f')
# fig.add_scatter(x=eqprofrezixes, y=meBid1f, line_color=clr, name= " - " + ' meBid1f')
# clr = color()
# fig.add_scatter(x=eqprofrezixes, y=meAsk2f, line_color=clr, name=" - " + ' meAsk2f')
# fig.add_scatter(x=eqprofrezixes, y=meBid2f, line_color=clr, name= " - " + ' meBid2f')
# fig.show()

# meAsk1.append(eAsk1)
# meBid1.append(eBid1)
# meAsk2.append(eAsk2)
# meBid2.append(eBid2)
# meAsk1f.append(eAsk1f)
# meBid1f.append(eBid1f)
# meAsk2f.append(eAsk2f)
# meBid2f.append(eBid2f)
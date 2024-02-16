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

comis=0.03
Ask1 =None
Bid1 = None
Ask2 = None
Bid2 = None
Ask1f =None
Bid1f = None
Ask2f = None
Bid2f = None
flagsell = True
flagbuy = True
flagsellvih = False
flagbuyvih = False
last=None

EQmas=myload('rez')


for eq in EQmas:
	print(eq)
	
# REZ.append(['buyvih', [Ask1, Bid1], [Ask2, Bid2], [Ask1f, Bid1f], [Ask2f, Bid2f]])
# # EQ.append([tme, [[Ask1, Bid1],   [Ask2, Bid2], [Ask1f, Bid1f], [Ask2f, Bid2f]],    ['buyvih', [Ask1, Bid1], [Ask2, Bid2], [Ask1f, Bid1f], [Ask2f, Bid2f]]])

# # REZ = []
#
timer=time.time()
for eq in EQmas:


	for rez in eq[2]:

		Ask1 = rez[1][0]
		Bid1 = rez[1][1]
		Ask2 = rez[2][0]
		Bid2 = rez[2][1]
		Ask1f = rez[3][0]
		Bid1f = rez[3][1]
		Ask2f = rez[4][0]
		Bid2f = rez[4][1]

		if last != None:
			if rez[0] =='buyvih' and last[0] == 'buy':
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

				ksdelok += 1
				profrezixes.append(ksdelok)
				profcomis.append(ksdelok * comis)

			elif rez[0] == 'sellvih' and last[0] == 'sell':
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


				ksdelok += 1
				profrezixes.append(ksdelok)
				profcomis.append(ksdelok*comis)


		last= rez
		buyopenprice1 = rez[1][0]
		sellopenprice2 = rez[2][1]
		buyopenprice1f = rez[3][0]
		sellopenprice2f = rez[4][1]

		sellopenprice1 = rez[1][1]
		buyopenprice2 = rez[2][0]
		sellopenprice1f = rez[3][1]
		buyopenprice2f = rez[4][0]

	if last != None:

		eAsk1 = eq[1][0][0]
		eBid1 = eq[1][0][1]
		eAsk2 = eq[1][1][0]
		eBid2 = eq[1][1][1]
		eAsk1f = eq[1][2][0]
		eBid1f = eq[1][2][1]
		eAsk2f = eq[1][3][0]
		eBid2f = eq[1][3][1]

		if last[0] == 'buy':
			Reqprofrez1 = (nakprofrez1 + 100 * (eBid1 - buyopenprice1))
			Reqprofrez2 = (nakprofrez2 + 100 * (sellopenprice2 - eAsk2))

			Reqprofrez1f = (nakprofrez1f + 100 * (eBid1f - buyopenprice1f))
			Reqprofrez2f = (nakprofrez2f + 100 * (sellopenprice2f - eAsk2f))

		elif last[0] == 'sell':
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



print(' time= ',time.time()-timer)
color = get_color()
fig = px.line(	title=f" REZ ")
clr = color()
fig.add_scatter(x=profrezixes, y=profrez1, line_color=clr, name= " - " + ' profrez1')
clr = color()
fig.add_scatter(x=profrezixes, y=profrez2, line_color=clr, name=" - " + ' profrez2')
clr = color()
fig.add_scatter(x=profrezixes, y=profrezall, line_color=clr, name=' profrezall')
clr = color()
fig.add_scatter(x=profrezixes, y=profrez1f, line_color=clr, name= " - " + ' profrez1f')
clr = color()
fig.add_scatter(x=profrezixes, y=profrez2f, line_color=clr, name= " - " + ' profrez2f')
clr = color()
fig.add_scatter(x=profrezixes, y=profrezallf, line_color=clr, name=' profrezallf')
clr = color()
fig.add_scatter(x=profrezixes, y=profcomis, line_color=clr, name='comis')
fig.show()


color = get_color()
fig = px.line( 	title=f" REZ eq ")
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
fig.show()
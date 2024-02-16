from PROJECT.SBOR.my_lib import *
import plotly.express as px
from PROJECT.VIZUAL.Viz_lib import get_color
import time
comis = 0.03

profrez1 = dict()
profrez2 = dict()
profrezall = dict()
profrez1f = dict()
profrez2f = dict()
profrezallf = dict()
profrezixes = dict()
profcomis = dict()
nakprofrez1 = dict()
nakprofrez2 = dict()
nakprofrez1f = dict()
nakprofrez2f = dict()
ksdelok = dict()
countprofrezixes =dict()

eqprofrez1 = dict()
eqprofrez2 = dict()
eqprofrezall = dict()
eqprofrez1f = dict()
eqprofrez2f = dict()
eqprofrezallf = dict()
eqprofrezixes = dict()
eqcountprofrezixes = dict()
eqprofcomis = dict()

Ask1 = dict()
Bid1 = dict()
Ask2 = dict()
Bid2 = dict()
Ask1f = dict()
Bid1f = dict()
Ask2f = dict()
Bid2f = dict()
flagsell = dict()
flagbuy = dict()
flagsellvih = dict()
flagbuyvih = dict()
pos= dict()


eAsk1 = dict()
eBid1 = dict()
eAsk2 = dict()
eBid2 = dict()
eAsk1f = dict()
eBid1f = dict()
eAsk2f = dict()
eBid2f = dict()
fixprof1= dict()
fixprof2 =dict()


timer = time.time()
EQmas = myload('rez6')
print('UNPASC time= ', time.time() - timer)

for id in EQmas:
	fixprof1[id] = []
	fixprof2[id]  = []

	profrez1[id]  = []
	profrez2[id]  = []
	profrezall[id]  = []
	profrez1f[id]  = []
	profrez2f[id]  = []
	profrezallf[id]  = []
	profrezixes[id]  = []
	profcomis[id]  = []
	nakprofrez1[id]  = 0
	nakprofrez2[id]  = 0
	nakprofrez1f[id]  = 0
	nakprofrez2f[id]  = 0
	ksdelok[id]  = 0
	countprofrezixes[id]  = 0

	eqprofrez1[id]  = []
	eqprofrez2[id]  = []
	eqprofrezall[id]  = []
	eqprofrez1f[id]  = []
	eqprofrez2f[id]  = []
	eqprofrezallf[id]  = []
	eqprofrezixes[id]  = []
	eqcountprofrezixes[id]  = 0
	eqprofcomis[id]  = []

	Ask1[id]  = None
	Bid1[id]  = None
	Ask2[id]  = None
	Bid2[id]  = None
	Ask1f[id]  = None
	Bid1f[id]  = None
	Ask2f[id]  = None
	Bid2f[id]  = None
	flagsell[id]  = True
	flagbuy[id]  = True
	flagsellvih[id]  = False
	flagbuyvih[id]  = False
	pos[id]  = None

	eAsk1[id]  = None
	eBid1[id]  = None
	eAsk2[id]  = None
	eBid2[id]  = None
	eAsk1f[id]  = None
	eBid1f[id]  = None
	eAsk2f[id]  = None
	eBid2f[id]  = None
	print(id ,EQmas [id ] )
	


# REZ.append(['buyvih', [Ask1, Bid1], [Ask2, Bid2], [Ask1f, Bid1f], [Ask2f, Bid2f]])
# # EQ.append([tme, [[Ask1, Bid1],   [Ask2, Bid2], [Ask1f, Bid1f], [Ask2f, Bid2f]],    ['buyvih', [Ask1, Bid1], [Ask2, Bid2], [Ask1f, Bid1f], [Ask2f, Bid2f]]])


timer = time.time()
for id in EQmas:
	for eq in EQmas[id ][0:]:
		for rez in eq[2]:
			if rez[0]== 'buy' or rez[0]== 'sell':
				pos=rez[0]

			Ask1[id]  = rez[1][0]
			Bid1[id]  = rez[1][1]
			Ask2[id]  = rez[2][0]
			Bid2[id]  = rez[2][1]
			Ask1f[id]  = rez[3][0]
			Bid1f[id]  = rez[3][1]
			Ask2f[id]  = rez[4][0]
			Bid2f[id]  = rez[4][1]


		# закрытие покупки продажей
			if  rez[0]=='buyvih' and flagbuyvih[id]  :  # Bidsp>SoAsk
				flagbuyvih[id]  = False
				flagbuy[id]  = True
				flagsell[id]  = True

				nakprofrez1[id]  += 100 * (Bid1[id] - buyopenprice1[id] )/ buyopenprice1[id]
				nakprofrez2[id]  += 100 * (sellopenprice2[id]  - Ask2[id] )/sellopenprice2[id]
				nakprofrez1f[id]  += 100 * ( Bid1f[id]  - buyopenprice1f[id] ) / buyopenprice1f[id]
				nakprofrez2f[id]  += 100 * (sellopenprice2f[id]  - Ask2f[id] )/ sellopenprice2f[id]

				profrez1[id] .append(nakprofrez1[id] )
				profrez2[id] .append(nakprofrez2[id] )
				profrez1f[id] .append(nakprofrez1f[id] )
				profrez2f[id] .append(nakprofrez2f[id] )
				profrezall[id] .append(nakprofrez1[id]  + nakprofrez2[id] )
				profrezallf[id] .append(nakprofrez1f[id]  + nakprofrez2f[id] )

				countprofrezixes[id]  += 1
				profrezixes[id] .append(countprofrezixes[id] )

				ksdelok += 1
				# profrezixes.append(ksdelok)
				profcomis[id] .append(ksdelok[id]  * comis)
				# print('ok')
			# закрытие продажи  покупкой
			if  rez[0]=='sellvih' and flagsellvih[id]  :
				flagsellvih[id]  = False
				flagsell[id]  = True
				flagbuy[id]  = True

				nakprofrez1[id]  += 100 * (sellopenprice1[id]  - Ask1[id] ) / sellopenprice1[id]
				nakprofrez2[id]  += 100 * (Bid2[id]  - buyopenprice2[id] )/ buyopenprice2[id]
				nakprofrez1f[id]  += 100 * (sellopenprice1f[id]  - Ask1f[id] )/sellopenprice1f[id]
				nakprofrez2f[id]  += 100 * (Bid2f[id]  - buyopenprice2f[id] )/buyopenprice2f [id]

				profrez1[id] .append(nakprofrez1[id] )
				profrez2[id] .append(nakprofrez2[id] )
				profrez1f[id] .append(nakprofrez1f[id] )
				profrez2f[id] .append(nakprofrez2f[id] )
				profrezall[id] .append(nakprofrez1[id]  + nakprofrez2[id] )
				profrezallf[id] .append(nakprofrez1f[id]  + nakprofrez2f[id] )

				countprofrezixes += 1
				profrezixes[id] .append(countprofrezixes[id] )
				ksdelok += 1
				# profrezixes.append(ksdelok)
				profcomis[id] .append(ksdelok[id] *comis)
				# print('ok')
			# покупка
			if  rez[0]=='buy' and flagbuy[id] :
				flagbuy[id]  = False
				flagsell[id]  = False
				flagbuyvih[id]  = True
				buyopenprice1[id]  = Ask1 [id]
				sellopenprice2[id]  = Bid2[id]
				buyopenprice1f[id]  = Ask1f [id]
				sellopenprice2f[id]  = Bid2f [id]
				# print('ok')
			# продажа
			if  rez[0]=='sell' and flagsell[id] :
				flagsell[id]  = False
				flagbuy[id] =False
				flagsellvih[id]  = True
				sellopenprice1[id]  = Bid1[id]
				buyopenprice2[id]  = Ask2[id]
				sellopenprice1f[id]  = Bid1f [id]
				buyopenprice2f[id]  = Ask2f[id]

		if pos != None:

			eAsk1[id]  = eq[1][0][0]
			eBid1[id]  = eq[1][0][1]
			eAsk2[id]  = eq[1][1][0]
			eBid2[id]  = eq[1][1][1]
			eAsk1f[id]  = eq[1][2][0]
			eBid1f[id]  = eq[1][2][1]
			eAsk2f[id]  = eq[1][3][0]
			eBid2f[id]  = eq[1][3][1]

			if pos == 'buy':
				Reqprofrez1 = (nakprofrez1[id]  + 100 * (eBid1[id]  - buyopenprice1[id] )/buyopenprice1[id] )
				Reqprofrez2  = (nakprofrez2[id]  + 100 * (sellopenprice2[id]  - eAsk2[id] )/sellopenprice2[id] )

				Reqprofrez1f = (nakprofrez1f[id]  + 100 * (eBid1f[id]  - buyopenprice1f[id] )/buyopenprice1f[id] )
				Reqprofrez2f  = (nakprofrez2f[id]  + 100 * (sellopenprice2f[id]  - eAsk2f[id] )/sellopenprice2f[id] )



			elif pos == 'sell':
				Reqprofrez1 = (nakprofrez1[id]  + 100 * (sellopenprice1 - eAsk1)/sellopenprice1)
				Reqprofrez2 = (nakprofrez2[id]  + 100 * (eBid2 - buyopenprice2)/buyopenprice2)

				Reqprofrez1f = (nakprofrez1f[id]  + 100 * (sellopenprice1f - eAsk1f)/sellopenprice1f)
				Reqprofrez2f = (nakprofrez2f[id]  + 100 * (eBid2f - buyopenprice2f)/buyopenprice2f)


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

		fixprof1.append(nakprofrez1)
		fixprof2.append(nakprofrez2)

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
	fig.add_scatter(x=eqprofrezixes, y=fixprof1, line_color=clr, name=' fixprof1')
	clr = color()
	fig.add_scatter(x=eqprofrezixes, y=fixprof2, line_color=clr, name=' fixprof2')

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
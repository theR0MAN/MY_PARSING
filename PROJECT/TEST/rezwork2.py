import time

from PROJECT.SBOR.my_lib import *
import plotly.express as px
from PROJECT.VIZUAL.Viz_lib import get_color
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
rez=myload('rez')


for eq in rez:
	print(eq)
#
# # EQ.append([tme, [[Ask1, Bid1], [Ask2, Bid2], [Ask1f, Bid1f], [Ask2f, Bid2f]], REZ])
# # REZ = []
#
timer = time.time()
for eq in rez:
	for i in eq[2]:

		Ask1 = i[1][0]
		Bid1 = i[1][1]
		Ask2 = i[2][0]
		Bid2 = i[2][1]
		Ask1f = i[3][0]
		Bid1f = i[3][1]
		Ask2f = i[4][0]
		Bid2f = i[4][1]

		

		# REZ.append(['buyvih', [Ask1, Bid1], [Ask2, Bid2], [Ask1f, Bid1f], [Ask2f, Bid2f]])
		# закрытие покупки продажей
		if  i[0]=='buyvih' and flagbuyvih :  # Bidsp>SoAsk
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
		if  i[0]=='sellvih' and flagsellvih :
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
		if  i[0]=='buy' and flagbuy:
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
		if  i[0]=='sell' and flagsell:
			flagsell = False
			flagbuy=False
			flagsellvih = True
			sellopenprice1 = Bid1
			buyopenprice2 = Ask2
			sellopenprice1f = Bid1f
			buyopenprice2f = Ask2f


print(' time= ',time.time()-timer)
color = get_color()
fig = px.line(
	title=f" REZ ")
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
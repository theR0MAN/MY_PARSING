from PROJECT.TEST.Test_lib import *
from PROJECT.VIZUAL.Viz_lib import get_color
from PROJECT.SCIENTIC.sc_sredn_lib import *
from platform import system
import plotly.express as px
import datetime, time
import traceback

markets = ['FRTS']  # ,'MOEX'
minutki = 0
onlymerge = 0
instrument = 'Si-12.23*FRTS'

start_year, start_month, start_day, start_hour = 2023, 9, 20, 12
stop_year, stop_month, stop_day, stop_hour = 2023, 9, 20, 12

getpath = 'G:\\DATA_SBOR' if system() == 'Windows' else '/media/roman/J/DATA_SBOR'
content = getdata_merge(onlymerge, minutki, markets, getpath, start_year, start_month, start_day, start_hour, stop_year,
						stop_month, stop_day, stop_hour)
print(content)

askmas = []
bidmas = []
srexpmas = []
sreasymas = []
medmas = []
shlifmedmas = []
shlifmedmas2 = []
shlifmedmas20 = []
ixmas = []
tm = 0
# z = get_l2(content)

exem = Getl2(content)
scie = Mysredn()


z = exem.get_l2()  # получает словарь котиров

while True:
	try:
		a = next(z)

		# список инструментов раз в день
		# print(exem.output)
		# print(exem.ttime)
		# print(exem.day)

		if a[instrument]['asks'] != []:
			Ask = a[instrument]['asks'][0][0]
			Bid = a[instrument]['bids'][0][0]
			data = (Ask + Bid) / 2
			askmas.append(Ask)
			bidmas.append(Bid)
			srexpmas.append(scie.getsredn_exp(data,instrument,400))
			sreasymas.append(scie.getsredn_easy(data,instrument,400))
			mediana=scie.getmediana(data,instrument,200)
			medmas.append(mediana)
			shlifmedmas.append(scie.getsredn_easy(mediana,instrument+'shlif',200))
			shlifmedmas2.append(scie.getsredn_exp(mediana, instrument + 'shlif', 200))
			shlifmedmas20.append(scie.getshlifmed_exp(data, instrument, 200))
			ixmas.append(tm)
			tm += 1


	except RuntimeError:
		print("StopIteration error handled successfully")
		break
# except Exception:
# 	traceback.print_exc()
# 	print('stop')
# 	break
#


color = get_color()
clr = color()
fig = px.line()
fig.add_scatter(x=ixmas, y=askmas, line_color=clr, name=' ask')
fig.add_scatter(x=ixmas, y=bidmas, line_color=clr, name=' bid')
#
# clr = color()
# fig.add_scatter(x=ixmas, y=srexpmas, line_color=clr, name=' srednexp')
# clr = color()
# fig.add_scatter(x=ixmas, y=sreasymas, line_color=clr, name=' sredneasy')
# clr = color()
# fig.add_scatter(x=ixmas, y=medmas, line_color=clr, name=' mediana')
# clr = color()
# fig.add_scatter(x=ixmas, y=shlifmedmas, line_color=clr, name=' shlifmed')
clr = color()
fig.add_scatter(x=ixmas, y=shlifmedmas2, line_color=clr, name=' shlifmed2')
clr = color()
fig.add_scatter(x=ixmas, y=shlifmedmas20, line_color=clr, name=' shlifmed20')

bidmas2 = []
ixmas2 = []
for i in range(0, len(ixmas), 30):
	ixmas2.append(i)
	bidmas2.append(bidmas[i])
fig.add_scatter(x=ixmas2, y=bidmas2, line_color='red', mode='markers', name=' M')

fig.show()
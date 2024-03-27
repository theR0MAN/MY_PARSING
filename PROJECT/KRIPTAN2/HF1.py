from PROJECT.TEST.Test_lib import *
from PROJECT.VIZUAL.Viz_lib import get_color
from PROJECT.SCIENTIC.sc_sredn_lib import *
from platform import system
import plotly.express as px
from collections import deque
import datetime, time  # timer=time.time()
import traceback
import statistics
import pandas as pd
from PROJECT.SBOR.my_lib import *


zadpol=3
zadtmsmp=2

pth='G:\\NEWKRIPT'

markets = ['binance&swap', ]  #'poloniex',24 1  7-10
print(markets)

instdict = dict()

minutki = 123
onlymerge = 0

hardsync=False
# hardsync True - жесткая синхронизация, когда все инструменты одновременно вписываются в задержки
# hardsync False - просто когда присутствуют все инструменры
start_year, start_month, start_day, start_hour = 2024, 3, 24, 0
stop_year, stop_month, stop_day, stop_hour = 2024, 3, 25, 23

content = getdata_merge(onlymerge, minutki, markets, pth, start_year, start_month, start_day, start_hour, stop_year,
						stop_month, stop_day, stop_hour)
print(content)

if content==[]:
	print(' нет данных за этот период' )
	quit()

exem = Getl2(content, 200, 0.95, 10)
scie = Mysredndiskret(300)
z = exem.get_l2NEW()  # получает словарь котиров
# spisinst=['BTC/USDT:USDT*binance&swap', 'MINA/USDT:USDT*binance&swap', 'OMG/USDT:USDT*binance&swap', 'SNT/USDT:USDT*binance&swap', 'SPELL/USDT:USDT*binance&swap', 'BAT/USDT:USDT*binance&swap', 'ASTR/USDT:USDT*binance&swap', 'KNC/USDT:USDT*binance&swap', 'COTI/USDT:USDT*binance&swap', 'FLOW/USDT:USDT*binance&swap', 'SXP/USDT:USDT*binance&swap', 'IOST/USDT:USDT*binance&swap', 'KAVA/USDT:USDT*binance&swap', 'ZIL/USDT:USDT*binance&swap', 'GAS/USDT:USDT*binance&swap', 'ADA/USDT:USDT*binance&swap', 'SEI/USDT:USDT*binance&swap', 'LOOM/USDT:USDT*binance&swap', 'EGLD/USDT:USDT*binance&swap', 'TWT/USDT:USDT*binance&swap', '1INCH/USDT:USDT*binance&swap', 'KSM/USDT:USDT*binance&swap', 'VET/USDT:USDT*binance&swap', 'REN/USDT:USDT*binance&swap', 'BAND/USDT:USDT*binance&swap', 'ICX/USDT:USDT*binance&swap', 'DAR/USDT:USDT*binance&swap', 'CVX/USDT:USDT*binance&swap', 'FXS/USDT:USDT*binance&swap', 'ALICE/USDT:USDT*binance&swap', 'ILV/USDT:USDT*binance&swap', 'TLM/USDT:USDT*binance&swap', 'ENS/USDT:USDT*binance&swap', 'DASH/USDT:USDT*binance&swap', 'REEF/USDT:USDT*binance&swap', 'MANTA/USDT:USDT*binance&swap', 'GMX/USDT:USDT*binance&swap', 'AUDIO/USDT:USDT*binance&swap', 'ENJ/USDT:USDT*binance&swap', 'AXS/USDT:USDT*binance&swap', 'RUNE/USDT:USDT*binance&swap', 'JOE/USDT:USDT*binance&swap', 'RLC/USDT:USDT*binance&swap', 'HFT/USDT:USDT*binance&swap', 'POWR/USDT:USDT*binance&swap', 'OGN/USDT:USDT*binance&swap', 'KLAY/USDT:USDT*binance&swap', 'INJ/USDT:USDT*binance&swap', 'ACE/USDT:USDT*binance&swap', 'GLMR/USDT:USDT*binance&swap', 'SLP/USDT:USDT*binance&swap', 'LSK/USDT:USDT*binance&swap', 'MTL/USDT:USDT*binance&swap', 'RVN/USDT:USDT*binance&swap', 'ORBS/USDT:USDT*binance&swap', 'AGLD/USDT:USDT*binance&swap', 'APE/USDT:USDT*binance&swap', 'XRP/USDT:USDT*binance&swap', 'BIGTIME/USDT:USDT*binance&swap', 'LINA/USDT:USDT*binance&swap', 'ETH/USDT:USDT*binance&swap', 'XTZ/USDT:USDT*binance&swap', 'STORJ/USDT:USDT*binance&swap', 'LRC/USDT:USDT*binance&swap', 'ETC/USDT:USDT*binance&swap', 'XEM/USDT:USDT*binance&swap', 'DYDX/USDT:USDT*binance&swap', 'SAND/USDT:USDT*binance&swap', 'WAXP/USDT:USDT*binance&swap', 'MANA/USDT:USDT*binance&swap', 'YFI/USDT:USDT*binance&swap', 'WIF/USDT:USDT*binance&swap', 'BNT/USDT:USDT*binance&swap', 'BICO/USDT:USDT*binance&swap', 'PYTH/USDT:USDT*binance&swap', 'WOO/USDT:USDT*binance&swap', 'DGB/USDT:USDT*binance&swap', 'MAGIC/USDT:USDT*binance&swap', 'WAVES/USDT:USDT*binance&swap', 'ALGO/USDT:USDT*binance&swap', 'AEVO/USDT:USDT*binance&swap', 'ETHFI/USDT:USDT*binance&swap', 'NMR/USDT:USDT*binance&swap', 'BLZ/USDT:USDT*binance&swap', 'GMT/USDT:USDT*binance&swap', 'GALA/USDT:USDT*binance&swap', 'PIXEL/USDT:USDT*binance&swap', 'ZETA/USDT:USDT*binance&swap', 'DOT/USDT:USDT*binance&swap', 'ALPHA/USDT:USDT*binance&swap', 'RNDR/USDT:USDT*binance&swap', 'HBAR/USDT:USDT*binance&swap', 'HOT/USDT:USDT*binance&swap', 'ORDI/USDT:USDT*binance&swap', 'BLUR/USDT:USDT*binance&swap', 'NEO/USDT:USDT*binance&swap', 'CELO/USDT:USDT*binance&swap', 'XMR/USDT:USDT*binance&swap', 'UMA/USDT:USDT*binance&swap', 'PERP/USDT:USDT*binance&swap', 'AR/USDT:USDT*binance&swap', 'AAVE/USDT:USDT*binance&swap', 'EOS/USDT:USDT*binance&swap', 'PORTAL/USDT:USDT*binance&swap', 'FET/USDT:USDT*binance&swap', 'LPT/USDT:USDT*binance&swap', 'XLM/USDT:USDT*binance&swap', 'ONE/USDT:USDT*binance&swap', 'LINK/USDT:USDT*binance&swap', 'OXT/USDT:USDT*binance&swap', 'MEME/USDT:USDT*binance&swap', 'OCEAN/USDT:USDT*binance&swap', 'QTUM/USDT:USDT*binance&swap', 'DOGE/USDT:USDT*binance&swap', 'CKB/USDT:USDT*binance&swap', 'YGG/USDT:USDT*binance&swap', 'MATIC/USDT:USDT*binance&swap', 'SUPER/USDT:USDT*binance&swap', 'RAD/USDT:USDT*binance&swap', 'T/USDT:USDT*binance&swap', 'AVAX/USDT:USDT*binance&swap', 'ETHW/USDT:USDT*binance&swap', 'ID/USDT:USDT*binance&swap', 'ONT/USDT:USDT*binance&swap', 'API3/USDT:USDT*binance&swap', 'ATOM/USDT:USDT*binance&swap', 'ROSE/USDT:USDT*binance&swap', 'ANKR/USDT:USDT*binance&swap', 'CHZ/USDT:USDT*binance&swap', 'MDT/USDT:USDT*binance&swap', 'CHR/USDT:USDT*binance&swap', 'IOTA/USDT:USDT*binance&swap', 'BADGER/USDT:USDT*binance&swap', 'AUCTION/USDT:USDT*binance&swap', 'GRT/USDT:USDT*binance&swap', 'IMX/USDT:USDT*binance&swap', 'TON/USDT:USDT*binance&swap', 'ALT/USDT:USDT*binance&swap', 'CELR/USDT:USDT*binance&swap', 'QNT/USDT:USDT*binance&swap', 'METIS/USDT:USDT*binance&swap', 'ARPA/USDT:USDT*binance&swap', 'AGIX/USDT:USDT*binance&swap', 'GLM/USDT:USDT*binance&swap', 'C98/USDT:USDT*binance&swap']
spisinst=['BTC/USDT:USDT*binance&swap', 'MINA/USDT:USDT*binance&swap', 'OMG/USDT:USDT*binance&swap', 'SNT/USDT:USDT*binance&swap', 'SPELL/USDT:USDT*binance&swap', 'BAT/USDT:USDT*binance&swap', 'ASTR/USDT:USDT*binance&swap', 'KNC/USDT:USDT*binance&swap', 'COTI/USDT:USDT*binance&swap', 'FLOW/USDT:USDT*binance&swap', 'SXP/USDT:USDT*binance&swap', 'IOST/USDT:USDT*binance&swap', 'KAVA/USDT:USDT*binance&swap', 'ZIL/USDT:USDT*binance&swap', 'GAS/USDT:USDT*binance&swap', 'ADA/USDT:USDT*binance&swap', 'SEI/USDT:USDT*binance&swap', 'LOOM/USDT:USDT*binance&swap', 'EGLD/USDT:USDT*binance&swap', 'TWT/USDT:USDT*binance&swap', '1INCH/USDT:USDT*binance&swap', 'KSM/USDT:USDT*binance&swap', 'VET/USDT:USDT*binance&swap', 'REN/USDT:USDT*binance&swap', 'BAND/USDT:USDT*binance&swap', 'ICX/USDT:USDT*binance&swap', 'DAR/USDT:USDT*binance&swap', 'CVX/USDT:USDT*binance&swap', 'FXS/USDT:USDT*binance&swap', 'ALICE/USDT:USDT*binance&swap', 'ILV/USDT:USDT*binance&swap', 'TLM/USDT:USDT*binance&swap', 'ENS/USDT:USDT*binance&swap', 'DASH/USDT:USDT*binance&swap', 'REEF/USDT:USDT*binance&swap']
# spisinst=['BTC/USDT:USDT*binance&swap', 'MINA/USDT:USDT*binance&swap']    #, 'MINA/USDT:USDT*binance&swap'

obryv = dict()
paintdict = {}
# подготовка словаря отрисовки
data = next(z)
# готовим итоговый массив
rezdict = dict()
rezdictcorrect = dict()

for sym in spisinst:
	rezdict[sym] = dict()
	rezdict[sym]['asks'] = []
	rezdict[sym]['bids'] = []
	rezdictcorrect[sym] = dict()
	rezdictcorrect[sym]['asks'] = []
	rezdictcorrect[sym]['bids'] = []

	rezdict[sym]['askbuf'] = 0
	rezdict[sym]['bidbuf'] = 0

period=4000
rezka=60 #через какой период рисовать - для снижения нагрузки на браузер
ixes = []
maxmas=[]
minmas=[]
wrt = False
count=0
strt=False
while True:

	try:
		# timer=time.time()
		data = next(z)  # это якобы на серваке - к нему нужен доступ

		if not wrt:
			wrt = True
			for inst in spisinst:
				if data[inst]['dat'] == None:
					wrt = False

		else:
			sum=0
			counsum=0
			for sym in spisinst:
				Ask0=data[sym]['dat']['asks'][0]
				Bid0=data[sym]['dat']['bids'][0]
				Ask,Bid=scie.getnormalize_by_getshlifmed_easy(sym,Ask0,Bid0,period)
				if Ask!=None:
					strt=True
					sum+=(Ask+Bid) /2
					counsum+=1
					rezdict[sym]['askbuf']=Ask
					rezdict[sym]['bidbuf']=Bid

					rezdict[sym]['asks'].append(Ask)
					rezdict[sym]['bids'].append(Bid)


			if strt:
				sredn = sum / counsum
				mx = -1000000
				mn = 1000000
				for sym in spisinst:
					ask = rezdict[sym]['askbuf'] - sredn
					bid = rezdict[sym]['bidbuf'] - sredn
					mx = max(mx, bid)
					mn = min(mn, ask)
					rezdictcorrect[sym]['asks'].append(ask)
					rezdictcorrect[sym]['bids'].append(bid)
				count += 1
				ixes.append(count)
				mxm=scie.getsredn_exp(mx,'mxsko',period*2)
				mnm=scie.getsredn_exp(mn,'mnsko',period*2)
				# if mxm!=None:
				# 	mxm*=2
				# if mnm!=None:
				# 	mnm*=2
				maxmas.append(mxm)
				minmas.append(mnm)
				#
				# pmx=(abs(mn)+abs(mx))/2
				# pms=scie.getshlifmed_easy(pmx,'sko',period)
				# if pms !=None:
				# 	maxmas.append(pms)
				# 	minmas.append(-pms)
				# else:
				# 	maxmas.append(None)
				# 	minmas.append(None)

	except Exception:
		print(traceback.format_exc())
		print('error')
		# quit()
		break

#
# color = get_color()
# fig = px.line(title=' do')
# for  inst in rezdict:
# 	clr = color()
# 	fig.add_scatter(x=ixes, y=rezdict [inst]['asks'], line_color=clr, name= inst + ' ask')
# 	fig.add_scatter(x=ixes, y=rezdict[inst]['bids'], line_color=clr, name= inst+ ' bid')
# fig.show()

color = get_color()
fig = px.line(title=' getsredn_exp *2')
for  inst in rezdict:
	clr = color()
	fig.add_scatter(x=ixes, y=rezdictcorrect [inst]['asks'], line_color=clr, name= inst + ' ask')
	fig.add_scatter(x=ixes, y=rezdictcorrect[inst]['bids'], line_color=clr, name= inst+ ' bid')

color = get_color()
clr = color()
fig.add_scatter(x=ixes, y=maxmas, line_color=clr, name=  'max')
fig.add_scatter(x=ixes, y=minmas, line_color=clr, name=  'min')
fig.show()
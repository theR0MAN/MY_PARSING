import copy
import MetaTrader5 as mt5
import time
import datetime
from PROJECT.SBOR.my_lib import *
# mysortdict(dict)
tme=time.time()
kmonth=7
km=kmonth* 2592000
# def get_fut(tme):
dat = datetime.datetime.utcfromtimestamp(int(tme))
year = dat.year
month = dat.month
day = dat.day
fortssymset=set()
mysyms = {'GD', 'SV', 'BR', 'NG', 'W4', 'Eu', 'Si', 'MX', 'ED', 'SR', 'SP'}
rez = dict()
spinst = []

if not mt5.initialize("E:\\FinamMT5\\terminal64.exe", timeout=30):
	print("initialize() failed, FinamMT5 error code =", mt5.last_error(), "? once TRY again")
	time.sleep(40)
	if not mt5.initialize("E:\\FinamMT5\\terminal64.exe", timeout=30):
		print("QUIT!!!!!!!!!!!! FinamMT5 initialize() failed, error code =", mt5.last_error())
		quit()
	else:
		print('initialize2  FinamMT5 sucsess')
else:
	print('initialize1 FinamMT5 sucsess')

symbols = mt5.symbols_get()
allsym = {}
for i in symbols:
	sym = i._asdict()
	if sym['name'] in allsym:
		print("fuckingsheat", sym['name'])
	else:
		allsym[sym['name']] = sym
a = allsym
for key in a:
	if a[key]['exchange'] == 'ФОРТС' and a[key]['expiration_time'] > tme + 86400  and a[key]['expiration_time'] < tme + km:
		if key== "RRH4":
			print(a[key])
		spinst.append(key)
		bd=key[:-2]
		if len (bd)==2:
			fortssymset.add(key[:-2])
print(fortssymset)



for i in fortssymset:
	rez[i] =dict()
	rez[i]['FRTS2']=[]
	for inst in spinst:
		bodyit = inst[:-2]
		if i == bodyit and a[inst]['point'] !=0 and a[inst]['margin_initial'] !=0:
			rez[i]['FRTS2'].append([inst,a[inst]['expiration_time'],(a[inst]['last']*a[inst]['trade_tick_value']/a[inst]['point'])/a[inst]['margin_initial'],a[inst]['margin_initial']])


for i in rez:
	rez[i]['FRTS2'] =mysortspis(rez[i]['FRTS2'])
	print(i,rez[i])



#
# 	for i in mysyms:  # instset
# 		rez[i] = dict()
# 		rez[i]['MAIN'] = []
# 		rez[i]['NEAR'] = []
# 		rez[i]['FAR'] = []
# 		rez[i]['USAFUT'] = []
# 		for inst in spinst:
# 			bodyit = inst[:-2]
# 			if i == bodyit:
# 				rez[i]['MAIN'].append(inst + '*FRTS2')
#
# 	# # добавим вечные фьючи
# 	# # 'USDRUBF 'IMOEXF 'GLDRUBF    'EURRUBF  Si MX  GD   Eu
# 	rez['Si']['MAIN'].insert(0, 'USDRUBF*FRTS2')
# 	rez['MX']['MAIN'].insert(0, 'IMOEXF*FRTS2')
# 	rez['GD']['MAIN'].insert(0, 'GLDRUBF*FRTS2')
# 	rez['Eu']['MAIN'].insert(0, 'EURRUBF*FRTS2')
# 	# # добавим форекс
# 	rez['ED']['NEAR'].append('EURUSD*FxCUR')
# 	rez['GD']['NEAR'].append('XAUUSD*FxMETBR')
# 	rez['SV']['NEAR'].append('XAGUSD*FxMETBR')
# 	rez['BR']['NEAR'].append('Brent*FxMETBR')
# 	rez['BR']['FAR'].append('Crude*FxMETBR')
# 	rez['NG']['NEAR'].append('NatGas*FxMETBR')
# 	rez['Si']['FAR'].append('USDind*FxMETBR')
# 	# добавим валютку   CURcross
# 	# rez['Si']['NEAR'].append('USDRUB*CURcross')
# 	# rez['Si']['NEAR'].append('USDRUR*CURcross')
# 	# rez['Si']['NEAR'].append('USDRUB_TMS*CURcross')
# 	# rez['Eu']['NEAR'].append('EURRUB*CURcross')
# 	# rez['Eu']['NEAR'].append('EURRUR*CURcross')
# 	# rez['Eu']['NEAR'].append('EURRUB_TMS*CURcross')
#
# 	# добавим валютку   CUR
# 	rez['Si']['NEAR'].append('USD000UTSTOM*CUR')
# 	rez['Si']['NEAR'].append('USD000000TOD*CUR')
# 	# rez['Eu']['NEAR'].append('EURUSD000TOM*CUR')
# 	# rez['Eu']['NEAR'].append('EURUSD000TOD*CUR')
# 	rez['Eu']['NEAR'].append('EUR_RUB__TOM*CUR')
# 	rez['Eu']['NEAR'].append('EUR_RUB__TOD*CUR')
#
# 	# добавим сырье
# 	rez['GD']['NEAR'].append('Золото*RAW')
# 	rez['GD']['FAR'].append('Платина*RAW')
# 	rez['GD']['FAR'].append('Медь*RAW')
# 	rez['SV']['NEAR'].append('Серебро*RAW')
# 	rez['BR']['FAR'].append('Нефть WTI*RAW')
# 	rez['BR']['NEAR'].append('Нефть Brent*RAW')
# 	rez['BR']['FAR'].append('Мазут*RAW')
# 	rez['BR']['FAR'].append('Бензин*RAW')
# 	rez['NG']['NEAR'].append('Природный газ*RAW')
# 	rez['W4']['NEAR'].append('Пшеница*RAW')
# 	# добавим сбер
# 	rez['SR']['NEAR'].append('SBER*MOEX2')
# 	rez['SR']['FAR'] = copy.copy(rez['SP']['MAIN'])
# 	rez['SR']['FAR'].append('SBERP*MOEX2')
#
# 	rez['SP']['NEAR'].append('SBERP*MOEX2')
# 	rez['SP']['FAR'] = copy.copy(rez['SR']['MAIN'])
# 	rez['SP']['FAR'].append('SBER*MOEX2')
#
# 	# добавим америку
# 	for sym in a:
# 		if "MCT\\Futures\\" in a[sym]['path'] and a[sym]['expiration_time'] > tme + 86400:
# 			# print(sym, a[sym]['description'])
# 			if 'Natural Gas' in a[sym]['description']:
# 				rez['NG']['USAFUT'].append(sym + '*USAFUT')
# 			if 'Gasoline' in a[sym]['description']:
# 				rez['BR']['FAR'].append(sym + '*USAFUT')
# 			if 'Gold' in a[sym]['description']:
# 				rez['GD']['USAFUT'].append(sym + '*USAFUT')
# 			if 'Silver' in a[sym]['description']:
# 				rez['SV']['USAFUT'].append(sym + '*USAFUT')
# 			if 'Brent' in a[sym]['description']:
# 				rez['BR']['USAFUT'].append(sym + '*USAFUT')
# 			if 'EURUSD' in a[sym]['description']:
# 				rez['ED']['USAFUT'].append(sym + '*USAFUT')
#
# 	# for key in rez:
#
# 	# myset=set()
# 	# mysetmarkets = set()
# 	# for key in rez:
# 	# 	for key2 in rez[key]:
# 	# 		for inst in rez[key][key2]:
# 	# 			myset.add(inst)
# 	# 			mysetmarkets.add(inst.partition('*')[2])
#
# 	# print(myset)
# 	# print(mysetmarkets)
# 	return rez
#
#
# # year=2024
# # month=1
# # day=5
# #
# a = get_fut(time.time() - 100000)
#
# for i in a:
# 	print(i, a[i])

# 'USDRUBF*FRTS2', 'SiH4*FRTS2', 'SiH5*FRTS2', 'SiM4*FRTS2', 'SiM5*FRTS2', 'USD000UTSTOM*CUR', 'USD000000TOD*CUR'
import time
import datetime
from PROJECT.SBOR.my_lib  import *




def get_fut(tme):
	dat = datetime.datetime.utcfromtimestamp(int(tme))
	year = dat.year
	month =dat.month
	day = dat.day

	mysyms = {'GD', 'SV', 'BR', 'NG', 'W4', 'Eu', 'Si', 'MX','ED','SR','SP'}
	rez=dict()
	spinst = []
	infopath = 'G:\\SYMBOLS_INFO\\MOEXSYMBOLS_INFO'
	name = infopath + '\\' + str(year) + '\\' + str(month) + '\\' + str(day) + '.roman'
	a = myload(name)
	for key in a:
		if a[key]['exchange'] == 'ФОРТС' and a[key]['expiration_time']>tme+ 86400:
			spinst.append(key)


	# instset=set()
	# for inst in spinst:
	# 	bodyit = inst[:-2]
	# 	instset.add(bodyit)
	for i in mysyms:     #instset
		rez[i] = dict()
		rez[i]['MAIN']=[]
		rez[i]['NEAR'] = []
		rez[i]['FAR'] = []
		rez[i]['USAFUT'] = []
		for inst in spinst:
			bodyit = inst[:-2]
			if i == bodyit:
				rez[i]['MAIN'].append(inst+'*FRTS2')

	# # добавим вечные фьючи
	# # 'USDRUBF 'IMOEXF 'GLDRUBF    'EURRUBF  Si MX  GD   Eu
	rez['Si']['MAIN'].insert(0,'USDRUBF*FRTS2')
	rez['MX']['MAIN'].insert(0, 'IMOEXF*FRTS2')
	rez['GD']['MAIN'].insert(0, 'GLDRUBF*FRTS2')
	rez['Eu']['MAIN'].insert(0, 'EURRUBF*FRTS2')
	# # добавим форекс
	rez['ED']['NEAR'].append('EURUSD*FxCUR')
	rez['GD']['NEAR'].append('XAUUSD*FxMETBR')
	rez['SV']['NEAR'].append('XAGUSD*FxMETBR')
	rez['BR']['NEAR'].append('Brent*FxMETBR')
	rez['BR']['FAR'].append('Crude*FxMETBR')
	rez['NG']['NEAR'].append('NatGas*FxMETBR')
	rez['Si']['FAR'].append('USDind*FxMETBR')
	# добавим валютку   CURcross
	rez['Si']['NEAR'].append('USDRUB*CURcross')
	rez['Si']['NEAR'].append('USDRUR*CURcross')
	rez['Si']['NEAR'].append('USDRUB_TMS*CURcross')
	rez['Eu']['NEAR'].append('EURRUB*CURcross')
	rez['Eu']['NEAR'].append('EURRUR*CURcross')
	rez['Eu']['NEAR'].append('EURRUB_TMS*CURcross')

	# добавим валютку   CUR
	rez['Si']['NEAR'].append('USD000UTSTOM*CUR')
	rez['Si']['NEAR'].append('USD000000TOD*CUR')
	rez['Eu']['NEAR'].append('EURUSD000TOM*CUR')
	rez['Eu']['NEAR'].append('EURUSD000TOD*CUR')
	rez['Eu']['NEAR'].append('EUR_RUB__TOM*CUR')
	rez['Eu']['NEAR'].append('EUR_RUB__TOD*CUR')

	# добавим сырье
	rez['GD']['NEAR'].append('Золото*RAW')
	rez['GD']['FAR'].append('Платина*RAW')
	rez['GD']['FAR'].append('Медь*RAW')
	rez['SV']['NEAR'].append('Серебро*RAW')
	rez['BR']['FAR'].append('Нефть WTI*RAW')
	rez['BR']['NEAR'].append('Нефть Brent*RAW')
	rez['BR']['FAR'].append('Мазут*RAW')
	rez['BR']['FAR'].append('Бензин*RAW')
	rez['NG']['NEAR'].append('Природный газ*RAW')
	rez['W4']['NEAR'].append('Пшеница*RAW')
	# добавим сбер
	rez['SR']['NEAR'].append('SBER*MOEX2')
	rez['SR']['FAR']=rez['SP']['MAIN']
	rez['SR']['FAR'].append('SBERP*MOEX2')
	
	rez['SP']['NEAR'].append('SBERP*MOEX2')
	rez['SP']['FAR']=rez['SR']['MAIN']
	rez['SP']['FAR'].append('SBER*MOEX2')
	

	# добавим америку
	for sym in a:
		if "MCT\\Futures\\" in a[sym]['path']and a[sym]['expiration_time']>tme+ 86400:
			# print(sym, a[sym]['description'])
			if 'Natural Gas' in a[sym]['description']:
				rez['NG']['USAFUT'].append(sym + '*USAFUT')
			if 'Gasoline' in a[sym]['description']:
				rez['BR']['FAR'].append(sym + '*USAFUT')
			if 'Gold' in a[sym]['description']:
				rez['GD']['USAFUT'].append(sym + '*USAFUT')
			if 'Silver' in a[sym]['description']:
				rez['SV']['USAFUT'].append(sym + '*USAFUT')
			if 'Brent' in a[sym]['description']:
				rez['BR']['USAFUT'].append(sym + '*USAFUT')
			if 'EURUSD' in a[sym]['description']:
				rez['ED']['USAFUT'].append(sym + '*USAFUT')

	# for key in rez:

	# myset=set()
	# mysetmarkets = set()
	# for key in rez:
	# 	for key2 in rez[key]:
	# 		for inst in rez[key][key2]:
	# 			myset.add(inst)
	# 			mysetmarkets.add(inst.partition('*')[2])

	# print(myset)
	# print(mysetmarkets)
	return rez

# year=2024
# month=1
# day=5
#
# get_fut(year,month,day)



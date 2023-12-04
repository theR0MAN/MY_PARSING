import MetaTrader5 as mt5
import datetime
from threading import Thread
import time
import json
import os

if not mt5.initialize("E:\\FinamMT5\\terminal64.exe", timeout=40):
	print("initialize() failed, error code =", mt5.last_error(), "? once TRY again")
	print('SLEEP')
	time.sleep(10)
	if not mt5.initialize("E:\\FinamMT5\\terminal64.exe", timeout=30):
		print("QUIT!!!!!!!!!!!! initialize() failed, error code =", mt5.last_error())
		quit()
	else:
		print('initialize2 sucsess')
else:
	print('initialize1 sucsess')



symbols = mt5.symbols_get()
allsym = {}
for i in symbols:
	sym = i._asdict()
	if sym['name'] in allsym:
		print("fuckingsheat", sym['name'])
	else:
		allsym[sym['name']] = sym

t = int(time.time()) + 86400
# for sym in allsym:
# 	print(allsym[sym])
# 	# expt=allsym[sym]['expiration_time']
# 	if "MFUT\\" in allsym[sym]['path'] and allsym[sym]['expiration_time'] >t:
# 		print(sym, allsym[sym]['expiration_time'], allsym[sym]['path'])
#
# for sym in allsym:
# 	sym= allsym[sym]
# 	if "MOEX\\" in sym['path'] and  sym['expiration_time']>t:
# 		print(sym['name'],  sym['expiration_time'])


# for sym in allsym:
# 	sym= allsym[sym]
# 	if "MOEX\\" in sym['path'] and ( sym['expiration_time']>t or sym['expiration_time']==0 ) :
# 		name= sym['name']
# 		lnn=len(name)
# 		perf=name[:2]
# 		if lnn>10 and (perf=='XS' or perf=='RU' or perf=='SU' ):
# 			print(sym['name'],  sym['expiration_time'])
# 	else:
# 		pass       ETHEUR
# a={}
# name= 'Нефть Brent'
# print (mt5.market_book_add(name))
# stakan=mt5.market_book_get(name)
# print(stakan)
# print(type(stakan))
# asks = []
# bids = []
# for i in stakan:
# 	i = i._asdict()
# 	if i['type'] == 1:
# 		asks.append((i['price'], i['volume']))
# 	if i['type'] == 2:
# 		bids.append((i['price'], i['volume']))
# asks.reverse()
# if len(asks) > 0 and len(bids) > 0:
# 	if asks[0][0] > bids[0][0] and bids[0][0] > 0:
# 		a['asks'] = asks
# 		a['bids'] = bids
# 		Ask = a['asks'][0][0]
# 		Bid = a['bids'][0][0]
# print(a)
# count =0
# countst =0
# for sym in allsym:
# 	sym= allsym[sym]
# 	if "Indicative continuous\\Сырье\\" in sym['path'] :    #"MCUR\\crossrate"
# 		if mt5.market_book_add(sym['name']):
# 			print(sym['name'])
# 			countst+=1
name='Медь'
data = mt5.symbol_info(name)
symbol_info_dict = data._asdict()
Ask = symbol_info_dict['ask']
Bid = symbol_info_dict['bid']
print(Ask,"    ",Bid)
print (mt5.market_book_add(name))
stakan=mt5.market_book_get(name)
print(stakan)
# putpath = 'G:\\SYMBOLS_INFO\\'
# dat = datetime.datetime.utcfromtimestamp(int(time.time()))
# year = str(dat.year)
# month=str(dat.month)
# day = str(dat.day)
# name=year+'-'+month+'-'+day+'\\'
#
# if not os.path.exists(putpath + name):
# 	os.mkdir(putpath + name)
#
# symbols = mt5.symbols_get()
# allsym={}
# for i in symbols:
# 	sym = i._asdict()
# 	if sym['name'] in allsym:
# 		print("fuckingsheat",sym['name'] )
# 	else:
# 		allsym[sym['name']]=sym
#
# with open(putpath+name+'finammt5.json', "w") as file:
# 	json.dump(allsym, file)
#
# with open(putpath+name+'finammt5.json', "r") as read_file:
# 	data = json.load(read_file)
#
# for key in data:
# 	print(data[key])

#
# t=int(time.time()) +86400

# count=0
# for sym in symbols:
# 	sym = sym._asdict()
# 	if "MFUT\\" in sym['path'] and sym['expiration_time']>t :
# 		print(sym['path'],sym['expiration_time'] )
# 		count+=1
# print(count)


# count=0
# for sym in symbols:
# 	sym = sym._asdict()
# 	if "MFUT\\" in sym['path']:  #"MFUT\\" in sym['path']
# #
# 		mt5.market_book_release(sym['name'])
# 		mt5.symbol_select(sym['name'], False)
#
# print(count)
# time.sleep(2)
# mt5.market_book_add('AA.US')
# time.sleep(10)
# mt5.market_book_release('AA.US')
# mt5.symbol_select('AA.US', False)    'USDRUR'

#
# name = 'SiZ3'
# z = mt5.market_book_add(name)
#
# Askst0 = 0
# Bidst0 = 0
# Ask0 = 0
# Bid0 = 0
#
# while True:
# 	time.sleep(0.01)
# 	symbol_info_dict = mt5.symbol_info(name)._asdict()
# 	Ask = symbol_info_dict['ask']
# 	Bid = symbol_info_dict['bid']
#
# 	stakan = mt5.market_book_get(name)
# 	Askst = 0
# 	Bidst = 0
#
# 	if stakan != None and z:
# 		asks = []
# 		bids = []
# 		for i in stakan:
# 			i = i._asdict()
# 			if i['type'] == 1:
# 				asks.append((i['price'], i['volume']))
# 			if i['type'] == 2:
# 				bids.append((i['price'], i['volume']))
# 		asks.reverse()
# 		if len(asks) > 0 and len(bids) > 0:
# 			if asks[0][0] > bids[0][0]:
# 				Askst = asks[0][0]
# 				Bidst = bids[0][0]
#
#
#
# 	if Ask!= Askst or Bid!= Bidst:
# 		print(f'ERROR!!!!!! Ask= {Ask} Askst={Askst}     Bid= {Bid} Bidst= {Bidst}  ')
#
# 	if Ask!= Ask0 or Bid!= Bid0 or Askst!= Askst0 or Bidst!= Bidst0 :
# 		Askst0 = Askst
# 		Bidst0 = Bidst
# 		Ask0 = Ask
# 		Bid0 = Bid
# 		print(f'Ask= {Ask} Askst={Askst}     Bid= {Bid} Bidst= {Bidst}  ')

# mt5.symbol_select('AA.US', True)

# mt5.market_book_release('AA.US')
# mt5.symbol_select('AA.US', False)
# #
# asks = []
# bids = []
# count=0
# count1=0
# count2=0
# for sym in symbols:
# 	sym = sym._asdict()
# 	if  "MFUT\\" in sym['path'] and sym['expiration_time'] > t  : #and (sym['expiration_time'] > t or sym['expiration_time']==0)
# 		count2 += 1
# 		# print(sym['name'])
# 		# mt5.symbol_select(sym['name'], True)
# 		if mt5.market_book_add(sym['name']):
# 			count1+=1
# 			asks=[]
# 			bids=[]
#
# 			stakan = mt5.market_book_get(sym['name'])
# 			for i in stakan:
# 				i = i._asdict()
# 				if i['type'] == 1:
# 					asks.append((i['price'], i['volume']))
# 				if i['type'] == 2:
# 					bids.append((i['price'], i['volume']))
# 			asks.reverse()
# 			if len(asks) > 0 and len(bids) > 0:
# 				if asks[0][0] > bids[0][0]:
# 					a = dict()
# 					a['asks'] = asks
# 					a['bids'] = bids
# 					print(sym['name'],a)
# 					count+=1
# else:
# 	mt5.market_book_release(sym['name'])
# 	mt5.symbol_select(sym['name'], False)


#
# print(count)
# print(count1)
# print(count2)

# count=0
# for sym in symbols:
# 	sym = sym._asdict()
# 	if "SPBEX\\" in sym['path'] and (sym['expiration_time'] > t or sym['expiration_time']==0):
# 		if mt5.market_book_add(sym['name']):
# 			print(sym['path'], sym['expiration_time'])
# 			count += 1
# 		else:
# 			print(sym['name'], sym['expiration_time'],'      FALSE')
#
# print(count)

# count=0
# for sym in symbols:
# 	sym = sym._asdict()
# 	if  sym['expiration_time']>t or sym['expiration_time']==0:
# 		print(sym['path'],sym['expiration_time'] )
# 		count+=1
# print(count)   ADM.SPB
# asks=[]
# bids=[]
# #
# if mt5.market_book_add('AA.US'):
# 	stakan = mt5.market_book_get('AA.US')
# 	for i in stakan:
# 		i = i._asdict()
# 		if i['type'] == 1:
# 			asks.append((i['price'], i['volume']))
# 		if i['type'] == 2:
# 			bids.append((i['price'], i['volume']))
# 	asks.reverse()
# 	if len(asks) > 0 and len(bids) > 0:
# 		if asks[0][0] > bids[0][0]:
# 			a = dict()
# 			a['asks'] = asks
# 			a['bids'] = bids
# 			print( a)
# 	else:
# 		print('SHIT')

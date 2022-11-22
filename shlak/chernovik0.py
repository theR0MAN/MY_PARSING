import MetaTrader5 as mt5
import json
from platform import system
from multiprocessing import Process
import time
import os
import lzma
import datetime

putpath = 'G:\\DATA_SBOR\\MOEX'

startsbor_hour = 0
stopsbor_hour = 23  # при переходе через 0 может быть ошибочно - поправить,но для мосбиржи пойдет


def arhivator(filename, jdict):
	print(f' start arhivator   {filename}')
	with lzma.open(filename, "w") as f:
		f.write(lzma.compress(json.dumps(jdict).encode('utf-8')))


if system() == 'Windows':
	dL = '\\'
else:
	dL = '/'

if not mt5.initialize("G:\\Открытие ФОРТС\\terminal64.exe", timeout=30):
	print("initialize() failed, error code =", mt5.last_error(), "? once TRY again")
	time.sleep(10)
	if not mt5.initialize("G:\\Открытие ФОРТС\\terminal64.exe", timeout=30):
		print("QUIT!!!!!!!!!!!! initialize() failed, error code =", mt5.last_error())
		quit()
	else:
		print('initialize2 sucsess')
else:
	print('initialize1 sucsess')

zapis = False
sbor = False
first_thour = -10
a = dict()
data = dict()
while True:
	time.sleep(1)
	dat = datetime.datetime.utcfromtimestamp(int(time.time()))
	year = dat.year
	month = dat.month
	day = dat.day
	hour = dat.hour
	minute = dat.minute
	second = dat.second

	if first_thour != hour and dat.hour >= startsbor_hour and dat.hour <= stopsbor_hour:
		first_thour = hour
		a = dict()
		data = dict()
		symbols = mt5.symbols_get()
		for i in symbols:
			i = i._asdict()
			# print(i)
			if "RTS\\FORTS\\" in i['path'] and 'Expired' not in i['path'] and 'Splice' not in i['name']:  # Expired
				if mt5.market_book_add(i['name']):
					a[i['name']] = dict()
					data[i['name']] = dict()
					data[i['name']]['makret'] = 'FRTS'
					data[i['name']]['a'] = 0
					data[i['name']]['vola'] = 0
					data[i['name']]['b'] = 0
					data[i['name']]['volb'] = 0

			if "MOEX\\Securities\\TQBR\\" in i['path']:
				if mt5.market_book_add(i['name']):
					a[i['name']] = dict()
					data[i['name']] = dict()
					data[i['name']]['makret'] = 'MOEX'
					data[i['name']]['a'] = 0
					data[i['name']]['vola'] = 0
					data[i['name']]['b'] = 0
					data[i['name']]['volb'] = 0
		time.sleep(3)
		if len(a) > 0:
			sbor = True
		else:
			sbor = False
		print(f'sbor= {sbor}   zapis= {zapis}')

		# ///////////////////////////////////////////////////////////////////////////////////////////////
		if zapis:
			zapis = False
			nextpath = putpath + dL + str(year)
			if not os.path.exists(nextpath):
				os.mkdir(nextpath)
			nextpath = nextpath + dL + str(month)
			if not os.path.exists(nextpath):
				os.mkdir(nextpath)
			nextpath = nextpath + dL + str(day)
			if not os.path.exists(nextpath):
				os.mkdir(nextpath)
			hourf = 23 if hour == 0 else hour - 1
			fullname = nextpath + dL + str(hourf) + '.roman'

			for name in data:
				print("a[name]=", a[name])
				print("data[name]=", data[name])
			# a[name + '*' + data['name']['makret']] = a.pop(name)

			if __name__ == '__main__':
				print("process")
				process1 = Process(target=arhivator, args=(fullname, a))
				process1.start()

	# ///////////////////////////////////////////////////////////////////////////////////////////////
	timekey = str(minute * 60 + second)
	for name in data:
		stakan = mt5.market_book_get(name)
		asks = []
		bids = []
		for i in stakan:
			i = i._asdict()
			if i['type'] == 1:
				asks.append((i['price'], i['volume']))
			if i['type'] == 2:
				bids.append((i['price'], i['volume']))
		asks.reverse()

		if len(asks) > 0 and len(bids) > 0 and asks[0][0] > bids[0][0] and \
				(asks[0][0] != data[name]['a'] or bids[0][0] != data[name]['b']
				 or asks[0][1] != data[name]['vola'] or data[name]['volb'] != bids[0][1]):
			zapis = True
			a[name][timekey] = dict()
			a[name][timekey]['a'] = asks[0][0]
			a[name][timekey]['b'] = bids[0][0]
			a[name][timekey]['asks'] = asks
			a[name][timekey]['bids'] = bids

			data[name]['a'] = asks[0][0]
			data[name]['vola'] = asks[0][1]
			data[name]['b'] = bids[0][0]
			data[name]['volb'] = bids[0][1]

	# print(f" name= {name}  timekey={timekey}  ask= {a[name][timekey]['a']}   bid={a[name][timekey]['b']}  ")
# ///////////////////////////////////////////////////////////////////////////////////////////////


import random
import lzma
import subprocess
import json
from platform import system
from threading import Thread
import time
import os
import lzma
import datetime
import pandas as pd
from multiprocessing import Process


def viz_stakan2(a, a2):
	def frmt(value, len_zapis, prefix, zapoln):
		v1 = (str(value) + prefix)[:len_zapis]
		if len(v1) < len_zapis:
			v1 += (len_zapis - len(v1)) * zapoln
		return v1

	if len(a) == 0:
		print('len<0  quit')
		quit()

	# шаг цены и ширина ячейки объема
	masrazn = []
	maxlen = 0
	for key in a:
		bidcens = []
		askcens = []
		for i in a[key]['asks']:
			askcens.append(i[0])
			maxlen = max(maxlen, len(str(i[1])))
		for i in a[key]['bids']:
			bidcens.append(i[0])
			maxlen = max(maxlen, len(str(i[1])))
		askcens.reverse()
		z = askcens + bidcens
		for i in range(1, len(z)):
			razn = z[i - 1] - z[i]
			masrazn.append(razn)
	shag = min(masrazn)

	# первый midl  a
	firstask = a[next(iter(a))]['asks'][0][0]
	firstbid = a[next(iter(a))]['bids'][0][0]
	firstmeda = (firstbid + firstask) / 2

	# первый midl  b
	firstask = a2[next(iter(a2))]['asks'][0][0]
	firstbid = a2[next(iter(a2))]['bids'][0][0]
	firstmeda2 = (firstbid + firstask) / 2

	koefa2a = firstmeda / firstmeda2
	# Нормализация цен второго массива к мервому с привязкой по первой медиане
	a3 = {}
	for key in a2:
		for cenlist in a2[key]['asks']:
			maxlen = max(maxlen, len(str(cenlist[1])))
		for cenlist in a2[key]['bids']:
			maxlen = max(maxlen, len(str(cenlist[1])))

	maxlen += 2
	for key in a2:
		a3[key] = dict()
		a3[key]['asks'] = []
		a3[key]['bids'] = []
		for cenlist in a2[key]['asks']:
			a3[key]['asks'].append([round(cenlist[0] * koefa2a / shag) * shag, frmt(cenlist[1], maxlen, "ps", ' ')])
		# print(f'{koefa2a} cenlist  {cenlist}    a3[key]["asks"]   {a3[key]["asks"]}')
		for cenlist in a2[key]['bids']:
			a3[key]['bids'].append([round(cenlist[0] * koefa2a / shag) * shag, frmt(cenlist[1], maxlen, "ms", ' ')])

	# переформатну ка я первый словарь по объемам
	a0 = {}
	for key in a:
		a0[key] = dict()
		a0[key]['asks'] = []
		a0[key]['bids'] = []
		for cenlist in a[key]['asks']:
			a0[key]['asks'].append([cenlist[0], frmt(cenlist[1], maxlen, "pf", ' ')])
		# print(f'{koefa2a} cenlist  {cenlist}    a3[key]["asks"]   {a0[key]["asks"]}')
		for cenlist in a[key]['bids']:
			a0[key]['bids'].append([cenlist[0], frmt(cenlist[1], maxlen, "mf", ' ')])

	# имеем два словаря	a0  a3 , замержим их
	# переименую, бо некрасиво, брутфорс -сила
	c1 = a0
	c2 = a3
	lastc1 = c1[next(iter(c1))]
	lastc2 = c2[next(iter(c2))]

	d3 = {}
	numc = 1
	startkey = min(int(next(iter(c1))), int(next(iter(c2))))
	print(startkey)
	for ikey in range(startkey, 3600):
		yes = False
		if str(ikey) in c1:
			lastc1 = c1[str(ikey)]
			yes = True
		if str(ikey) in c2:
			lastc2 = c2[str(ikey)]
			yes = True

		if yes:
			d3[str(numc)] = lastc1
			d3[str(numc + 1)] = lastc2
			numc += 2

	# максимум и минимум цены
	masmax = []
	masmin = []
	for key in d3:
		masmax.append(d3[key]['asks'][len(d3[key]['asks']) - 1][0])
		masmin.append(d3[key]['bids'][len(d3[key]['bids']) - 1][0])

	mx = max(masmax)
	mn = min(masmin)

	# количество шагов
	kvo_str = int((mx - mn) / shag)
	# строка по первому аску , заодно  формула номера строки для цен
	first = int((mx - firstask) / shag)
	# вывод шкалы процентных изменений цены от первой цены аск,  - первый столбец
	koef = 100 / firstmeda
	mmax = mx * koef
	mshag = shag * koef
	skala = []
	for i in range(kvo_str):
		skala.append(round(mmax - mshag * i, 2))
	# нормализация словаря замена  таймстампа на столбцы, цен -на строки, объемы аски с "+" биды с"-"
	# первц столбец -на шкалу
	# maxstlb=12000/maxlen
	b = {}
	for key in d3:
		b[key] = dict()
		b[key]['asks'] = {}
		b[key]['bids'] = {}
		b[key]['all'] = {}
		for n in d3[key]['asks']:
			b[key]['asks'][str(int((mx - n[0]) / shag))] = n[1]
		for n in d3[key]['bids']:
			b[key]['bids'][str(int((mx - n[0]) / shag))] = n[1]
		# соединяем аски и биды  в один словарь
		b[key]['all'] = b[key]['asks'] | b[key]['bids']
	kvo_stlb = len(b) + 1

	# переводим словарь в массив
	mas = [(maxlen) * " "] * kvo_str
	for i in range(kvo_str):
		mas[i] = [(maxlen) * " "] * kvo_stlb
	for i in range(kvo_str):
		mas[i][0] = frmt(skala[i], 10, " ", ' ')
	for i in range(kvo_str):
		for j in range(1, kvo_stlb):
			if str(j) in b and str(i) in b[str(j)]['all']:
				mas[i][j] = b[str(j)]['all'][str(i)]
	with open('STAKAN.txt', mode='w') as f:
		for i in range(kvo_str):
			f.write(''.join(mas[i]) + '\n')

	df = pd.DataFrame(mas)
	df.to_excel('F:\\Все\\MY_PARSING\\GENERAL\\teams.xlsx', index=False, header=False)
	print(df)
	# subprocess.run(["C:\\Users\\milro\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe", "STAKAN.txt"])
	os.system('start excel.exe teams.xlsx')


def viz_stakan1(a):
	def frmt(value, len_zapis, prefix, zapoln):
		v1 = (str(value) + prefix)[:len_zapis]
		if len(v1) < len_zapis:
			v1 += (len_zapis - len(v1)) * zapoln
		return v1

	if len(a) == 0:
		print('len<0  quit')
		quit()

	# шаг цены и ширина ячейки объема
	masrazn = []
	maxlen = 0
	for key in a:
		bidcens = []
		askcens = []
		for i in a[key]['asks']:
			askcens.append(i[0])
			maxlen = max(maxlen, len(str(i[1])))
		for i in a[key]['bids']:
			bidcens.append(i[0])
			maxlen = max(maxlen, len(str(i[1])))
		askcens.reverse()
		z = askcens + bidcens
		for i in range(1, len(z)):
			razn = z[i - 1] - z[i]
			masrazn.append(razn)
	shag = min(masrazn)

	# первый midl  a
	firstask = a[next(iter(a))]['asks'][0][0]
	firstbid = a[next(iter(a))]['bids'][0][0]
	firstmeda = (firstbid + firstask) / 2

	maxlen += 2
	# переформатну ка я первый словарь по объемам
	a0 = {}
	for key in a:
		a0[key] = dict()
		a0[key]['asks'] = []
		a0[key]['bids'] = []
		for cenlist in a[key]['asks']:
			a0[key]['asks'].append([cenlist[0], frmt(cenlist[1], maxlen, "pf", ' ')])
		for cenlist in a[key]['bids']:
			a0[key]['bids'].append([cenlist[0], frmt(cenlist[1], maxlen, "mf", ' ')])

	# имеем два словаря	a0  a3 , замержим их
	# переименую, бо некрасиво, брутфорс -сила
	lastc1 = a0[next(iter(a0))]

	d3 = {}
	numc = 1
	startkey = int(next(iter(a0)))
	print(startkey)
	for ikey in range(startkey, 3600):
		if str(ikey) in a0:
			lastc1 = a0[str(ikey)]
			d3[str(numc)] = lastc1
			numc += 1

	# максимум и минимум цены
	masmax = []
	masmin = []
	for key in d3:
		masmax.append(d3[key]['asks'][len(d3[key]['asks']) - 1][0])
		masmin.append(d3[key]['bids'][len(d3[key]['bids']) - 1][0])

	mx = max(masmax)
	mn = min(masmin)

	# количество шагов
	kvo_str = int((mx - mn) / shag)
	# строка по первому аску , заодно  формула номера строки для цен
	first = int((mx - firstask) / shag)
	# вывод шкалы процентных изменений цены от первой цены аск,  - первый столбец
	koef = 100 / firstmeda
	mmax = mx * koef
	mshag = shag * koef
	skala = []
	for i in range(kvo_str):
		skala.append(round(mmax - mshag * i, 2))
	# нормализация словаря замена  таймстампа на столбцы, цен -на строки, объемы аски с "+" биды с"-"
	# первц столбец -на шкалу
	# maxstlb=12000/maxlen
	b = {}
	for key in d3:
		b[key] = dict()
		b[key]['asks'] = {}
		b[key]['bids'] = {}
		b[key]['all'] = {}
		for n in d3[key]['asks']:
			b[key]['asks'][str(int((mx - n[0]) / shag))] = n[1]
		for n in d3[key]['bids']:
			b[key]['bids'][str(int((mx - n[0]) / shag))] = n[1]
		# соединяем аски и биды  в один словарь
		b[key]['all'] = b[key]['asks'] | b[key]['bids']
	kvo_stlb = len(b) + 1

	# переводим словарь в массив
	mas = [(maxlen) * " "] * kvo_str
	for i in range(kvo_str):
		mas[i] = [(maxlen) * " "] * kvo_stlb
	for i in range(kvo_str):
		mas[i][0] = frmt(skala[i], 10, " ", ' ')
	for i in range(kvo_str):
		for j in range(1, kvo_stlb):
			if str(j) in b and str(i) in b[str(j)]['all']:
				mas[i][j] = b[str(j)]['all'][str(i)]
	with open('STAKAN.txt', mode='w') as f:
		for i in range(kvo_str):
			f.write(''.join(mas[i]) + '\n')

	df = pd.DataFrame(mas)
	df.to_excel('F:\\Все\\MY_PARSING\\GENERAL\\teams.xlsx', index=False, header=False)
	print(df)
	# subprocess.run(["C:\\Users\\milro\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe", "STAKAN.txt"])
	os.system('start excel.exe teams.xlsx')


def get_color():
	i = -1

	def func():
		colors = ['black', 'red', 'blue', 'brown', 'green', 'violet', 'yellow', 'maroon', 'gold', 'pink', 'silver',
				  'coral', 'chocolate']
		colors0 = ['aliceblue', 'antiquewhite', 'aqua', 'aquamarine', 'azure',
				   'beige', 'bisque', 'black', 'blanchedalmond', 'blue',
				   'blueviolet', 'brown', 'burlywood', 'cadetblue',
				   'chartreuse', 'chocolate', 'coral', 'cornflowerblue',
				   'cornsilk', 'crimson', 'cyan', 'darkblue', 'darkcyan',
				   'darkgoldenrod', 'darkgray', 'darkgrey', 'darkgreen',
				   'darkkhaki', 'darkmagenta', 'darkolivegreen', 'darkorange',
				   'darkorchid', 'darkred', 'darksalmon', 'darkseagreen',
				   'darkslateblue', 'darkslategray', 'darkslategrey',
				   'darkturquoise', 'darkviolet', 'deeppink', 'deepskyblue',
				   'dimgray', 'dimgrey', 'dodgerblue', 'firebrick',
				   'floralwhite', 'forestgreen', 'fuchsia', 'gainsboro',
				   'ghostwhite', 'gold', 'goldenrod', 'gray', 'grey', 'green',
				   'greenyellow', 'honeydew', 'hotpink', 'indianred', 'indigo',
				   'ivory', 'khaki', 'lavender', 'lavenderblush', 'lawngreen',
				   'lemonchiffon', 'lightblue', 'lightcoral', 'lightcyan',
				   'lightgoldenrodyellow', 'lightgray', 'lightgrey',
				   'lightgreen', 'lightpink', 'lightsalmon', 'lightseagreen',
				   'lightskyblue', 'lightslategray', 'lightslategrey',
				   'lightsteelblue', 'lightyellow', 'lime', 'limegreen',
				   'linen', 'magenta', 'maroon', 'mediumaquamarine',
				   'mediumblue', 'mediumorchid', 'mediumpurple',
				   'mediumseagreen', 'mediumslateblue', 'mediumspringgreen',
				   'mediumturquoise', 'mediumvioletred', 'midnightblue',
				   'mintcream', 'mistyrose', 'moccasin', 'navajowhite', 'navy',
				   'oldlace', 'olive', 'olivedrab', 'orange', 'orangered',
				   'orchid', 'palegoldenrod', 'palegreen', 'paleturquoise',
				   'palevioletred', 'papayawhip', 'peachpuff', 'peru', 'pink',
				   'plum', 'powderblue', 'purple', 'red', 'rosybrown',
				   'royalblue', 'rebeccapurple', 'saddlebrown', 'salmon',
				   'sandybrown', 'seagreen', 'seashell', 'sienna', 'silver',
				   'skyblue', 'slateblue', 'slategray', 'slategrey', 'snow',
				   'springgreen', 'steelblue', 'tan', 'teal', 'thistle', 'tomato',
				   'turquoise', 'violet', 'wheat', 'white', 'whitesmoke',
				   'yellow', 'yellowgreen']
		nonlocal i
		i += 1
		if i < 13:
			return colors[i]
		else:
			return random.choice(colors0)

	return func

def  get_dict(cont):
	lz=lzma
	a=dict()
	for name in cont:
		with lz.open(name) as f:
			bb = dict(json.loads(lz.decompress(f.read()).decode('utf-8')))
		a |= bb
	return a

def getdata_merge(onlymerge, minutki, markets, getpath, start_year, start_month, start_day, start_hour, stop_year,
				  stop_month, stop_day, stop_hour):
	"""  возвращает список списков файлов по маркетам в виде
			[['G:\\DATA_SBOR\\FRTS\\2023\\5\\16\\10_mnt.roman', 'G:\\DATA_SBOR\\MOEX\\2023\\5\\16\\10_mnt.roman'],
		 ['G:\\DATA_SBOR\\FRTS\\2023\\5\\16\\11_mnt.roman', 'G:\\DATA_SBOR\\MOEX\\2023\\5\\16\\11_mnt.roman']
	"""
	fln = '_mnt.roman' if minutki else '.roman'
	dL = '\\' if system() == 'Windows' else '/'

	getpath = getpath + dL + markets[0]
	if stop_year < start_year \
			or stop_year == start_year and stop_month < start_month \
			or stop_year == start_year and stop_month == start_month and stop_day < start_day \
			or stop_year == start_year and stop_month == start_month and stop_day == start_day and stop_hour < start_hour:
		print("  ошибка введенный конец периода начинается раньше его начала ")
		quit()
	if start_month > 12 or stop_month > 12 or start_day > 31 or stop_day > 31 or start_hour > 23 or stop_hour > 23:
		print(" Ошибка - введено хреновое время")
		quit()
	if start_month <= 0 or stop_month <= 0 or start_day <= 0 or stop_day <= 0 or start_hour < 0 or stop_hour < 0:
		print("Ошибка - введено отрицательное время")
		quit()
	global name
	listfiles = []
	flag = False
	for y in range(start_year, stop_year + 1):
		name1 = getpath + dL + str(y)
		if flag:
			break
		if not os.path.exists(name1):
			continue
		for m in range(start_month, 13):
			name2 = name1 + dL + str(m)
			if flag:
				break
			if not os.path.exists(name2):
				continue
			for d in range(start_day, 32):
				name3 = name2 + dL + str(d)
				if flag:
					break
				if not os.path.exists(name3):
					continue
				for h in range(start_hour, 24):
					name10 = name3 + dL + str(h) + fln

					if os.path.exists(name10):
						listfiles.append(name10)

					if y > stop_year or \
							y == stop_year and m > stop_month or \
							y == stop_year and m == stop_month and d > stop_day or \
							y == stop_year and m == stop_month and d == stop_day and h >= stop_hour:
						flag = True
						break
				start_hour = 0
			start_day = 1
		start_month = 1

		# podlist = []
		# for market in markets:
		#     z = name10.replace(markets[0], market)
		#     if os.path.exists(z):
		#         podlist.append(z)
		# listfiles.append(podlist)
	listfiles2 = []
	for file in listfiles:
		podlist = []
		podlist.append(file)
		for market in markets[1:]:
			z = file.replace(markets[0], market)
			if os.path.exists(z):
				podlist.append(z)
		# print(len(podlist),'==',len(markets))
		#   Гребаная срань. Разбирался что я тут написал больше чем писал))
		# onlymerge - если тру, то добавляюся в список файлов файлы только если существуют файлы по всем маркетам за данный час, иначе -не добавляется ничего.
		if onlymerge:
			if len(podlist) == len(markets):
				listfiles2.append(podlist)
		else:
			# ели не онлимердж, то добавляется файлы вне зависимости, существуют ли файлы по другим маркетам за данный период.
			listfiles2.append(podlist)
	return listfiles2


class Histwrite2:
	def __init__(self, path=None, market=None):
		self.path = path
		self.market = market
		self.hr = None
		self.a = {}
		self.a_izm = {}
		self.zapis = False

	def putter(self, instr_name, dict_data):
		instr_name += "*" + self.market
		dat = datetime.datetime.utcfromtimestamp(int(time.time()))
		hour = dat.hour
		timekey = str(dat.minute * 60 + dat.second)
		if hour != self.hr:
			self.hr = hour
			if self.zapis:
				self.write_compress(self.a)
				# Thread(target=self.write_compress(), daemon=True).start()
				self.a = {}
				self.a_izm = {}
				self.zapis = False
			# self.mints =0

		if not instr_name in self.a:
			self.a_izm[instr_name] = dict_data
			self.a[instr_name] = {}
			self.a[instr_name][timekey] = dict_data
		if self.a_izm[instr_name] != dict_data:
			self.a_izm[instr_name] = dict_data
			self.a[instr_name][timekey] = dict_data
			self.zapis = True

	def get_filename(self):
		dL = '\\' if system() == 'Windows' else '/'
		dat = datetime.datetime.utcfromtimestamp(int(time.time()) - 3000)  # -открутим пару сек
		year = dat.year
		month = dat.month
		day = dat.day
		hour = dat.hour
		# self.mints= datetime.datetime(year, month, day, hour).timestamp()

		nextpath = self.path + dL + self.market
		if not os.path.exists(nextpath):
			os.mkdir(nextpath)
		nextpath = nextpath + dL + str(year)
		if not os.path.exists(nextpath):
			os.mkdir(nextpath)
		nextpath = nextpath + dL + str(month)
		if not os.path.exists(nextpath):
			os.mkdir(nextpath)
		nextpath = nextpath + dL + str(day)
		if not os.path.exists(nextpath):
			os.mkdir(nextpath)
		return nextpath + dL + str(hour)

	@staticmethod
	def find_key(dct, key):
		if key in dct:
			return key
		else:
			for i in range(int(key) - 1, -1, -1):
				if str(i) in dct:
					return str(i)

	def write_compress(self, data):
		namefile = self.get_filename()
		namefileLZ = namefile + '.roman'
		namefileJS = namefile + '_mnt.roman'
		Thread(target=self.COMRESS,args=(namefileLZ, data,)).start()
		Thread(target=self.COMRESSmin, args=(namefileJS,data, )).start()


	def COMRESS(self,namefile,data):
		# результат записи пример
#  '2243': {
# 			'asks': [[79430.0, 21], [79435.0, 2], [79436.0, 2], [79438.0, 1], [79439.0, 13], [79440.0, 4], [79441.0, 5],
# 					 [79443.0, 1], [79449.0, 5], [79457.0, 1], [79460.0, 6], [79461.0, 2], [79499.0, 10], [79500.0, 3],
# 					 [79550.0, 5], [79559.0, 2], [79591.0, 1], [79600.0, 11], [79646.0, 1], [79650.0, 3]],
# 			'bids': [[79419.0, 4], [79418.0, 3], [79417.0, 3], [79416.0, 8], [79413.0, 12], [79400.0, 9], [79385.0, 2],
# 					 [79352.0, 1], [79351.0, 2], [79350.0, 12], [79348.0, 1], [79320.0, 1], [79315.0, 1], [79310.0, 1],
# 					 [79301.0, 1], [79290.0, 54], [79285.0, 2], [79282.0, 8], [79266.0, 5], [79263.0, 5]]},
# '2244': {
# 			'asks': [[79439.0, 11], [79447.0, 2], [79448.0, 4], [79449.0, 6], [79450.0, 5], [79451.0, 2], [79460.0, 6],
# 					 [79469.0, 1], [79476.0, 2], [79499.0, 10], [79500.0, 3], [79550.0, 5], [79559.0, 2], [79591.0, 1],
# 					 [79600.0, 11], [79646.0, 1], [79650.0, 3], [79663.0, 3], [79664.0, 1], [79680.0, 1]],
# 			'bids': [[79431.0, 8], [79430.0, 4], [79429.0, 2], [79428.0, 6], [79427.0, 3], [79400.0, 9], [79394.0, 2],
# 					 [79352.0, 1], [79351.0, 2], [79350.0, 12], [79348.0, 1], [79320.0, 1], [79315.0, 1], [79310.0, 1],
# 					 [79301.0, 1], [79290.0, 54], [79285.0, 2], [79282.0, 8], [79266.0, 5], [79263.0, 5]]},

		lz = lzma
		with lz.open(namefile, "w") as f:
			print("   СТАРТ ЗАПИСИ  ", namefile)
			f.write(lz.compress(json.dumps(data).encode('utf-8')))
			print( "   ЗАПИСАНО   ", namefile)

	def COMRESSmin(self,namefile, data):
		# Вытаскиваем минутки from  a_cop
		# пример записи минуток
		# {'1': {'a': 79401.0, 'b': 79394.0}, '2': {'a': 79427.0, 'b': 79416.0}, '3': {'a': 79428.0, 'b': 79417.0},
		mina = {}
		for inst in data:
			mina[inst] = {}
			first_key = int(next(iter(data[inst])))
			d = 60
			first_key = int(first_key / d) * d + d

			for i in range(first_key, 3600, d):
				# mymin= str(int((self.mints+i)/60))
				mymin = str(int(i / 60))
				mina[inst][mymin] = {}
				key = self.find_key(data[inst], str(i))
				if key != None:
					try:
						mina[inst][mymin]["a"] = data[inst][key]['asks'][0][0]
						mina[inst][mymin]["b"] = data[inst][key]['bids'][0][0]
					except:
						mina[inst][mymin]["a"] = data[inst][key]['a']
						mina[inst][mymin]["b"] = data[inst][key]['b']
		lz = lzma
		with lz.open(namefile, "w") as f:
			print("   СТАРТ ЗАПИСИ  ", namefile)
			f.write(lz.compress(json.dumps(mina).encode('utf-8')))
			print( "   ЗАПИСАНО   ", namefile)

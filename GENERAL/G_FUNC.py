import random
import subprocess
import json
from platform import system
from threading import Thread
import time
import os
import lzma
import datetime


def viz_stakan(a):
	def frmt(value, len_zapis, prefix, zapoln):
		v1 = (prefix + str(value))[:len_zapis]
		if len(v1) < len_zapis:
			v1 += (len_zapis - len(v1)) * zapoln
		return v1
	# максимум и минимум цены
	masmax = []
	masmin = []
	for key in a:
		masmax.append(a[key]['asks'][len(a[key]['asks']) - 1][0])
		masmin.append(a[key]['bids'][len(a[key]['bids']) - 1][0])
	mx = max(masmax)
	mn = min(masmin)
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
	shag = int(min(masrazn))
	maxlen += 1
	# первый аск
	firstask = a[next(iter(a))]['asks'][0][0]
	# первый bid
	firstbid = a[next(iter(a))]['bids'][0][0]
	firstmed = (firstbid + firstask) / 2
	# количество шагов
	kvo_str = int((mx - mn) / shag)
	# строка по первому аску , заодно  формула номера строки для цен
	first = int((mx - firstask) / shag)
	# вывод шкалы процентных изменений цены от первой цены аск,  - первый столбец
	koef = 100 / firstmed
	mmax = mx * koef
	mshag = shag * koef
	skala = []
	for i in range(kvo_str):
		skala.append(round(mmax - mshag * i, 2))
	# нормализация словаря замена  таймстампа на столбцы, цен -на строки, объемы аски с "+" биды с"-"
	# первц столбец -на шкалу
	b = {}
	nom_stlb = 0
	for key in a:
		nom_stlb += 1
		b[str(nom_stlb)] = dict()
		b[str(nom_stlb)]['asks'] = {}
		b[str(nom_stlb)]['bids'] = {}
		b[str(nom_stlb)]['all'] = {}
		for n in a[key]['asks']:
			b[str(nom_stlb)]['asks'][str(int((mx - n[0]) / shag))] = frmt(n[1], maxlen, "+", ' ')
		for n in a[key]['bids']:
			b[str(nom_stlb)]['bids'][str(int((mx - n[0]) / shag))] = frmt(n[1], maxlen, "-", ' ')
		# соединяем аски и биды  в один словарь
		b[str(nom_stlb)]['all'] = b[str(nom_stlb)]['asks'] | b[str(nom_stlb)]['bids']
	kvo_stlb = len(b) + 1

	# переводим словарь в массив
	mas = [maxlen * " "] * kvo_str
	for i in range(kvo_str):
		mas[i] = [maxlen * " "] * kvo_stlb
	for i in range(kvo_str):
		mas[i][0] = frmt(skala[i], 10, "", ' ')
	for i in range(kvo_str):
		for j in range(1, kvo_stlb):
			if str(j) in b and str(i) in b[str(j)]['all']:
				mas[i][j] = b[str(j)]['all'][str(i)]
	with open('STAKAN.txt', mode='w') as f:
		for i in range(kvo_str):
			f.write(''.join(mas[i]) + '\n')

	subprocess.run(["C:\\Users\\milro\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe", "STAKAN.txt"])

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
        if i<13:
            return colors[i]
        else:
            return random.choice(colors0)
    return func


def getdata_merge(onlymerge,minutki,markets,getpath, start_year, start_month, start_day, start_hour, stop_year, stop_month, stop_day, stop_hour):

    fln = '_mnt.roman' if minutki else '.roman'
    dL = '\\' if system() == 'Windows' else '/'

    getpath = getpath +dL+ markets[0]
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

        if onlymerge:
            if len(podlist)==len(markets):
                listfiles2.append(podlist)
        else:
            listfiles2.append(podlist)
    return listfiles2


class Histwrite2:
	def __init__(self, path=None, market=None):
		self.path = path
		self.market = market
		self.hr = None
		self.a_cop = {}
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
				self.a_cop = self.a.copy()
				Thread(self.write_compress()).start()
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

	def write_compress(self):
		lz = lzma
		namefile=self.get_filename()
		namefileLZ =namefile+ '.roman'
		namefileJS=namefile+ '_mnt.roman'
		with lz.open(namefileLZ, "w") as f:
			f.write(lz.compress(json.dumps(self.a_cop).encode('utf-8')))
			print(self.market, "   ЗАПИСАНО   ", namefileLZ)

		# Вытаскиваем минутки from  a_cop
		mina={}
		for inst in self.a_cop:
			mina[inst]={}
			first_key=int(next(iter(self.a_cop[inst])))
			d = 60
			first_key=int(first_key / d) * d + d

			for i in range(first_key,3600,d):
				# mymin= str(int((self.mints+i)/60))
				mymin = str(int( i / 60))
				mina[inst][mymin]={}
				key=self.find_key(self.a_cop[inst], str(i))
				if key!=None:
					try:
						mina[inst][mymin]["a"]= self.a_cop[inst][key] ['asks'][0][0]
						mina[inst][mymin]["b"]= self.a_cop[inst][key] ['bids'][0][0]
					except:
						mina[inst][mymin]["a"] = self.a_cop[inst][key]['a']
						mina[inst][mymin]["b"] = self.a_cop[inst][key]['b']
				# else:
				# 	print(f" Nonekey in {inst}  {str(i)} ")

		with lz.open(namefileJS, "w") as f:
			f.write(lz.compress(json.dumps(mina).encode('utf-8')))
		print(self.market, "   ЗАПИСАНО   ", namefileJS)
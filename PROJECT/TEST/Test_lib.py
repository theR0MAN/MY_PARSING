
from platform import system
import os
import datetime
import time
import lzma as lz
import json



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





# 	класс распаковки и получения списка инстр
class Getl2:
	def __init__(self, content):
		self.content=content
		# self.output=[]  #список инструментов
	def gettm(self,z):
		'''получает путь , возвращает время в юникод'''
		x = z.split('\\')
		l = len(x)
		self.year = int(x[l - 4])
		self.mon = int(x[l - 3])
		self.day = int(x[l - 2])
		self.hr = int(x[l - 1].split('.')[0])
		tm = int(time.mktime(datetime.datetime(self.year, self.mon, self.day, self.hr).timetuple()))
		return tm  # ,year,mon,day,hr

	def getd(self):
		for cont in self.content:
			a = dict()
			for name in cont:
				with lz.open(name) as f:
					bb = dict(json.loads(lz.decompress(f.read()).decode('utf-8')))
				a |= bb
				yield [a,self.gettm(cont[0])]


	def get_l2(self):
		z = self.getd()
		L2 = dict()
		while True:
			cc = next(z)
			a = cc[0]
			self.output = list(a)
			starttime = cc[1]

			# обозначим списки инструментов
			for inst in a:
				if inst not in L2:
					if True:  # inst == 'Eu-12.23*FRTS'
						L2[inst] = dict()
						L2[inst]['asks'] = []
						L2[inst]['bids'] = []

			for ttm in range(3600):
				tmp = str(ttm)
				self.ttime=starttime + ttm
				for inst in a:
					if tmp in a[inst]:
						L2[inst]['asks'] = a[inst][tmp]['asks']
						L2[inst]['bids'] = a[inst][tmp]['bids']
				yield L2
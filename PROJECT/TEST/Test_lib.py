
from platform import system
import os
import datetime
import time
import lzma as lz
import json
from numpy import argsort


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
		self.timer=0
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
			print(cont, 'время предыдущего  расчета  ', time.time() - self.timer)
			# self.timer = time.time()
			for name in cont:
				with lz.open(name) as f:
					bb = dict(json.loads(lz.decompress(f.read()).decode('utf-8')))
				a |= bb
			# print( 'время распаковки ', time.time() - self.timer)
			self.timer=time.time()
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
				self.hoursec = ttm
				tmp = str(ttm)
				self.ttime=starttime + ttm
				for inst in a:
					if tmp in a[inst]:
						L2[inst]['asks'] = a[inst][tmp]['asks']
						L2[inst]['bids'] = a[inst][tmp]['bids']
				yield L2

# помойная функция, но пусть будет -использовать нужно ту что ниже
def getfut0(l):
	REZ=dict()
	for inst in l:
		if"-" in inst and '.' in inst:
			REZ[inst]=[]
			REZ[inst].append([])
			REZ[inst].append([])
			REZ[inst].append([])
	for inst0 in l:
		if"-" in inst0 and '.' in inst0:
			bodyit = inst0[:inst0.find('-')]
			x = inst0[inst0.find('-') + 1:inst0.find('*')].split(".")
			x2 = float(x[0]) + float(x[1]) * 12
			for inst in l:
				if "-" in inst and '.' in inst:
					bodyinst = inst[:inst.find('-')]
					xi = inst[inst.find('-') + 1:inst.find('*')].split(".")
					x2i = float(xi[0]) + float(xi[1]) * 12
					if bodyinst==bodyit and not x2==x2i:
						REZ[inst0][0].append(inst)
						if x2<x2i:
							REZ[inst0][1].append(inst)
						if x2>x2i:
							REZ[inst0][2].append(inst)
	return REZ
# словарь списков фьючей с более поздним и ранник сроком экспирации
# instr в список не входит -получать из ключа
# REZ[instr][0] - все
# REZ[instr][1] - более поздние
# REZ[instr][2]  -более ранние

#  сортирует словарь по значениям
def sortdict(dict) :
	keys = list(dict.keys())
	values = list(dict.values())
	sorted_value_index = argsort(values)
	return {keys[i]: values[i] for i in sorted_value_index}

# принимает список фьючей - возвращает
# список инструментов
# словарь для календарок в виде
# {'HOME': ['HOME-12.23*FRTS', 'HOME-3.24*FRTS'], 'MGNT': ['MGNT-12.23*FRTS', 'MGNT-3.24*FRTS', 'MGNT-6.24*FRTS'],
def get_fut(l):
	pred=dict()
	dinst=[]
	instset=set()
	for inst in l:
		if"-" in inst and '.' in inst:
			dinst.append(inst)
			bodyit = inst[:inst.find('-')]
			instset.add(bodyit)
	for i in instset:
		pred[i] = dict()
		for inst in l:
			if "-" in inst and '.' in inst:
				bodyit = inst[:inst.find('-')]
				xi = inst[inst.find('-') + 1:inst.find('*')].split(".")
				x2i = float(xi[0]) + float(xi[1]) * 12
				if i == bodyit:
					pred[i][inst]=x2i
	pred2=dict()
	for key in pred:
		pred2[key]=[]
		pred[key]= sortdict(pred[key])
	for key in pred2:
		for key2 in pred[key]:
			pred2[key].append(key2)

	# брать список с минимум 2 инструментами
	pred3=pred2.copy()
	for key in pred2:
		if len(pred2[key])==1:
			print(key,   '     ',len(pred2[key]))
			dinst.remove(pred3[key][0])
			del pred3[key]
	return (dinst,pred3)

def get_futforst(spisinstr):
	rez = dict()
	for inst in spisinstr:
		if "-" in inst and '.' in inst:
			bodyit = inst[:inst.find('-')]
			if bodyit in rez:
				rez[bodyit].append(inst)
			else:
				rez[bodyit] = []
				rez[bodyit].append(inst)
	return rez

# принимает список словарей, содержащий стаканы - возвращает кумулятивный стакан
def megamerge_stakan(spis):
	def mergestakan (asks1,bids1,asks2,bids2):
		def askmerge(a1,a2):
			rez = []
			la1 = len(a1)
			la2 = len(a2)
			cnt1 = 0
			cnt2 = 0
			fcnt1 = True
			fcnt2 = True
			while True:
				if cnt1==la1:
					fcnt1=False
				if cnt2==la2:
					fcnt2=False
				if not fcnt1 and not fcnt2 :
					break

				if  fcnt1 and fcnt2:
					if(a1[cnt1][0]<a2[cnt2][0]):
						rez.append(a1[cnt1])
						cnt1+=1
					elif (a1[cnt1][0] > a2[cnt2][0]):
						rez.append(a2[cnt2])
						cnt2 += 1
					else:
						rez.append([a1[cnt1][0],a1[cnt1][1]+a2[cnt2][1]])
						cnt1 += 1
						cnt2 += 1
				elif fcnt1:
					rez.append(a1[cnt1])
					cnt1 += 1
				elif fcnt2:
					rez.append(a2[cnt2])
					cnt2 += 1
			return rez

		def bidmerge(b1,b2):
			rez = []
			lb1 = len(b1)
			lb2 = len(b2)
			cnt1 = 0
			cnt2 = 0
			fcnt1 = True
			fcnt2 = True
			while True:
				if cnt1==lb1:
					fcnt1=False
				if cnt2==lb2:
					fcnt2=False

				if not fcnt1 and not fcnt2 :
					break

				if  fcnt1 and fcnt2:
					if(b1[cnt1][0]>b2[cnt2][0]):
						rez.append(b1[cnt1])
						cnt1+=1
					elif (b1[cnt1][0] < b2[cnt2][0]):
						rez.append(b2[cnt2])
						cnt2 += 1
					else:
						rez.append([b1[cnt1][0],b1[cnt1][1]+b2[cnt2][1]])
						cnt1 += 1
						cnt2 += 1
				elif fcnt1:
					rez.append(b1[cnt1])
					cnt1 += 1
				elif fcnt2:
					rez.append(b2[cnt2])
					cnt2 += 1
			return rez


		def funreb(asks, bids):
			while asks[0][0] <= bids[0][0]:
				minus = min(asks[0][1], bids[0][1])
				asks[0][1] = asks[0][1] - minus
				bids[0][1] = bids[0][1] - minus
				if asks[0][1] == 0:
					asks.pop(0)
				if bids[0][1] == 0:
					bids.pop(0)

				if len(asks) == 0 or len(bids) == 0:
					break
			return asks, bids
		return funreb (askmerge(asks1,asks2),bidmerge(bids1,bids2))

	startasks=[]
	startbids=[]
	for st in spis:
		asks=st['asks']
		bids=st['bids']
		startasks,startbids=mergestakan(startasks, startbids, asks, bids)
	rz=dict()
	rz['asks']=startasks
	rz['bids']=startbids
	return rz



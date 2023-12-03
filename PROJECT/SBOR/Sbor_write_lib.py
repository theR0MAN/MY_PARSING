import json
from platform import system
import time
import os
import lzma
import datetime



# _mnt.
def Compress(QE):
	def COMRESS0(namefile,data):
		lz = lzma
		with lz.open(namefile, "w") as f:
			print("   СТАРТ ЗАПИСИ  ", namefile)
			f.write(lz.compress(json.dumps(data).encode('utf-8')))
			print( "   ЗАПИСАНО   ", namefile)
	while True:
		if not QE.empty():
			print(" УРА - полный")
			COMRESS0(QE.get()[0],QE.get()[1])
		else:
			# print(" ПУСТОЙ")
			time.sleep(20)




class Histwrite2:
	def __init__(self, path, market,QE):
		self.timekeyminute0='0'
		self.path = path
		self.market = market
		self.hr = None
		self.a = {}
		self.ab = {}
		self.abm = {}

		self.a_izm = {}
		self.ab_izm = {}
		self.zapis = False
		self.zapisab = False
		self.QE=QE

	def putter(self, instr_name,askbid, dict_data):
		if askbid==[]:
			return
		instr_name += "*" + self.market
		dat = datetime.datetime.utcfromtimestamp(int(time.time()))
		hour = dat.hour
		timekey = str(dat.minute * 60 + dat.second)
		timekeyminute = str(dat.minute)
		if hour != self.hr:
			self.hr = hour
			if self.zapisab:
				self.write_compress('abt',self.ab)
				self.write_compress('abm',self.abm)
				self.abm = {}
				self.ab = {}
				self.ab_izm = {}
				self.zapisab = False

			if self.zapis:
				self.write_compress('stk',self.a)
				self.a = {}
				self.a_izm = {}
				self.zapis = False

		if not instr_name in self.ab:
			self.abm[instr_name] = {}
			self.ab[instr_name] = {}
			self.ab[instr_name][timekey] = askbid
			self.ab_izm[instr_name] = askbid
		if self.ab_izm[instr_name] != askbid:
			self.ab_izm[instr_name] = askbid
			self.ab[instr_name][timekey] = askbid
			self.zapisab = True
		if timekeyminute != self.timekeyminute0 and instr_name in self.ab_izm:
			self.timekeyminute0 = timekeyminute
			self.abm[instr_name][timekeyminute] = self.ab_izm[instr_name]

		if  dict_data!={}:
			if not instr_name in self.a:
				self.a[instr_name] = {}
				self.a[instr_name][timekey] = dict_data
				self.a_izm[instr_name] = dict_data
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

	def write_compress(self,c, data):
		self.QE.put((self.get_filename()+c+'.roman',data))

		# результат записи приме
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


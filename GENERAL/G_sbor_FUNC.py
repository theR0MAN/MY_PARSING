import json
from platform import system
# from multiprocessing import Process
from threading import Thread
import time
import os
import lzma
import datetime


class Histwrite:
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
		dat = datetime.datetime.utcfromtimestamp(
			int(time.time()) - 500)  # -открутим пару сек чтобы за час вперед не скочить
		year = dat.year
		month = dat.month
		day = dat.day
		hour = dat.hour

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
		return nextpath + dL + str(hour) + '.roman'

	def write_compress(self):
		lz = lzma
		with lz.open(self.get_filename(), "w") as f:
			f.write(lz.compress(json.dumps(self.a_cop).encode('utf-8')))
			print(self.market, "   ЗАПИСАНО   ", self.get_filename())


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
		dat = datetime.datetime.utcfromtimestamp(int(time.time()) - 500)  # -открутим пару сек
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
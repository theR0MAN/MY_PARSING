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
				Thread(self.wrie_compress()).start()
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

	def wrie_compress(self):
		lz = lzma
		with lz.open(self.get_filename(), "w") as f:
			f.write(lz.compress(json.dumps(self.a_cop).encode('utf-8')))
		print(self.a_cop)
		print(self.market, "   ЗАПИСАНО   ", self.get_filename())

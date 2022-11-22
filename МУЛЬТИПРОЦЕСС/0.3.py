import json
from platform import system
import multiprocessing
import time
import os
import lzma
import datetime


class Histwrite:
	def __init__(self):
		self.mas = []

	def perepars(self,x):
		self.mas.append(x*x)

	def putter(self, mas):
		with multiprocessing.Pool(4) as pool:
			pool.map_async(Histwrite.perepars, mas)
			pool.close()
			pool.join()
	def writer(self):
		print(self.mas)


c=[1,2,3,4,5,6]
Z= Histwrite()
Z.putter(c)



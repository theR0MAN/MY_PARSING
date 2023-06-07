

import plotly.express as px
from GENERAL.G_FUNC import get_color
from collections import deque


class Myinst:
	def __init__(self, inst=None, period_sred=None):
		self.period_sred = period_sred
		self.inst = inst
		self.asks = []
		self.bids = []
		self.sredn = []
		self.mediana = []
		self.supersredn = []
		self.supermediana = []

		self.asksrotkl = []
		self.bidsrotkl = []
		self.askmedotkl = []
		self.bidmedotkl = []

		self.nak = 0
		self.nakss = 0
		self.nakSO = 0
		self.nakMO = 0
		self.count = 0
		self.countss = 0
		self.countSO = 0
		self.countMO = 0
		self.countm = 0
		self.countsm = 0

		self.q = deque()
		self.qmo = deque()
		self.qsm = deque()

		self.count2 = 0

	def takedata(self, tm, data):
		Ask = data["asks"][0][0]
		Bid = data["bids"][0][0]
		# Ask=200
		# Bid=-200
		# Ask=50+self.count2
		# Bid=-50+self.count2
		# self.count2+=1
		self.asks.append(Ask)
		self.bids.append(Bid)
		SR = self.getsredn((Ask + Bid) / 2)
		self.sredn.append(SR)
		SS = self.getsupersredn(SR, (Ask + Bid) / 2)
		self.supersredn.append(SS)
		MD = self.getmediana((Ask + Bid) / 2)
		self.mediana.append(MD)
		SM = self.getsupermediana(MD, (Ask + Bid) / 2)
		self.supermediana.append(SM)

		SO = self.getSO(SR, Ask, Bid)
		MO = self.getMO(MD, Ask, Bid)

		SR = SS
		if SR == None or SO == None:
			self.asksrotkl.append(None)
			self.bidsrotkl.append(None)
		else:
			self.asksrotkl.append(SR + SO)
			self.bidsrotkl.append(SR - SO)

		MD = SS
		if MO == None or MD == None:
			self.askmedotkl.append(None)
			self.bidmedotkl.append(None)
		else:
			self.askmedotkl.append(MD + MO)
			self.bidmedotkl.append(MD - MO)

	def getsredn(self, data):
		if self.count < self.period_sred:
			self.nak += data
			self.count += 1
			return (None)
		else:
			self.nak = self.nak - self.nak / self.period_sred + data
			return (self.nak / self.period_sred)

	def getsupersredn(self, sr, kotir):  # kotir - (Ask+Bid)/2
		if sr == None:
			return (None)
		else:
			data = sr - kotir
			if self.countss < self.period_sred:
				self.nakss += data
				self.countss += 1
				return (None)
			else:
				self.nakss = self.nakss - self.nakss / self.period_sred + data
				return (sr - self.nakss / self.period_sred)

	def getSO(self, sr, Ask, Bid):
		if sr == None:
			return (None)
		else:
			data = max(abs(Ask - sr), abs(Bid - sr))
			if self.countSO < self.period_sred:
				self.nakSO += data
				self.countSO += 1
				return (None)
			else:
				self.nakSO = self.nakSO - self.nakSO / self.period_sred + data
				return (self.nakSO / self.period_sred)

	def getmediana(self, data):
		if self.countm < self.period_sred:
			self.q.append(data)
			self.countm += 1
			return (None)
		else:
			self.q.append(data)
			self.q.popleft()
			l = list(self.q)
			l.sort()
			ln = len(l)
			d = l[int(ln / 2)] if ln % 2 == 1 else (l[int(ln / 2)] + l[int(ln / 2) - 1]) / 2
			return (d)

	def getsupermediana(self, MD, kotir):  # kotir - (Ask+Bid)/2
		if MD == None:
			return (None)
		else:
			data = MD - kotir
			if self.countsm < self.period_sred:
				self.qsm.append(data)
				self.countsm += 1
				return (None)
			else:
				self.qsm.append(data)
				self.qsm.popleft()
				l = list(self.qsm)
				l.sort()
				ln = len(l)
				d = l[int(ln / 2)] if ln % 2 == 1 else (l[int(ln / 2)] + l[int(ln / 2) - 1]) / 2
				return (MD - d)

	def getMO(self, M, Ask, Bid):
		if M == None:
			return (None)
		else:
			data = max(abs(Ask - M), abs(Bid - M))
			if self.countMO < self.period_sred * 2:
				self.qmo.append(data)
				self.countMO += 1
				return (None)
			else:
				self.qmo.append(data)
				self.qmo.popleft()
				l = list(self.qmo)
				l.sort()
				ln = len(l)
				d = l[int(ln / 2)] if ln % 2 == 1 else (l[int(ln / 2)] + l[int(ln / 2) - 1]) / 2
				return (d)

	def chartdt(self):
		ix = list(range(0, len(self.asks)))
		color = get_color()
		fig = px.line()
		clr = color()
		fig.add_scatter(x=ix, y=self.asks, line_color=clr, name=' ask')
		fig.add_scatter(x=ix, y=self.bids, line_color=clr, name=' bid')
		# clr = color()
		# fig.add_scatter(x=ix, y=self.sredn, line_color=clr, name=' sredn')
		clr = color()
		fig.add_scatter(x=ix, y=self.supersredn, line_color=clr, name=' supersredn')
		#
		clr = color()
		# fig.add_scatter(x=ix, y=self.mediana, line_color=clr, name=' mediana')
		# clr = color()
		# fig.add_scatter(x=ix, y=self.supermediana, line_color=clr, name=' supermediana')

		clr = color()
		fig.add_scatter(x=ix, y=self.asksrotkl, line_color=clr, name=' asksrotkl')
		fig.add_scatter(x=ix, y=self.bidsrotkl, line_color=clr, name=' asksrotkl')
		#
		clr = color()
		fig.add_scatter(x=ix, y=self.askmedotkl, line_color=clr, name=' askmedotkl')
		fig.add_scatter(x=ix, y=self.bidmedotkl, line_color=clr, name=' bidmedotkl')

		fig.show()



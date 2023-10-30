from collections import deque

class Myheartbeat:
	def __init__(self,periodhertbeat,periodraschet,part,mnoz):
		# periodraschet через какой период перерасчитывать хертбиты- это для понижения нагрузки
		# part - 0,5 - медиана  1-самый хвост сортированных хартбитов
		# mnoz - уможение расчетного хартбита на коф для сравнения с текущим

		self.a = dict()
		self.b = dict()
		self.periodhertbeat=periodhertbeat
		self.periodraschet=periodraschet
		self.part=part
		self.mnoz=mnoz


	def get_heartbeats(self,dt,tme):
		for key in dt:
			if key not  in self.a:
				self.b[key]=False
				self.a[key] =dict()
				self.a[key]['asks'] =dt[key]['asks']
				self.a[key]['bids'] = dt[key]['bids']
				self.a[key]['lasttime'] = tme
				self.a[key]['kvotimestamps'] = 0
				self.a[key]['kvoraschet'] =0
				self.a[key]['heartbeat'] = deque()
				self.a[key]['medheartbeat'] = None
			if self.a[key] ['asks'] != dt[key] ['asks'] or self.a[key] ['bids'] != dt[key] ['bids'] :
				self.a[key]['asks'] = dt[key]['asks']
				self.a[key]['bids'] = dt[key]['bids']
				self.a[key]['timestamp'] = tme-self.a[key]['lasttime']
				self.a[key]['lasttime'] = tme
				if self.a[key]['kvotimestamps']< self.periodhertbeat:
					self.a[key]['heartbeat'].append(self.a[key]['timestamp'] )
					self.a[key]['kvotimestamps'] += 1
					self.a[key]['kvoraschet'] += 1
				else:
					self.a[key]['heartbeat'].append(self.a[key]['timestamp'])
					self.a[key]['heartbeat'] .popleft()
					self.a[key]['kvoraschet'] += 1
					if self.a[key]['kvoraschet']> self.periodraschet:
						self.a[key]['kvoraschet'] = 0
						l=list(self.a[key]['heartbeat'])
						l.sort()
						ln=int(self.periodhertbeat*self.part)
						self.a[key]['medheartbeat'] =l[ln]*self.mnoz
			if self.a[key]['medheartbeat']!=None:
				self.b[key] =tme - self.a[key]['lasttime'] < self.a[key]['medheartbeat']
		# False -инструмент спит
		return  self.b


class Mysredn:
	def __init__(self):
		self.baza=dict()


	def getsredn_exp(self,data,instrument,period):
		per = str(period)
		instrument=instrument+'exp'
		if instrument not in self.baza:
			self.baza[instrument]=dict()
			self.baza[instrument][per] = dict()
			self.baza[instrument][per]['nak']=0
			self.baza[instrument][per]['count'] = 0
		elif per not in self.baza[instrument]:
			self.baza[instrument][per] = dict()
			self.baza[instrument][per]['nak']=0
			self.baza[instrument][per]['count'] = 0
		if data==None:
			return (None)
		else:
			if self.baza[instrument][per]['count']<period:
				self.baza[instrument][per]['nak']+=data
				self.baza[instrument][per]['count']+=1
				return(None)
			else:
				self.baza[instrument][per]['nak']=self.baza[instrument][per]['nak']-self.baza[instrument][per]['nak']/period + data
				return (self.baza[instrument][per]['nak']/period)


	def getsredn_easy(self,data,instrument,period):
		per = str(period)
		instrument = instrument + 'easy'
		if instrument not in self.baza:
			self.baza[instrument]=dict()
			self.baza[instrument][per] = dict()
			self.baza[instrument][per]['nake']=0
			self.baza[instrument][per]['counte'] = 0
			self.baza[instrument][per]['qe'] = deque()
		elif per not in self.baza[instrument]:
			self.baza[instrument][per] = dict()
			self.baza[instrument][per]['nake']=0
			self.baza[instrument][per]['counte'] = 0
			self.baza[instrument][per]['qe'] = deque()
		if data==None:
			return (None)
		else:
			if self.baza[instrument][per]['counte'] < period:
				self.baza[instrument][per]['qe'].append(data)
				self.baza[instrument][per]['nake'] += data
				self.baza[instrument][per]['counte'] += 1
				return (None)
			else:
				self.baza[instrument][per]['qe'].append(data)
				last = self.baza[instrument][per]['qe'].popleft()
				self.baza[instrument][per]['nake'] = self.baza[instrument][per]['nake'] - last + data
				return (self.baza[instrument][per]['nake'] / period)

	def getmediana(self,data,instrument,period):
		per = str(period)
		instrument = instrument + 'med'
		if instrument not in self.baza:
			self.baza[instrument]=dict()
			self.baza[instrument][per] = dict()
			self.baza[instrument][per]['countm'] = 0
			self.baza[instrument][per]['qm'] = deque()
		elif per not in self.baza[instrument]:
			self.baza[instrument][per] = dict()
			self.baza[instrument][per]['countm'] = 0
			self.baza[instrument][per]['qm'] = deque()

		if data==None:
			return (None)
		else:
			if self.baza[instrument][per]['countm']<period:
				self.baza[instrument][per]['qm'].append(data)
				self.baza[instrument][per]['countm']+=1
				return(None)
			else:
				self.baza[instrument][per]['qm'].append(data)
				self.baza[instrument][per]['qm'].popleft()
				l=list(self.baza[instrument][per]['qm'])
				l.sort()
				ln=len(l)
				return(l[int(ln / 2)] if ln % 2 == 1 else (l[int(ln / 2)] + l[int(ln / 2) - 1]) / 2)


	def getshlifmed_exp(self,data,instrument,period):
		mediana = self.getmediana(data, instrument+ 'shlifexp', period)
		return(self.getsredn_exp(mediana, instrument + 'shlifexp', period))

	def getshlifmed_easy(self,data,instrument,period):
		mediana = self.getmediana(data, instrument+ 'shlifeasy', period)
		return(self.getsredn_easy(mediana, instrument + 'shlifeasy', period))



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





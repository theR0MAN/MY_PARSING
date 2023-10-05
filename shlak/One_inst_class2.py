import plotly.express as px
from GENERAL.G_FUNC import get_color
from collections import deque

class Myinst:
	def __init__(self, inst=None,period_sred =None):
		self.period_sred = period_sred
		self.inst = inst
		self.asks=[]
		self.bids = []
		self.sredn = []
		self.sredne = []
		self.mediana = []
		self.supersredn=[]
		self.supermediana = []

		self.asksrotkl=[]
		self.bidsrotkl=[]
		self.askmedotkl=[]
		self.bidmedotkl=[]
		
		self.nak=0
		self.nakss = 0
		self.nakSO = 0
		self.nakMO = 0
		self.count=0
		self.countss=0
		self.countSO = 0
		self.countMO = 0
		self.countm = 0
		self.countsm = 0

		self.q= deque()
		self.qe = deque()
		self.nake = 0
		self.counte = 0
		self.qmo = deque()
		self.qsm = deque()


		self.count2 = 0



	def takedata(self,data):
		Ask=data["asks"][0][0]
		Bid=data["bids"][0][0]
		# Ask=200
		# Bid=-200
		# Ask=50+self.count2
		# Bid=-50+self.count2
		# self.count2+=1
		self.asks.append(Ask)
		self.bids.append(Bid)
		SR=self.getsredn((Ask+Bid)/2)
		self.sredn.append(SR)

		SRe = self.geteasy((Ask + Bid) / 2)
		self.sredne.append(SRe)

		SS=self.getsupersredn(SR,(Ask+Bid)/2)
		self.supersredn.append(SS)
		MD=self.getmediana((Ask + Bid) / 2)
		self.mediana.append(MD)
		SM=self.getsupermediana(MD,(Ask+Bid)/2)
		self.supermediana.append(SM)
		
		SO=self.getSO(SR,Ask,Bid)
		MO=self.getMO(MD, Ask, Bid)


		if SR==None or SO==None :
			self.asksrotkl.append(None)
			self.bidsrotkl.append(None)
		else:
			self.asksrotkl.append(SR + SO)
			self.bidsrotkl.append(SR - SO)


		if MO==None  or MD==None  :
			self.askmedotkl.append(None)
			self.bidmedotkl.append(None)
		else:
			self.askmedotkl.append(MD + MO)
			self.bidmedotkl.append(MD - MO)





	def getsredn(self,data):
		if self.count<self.period_sred:
			self.nak+=data
			self.count+=1
			return(None)
		else:
			self.nak=self.nak-self.nak/self.period_sred + data
			return (self.nak/self.period_sred)



	def geteasy(self,data):
		if self.counte<self.period_sred:
			self.qe.append(data)
			self.nake += data
			self.counte+=1
			return(None)
		else:
			self.qe.append(data)
			last=self.qe.popleft()
			# print(last)
			# l = list(self.qe)
			self.nake = self.nake - last + data
			return (self.nake / self.period_sred)

	def getsupersredn(self,sr,kotir): # kotir - (Ask+Bid)/2
		if sr==None:
			return (None)
		else:
			data = sr - kotir
			if self.countss<self.period_sred:
				self.nakss+=data
				self.countss+=1
				return (None)
			else:
				self.nakss=self.nakss-self.nakss/self.period_sred + data
				return (sr-self.nakss/self.period_sred)


	def getSO(self,sr,Ask,Bid):
		if sr==None:
			return (None)
		else:
			data= max( abs(Ask-sr) , abs(Bid-sr))
			if self.countSO<self.period_sred:
				self.nakSO+=data
				self.countSO += 1
				return (None)
			else:
				self.nakSO=self.nakSO-self.nakSO/self.period_sred + data
				return (self.nakSO/self.period_sred)




	def getmediana(self,data):
		if self.countm<self.period_sred:
			self.q.append(data)
			self.countm+=1
			return(None)
		else:
			self.q.append(data)
			self.q.popleft()
			l=list(self.q)
			l.sort()
			ln=len(l)
			d = l[int(ln / 2)] if ln % 2 == 1 else (l[int(ln / 2)] + l[int(ln / 2) - 1]) / 2
			return(d)



	def getsupermediana(self,MD,kotir): # kotir - (Ask+Bid)/2
		if MD==None:
			return (None)
		else:
			data = MD - kotir
			if self.countsm<self.period_sred:
				self.qsm.append(data)
				self.countsm+=1
				return (None)
			else:
				self.qsm.append(data)
				self.qsm.popleft()
				l = list(self.qsm)
				l.sort()
				ln = len(l)
				d = l[int(ln / 2)] if ln % 2 == 1 else (l[int(ln / 2)] + l[int(ln / 2) - 1]) / 2
				return (MD -d)

	def getMO(self,M,Ask,Bid):
		if M==None:
			return (None)
		else:
			data= max( abs(Ask-M) , abs(Bid-M))
			if self.countMO < self.period_sred*2 :
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
		ix=list(range(0, len(self.asks)))
		color = get_color()
		fig = px.line()
		clr = color()
		fig.add_scatter(x=ix, y=self.asks, line_color=clr, name= ' ask')
		fig.add_scatter(x=ix, y=self.bids, line_color=clr, name= ' bid')
		clr = color()
		fig.add_scatter(x=ix, y=self.sredn, line_color=clr, name=' sredn')
		clr = color()
		fig.add_scatter(x=ix, y=self.sredne, line_color=clr, name=' sredne')
		# clr = color()
		# fig.add_scatter(x=ix, y=self.supersredn, line_color=clr, name=' supersredn')
		#
		clr = color()
		fig.add_scatter(x=ix, y=self.mediana, line_color=clr, name=' mediana')
		# clr = color()
		# fig.add_scatter(x=ix, y=self.supermediana, line_color=clr, name=' supermediana')

		# clr = color()
		# fig.add_scatter(x=ix, y=self.asksrotkl, line_color=clr, name=' asksrotkl')
		# fig.add_scatter(x=ix, y=self.bidsrotkl, line_color=clr, name=' asksrotkl')
		#
		# clr = color()
		# fig.add_scatter(x=ix, y=self.askmedotkl, line_color=clr, name=' askmedotkl')
		# fig.add_scatter(x=ix, y=self.bidmedotkl, line_color=clr, name=' bidmedotkl')

		fig.show()
 # Тезисы - мозг штурм асинхронный
# 		Самая флетовая средняя - это средняя , у которой показатель период/(СКО+комис) самый высокий
# волатильность средней равна СКО- идеальный тренд
# А что если ско брать не по модулю. чем ближе такой СКО к средней - тем флетовее средняя . Такое СКО- это есть суперсредняя, те первая производная от средней
# точнее, не СКО, а среднее отклонение СО
# но волу средней нужно выводить по любому
#  сравнить простое среднее с экспонетной в плане простое примерно равно экспонец. с периодом вдвое меньше
#  простое для производительности считать через очередь с корректировкой на новую и крайнюю
# простое медленнее, но не имеет долгой памяти - защита от случайноко выброса в истории (хотя если много выбросов- лучше медиана)
# если параметры волы средней и СО соответствуют флету, СО считать от суперсредней- - избавит от микротренда а ля контанго
# проверить всё на синусоиде с подмешиванием тренда, визуализировать сделки. Скорее всего, придется юзать суперсреднюю и её волу
# проверить гипотезу - предельный профитный параметр - когда СО по суперсредней касается средней. и вола суперсредней равна её ско.
# Вместо медианы можно использовать фильтр -ввести вспомогательну среднюю и игнорить тройное ско в расчете основной. будет бысрей при большом периоде.
# скорей всего, правильнее будет считать СО по минимумам ак-бид, а не по аск+бид/2  или максимумам  - проверить на аск/бид синусоиде
#  но это в спреде будет неадекватно- уменьшаться при росте волы в пределах спреда
#  или профитней - на искусственной синусоиде, в рынке -лучше (аск+бид)/2
#  вывести СО, являющиеся минимумумом профитности при данной воле средней... так. индикативно - не обязательно

#  Матожидание регулировать задаваемым запасом по издержками с множителем или задаваемыми абсолютна -т.е с форой - это минимум СО
# вхлд в позицию кода цена превышает фору и когда СО превышает фору,лучше когда (фора-СО)/2 больше форы и вход по (фора-СО)/2
#  а может, к СО добавить (лучше отнять (чтобы ушла ниже форы)) волатильность средней и уже тогда входить  по (фора-СО)/2?  -решит проблему торга внутри спреда
#  да уж. если среднее отклонение от суперсредней  совпадает со средним отклонением от средней - тогда ОК но при кекоторыз условиях выше
# проверить совпадение отклонений при резком пересечении при смене тренда - если не совпадает, тогда ок, иначе придется юзать волу средней

# вола по инструменту нужна - входить если ведущие пробили, если нет - не входить

# несколько окон с графиками https://stackru.com/questions/58638228/spyder-plotly-neskolko-grafikov-v-odnom-okne-brauzera
# https://plotly.com/python/subplots/
# https://habr.com/ru/articles/502958/
# https://plotly.com/python/marker-style/
# https://qwertybox.ru/articles/39244/

# https://digitrain.ru/articles/218557/
# https://www.youtube.com/watch?v=mvVt-raJIpo
# from plotly.subplots import make_subplots
# https://dash.gallery/Portal/
# import plotly.graph_objects as go
#
# fig = make_subplots(rows=3, cols=2)
#
# fig.add_trace(go.Scatter( x=[3, 4, 5],     y=[1000, 1100, 1200],), row=1, col=1)
#
# fig.add_trace(go.Scatter(  x=[2, 3, 4], y=[100, 110, 120],), row=2, col=2)
#
# fig.add_trace(go.Scatter( x=[0, 1, 2], y=[10, 11, 12]), row=3, col=1)

# fig.update_layout(height=1000, width=1000, title_text="Stacked Subplots")
# fig.update_layout(height=1000, width=1000, title_text="Stacked Subplots")
# fig.show()

# Тестирование - смотреть что будет когда возьмут в стакане объем, который ты бы взял.  Так получится избежать отсутствие влияние на цену при тесте.
# для изи стратегий - изменчивость размера спреда считать и сравнивать с издержками  издержки-шаг зигзага

# функция , которая выдает из истории котировку инструмента - аналаг как в   реале
# сперва в словарь пишем инструмент-котировка , а ужев следующем операторе цикле тестировщик изсловаря берет данные
#  т.е они идут один за одним . не эффективно, но удобно
# использовать try ключ , ане "if  key in dict" дабы избежать итераций поиска
#     сделки пишутся в фпйл (), на основании этого идет обработчик и визуализатор
# сопоставить фильтры - двойная медиана против двойной средней против одиночной медианы , отпалированной средней . простой средней

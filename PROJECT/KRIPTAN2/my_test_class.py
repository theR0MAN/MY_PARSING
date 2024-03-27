class Testtrade():
	def __init__(self):
		self.pos = dict()

	def trade(self, sym, type, price,comis, dolya):
		'''
		:param sym:
		:param type: 'buy' 'sell' or 'close' -закрытие текущей позиции
		:param price: цена входа в позицию
		:param comis: комиссии %
		:param dolya: доля капитала на символ
		:return:
		'''
		rz=0
		if sym not in self.pos:
			self.pos[sym] = dict()
			self.pos[sym]['type'] = type
			self.pos[sym]['price'] = price
			self.pos[sym]['dolya'] = dolya
			self.pos[sym]['rez'] = 0
			self.pos[sym]['comis'] = dolya * comis
			print(f' START {sym}   {type} {price}  ')

		else:
			if type == 'sell':  # если запрос на продажу
				# print(f" before mistake self.pos[sym]= {self.pos[sym]}  type={type}")
				if self.pos[sym]['type'] == 'buy':  # если предыдущая - покупка
					rz=self.pos[sym]['dolya'] * 100 * (price - self.pos[sym]['price']) / self.pos[sym]['price']
					print(f' {sym}   {type} {price}  rez= {rz}')
					self.pos[sym]['rez'] += rz
					self.pos[sym]['comis']+=dolya*comis*2
					self.pos[sym]['type'] = 'sell'
					self.pos[sym]['price'] = price
					self.pos[sym]['dolya'] = dolya
			# if self.pos[sym][type] == 'buy'  and NONE  - игнорится автоматом

			elif type == 'buy':  # запрос  покупка
				if self.pos[sym]['type'] == 'sell':  # предыдущая  на продажу
					rz=self.pos[sym]['dolya'] * 100 * (self.pos[sym]['price'] - price) / self.pos[sym]['price']
					print(f' {sym}   {type} {price}  rez= {rz}')
					self.pos[sym]['rez'] += rz
					self.pos[sym]['comis'] += dolya * comis*2
					self.pos[sym]['type'] = 'buy'
					self.pos[sym]['price'] = price
					self.pos[sym]['dolya'] = dolya

			elif type == 'close':
				if self.pos[sym]['type'] == 'sell':
					rz = self.pos[sym]['dolya'] * 100 * (price - self.pos[sym]['price']) / self.pos[sym]['price']
					print(f' {sym}   {type} {price}  rez= {rz}')
					self.pos[sym]['rez'] += rz
					self.pos[sym]['comis'] += dolya * comis*2

					self.pos[sym]['type'] = 'close'
					self.pos[sym]['price'] = price
					self.pos[sym]['dolya'] = dolya

				elif self.pos[sym]['type'] == 'buy':
					rz = self.pos[sym]['dolya'] * 100 * (self.pos[sym]['price'] - price) / self.pos[sym]['price']
					print(f' {sym}   {type} {price}  rez= {rz}')
					self.pos[sym]['rez'] += rz
					self.pos[sym]['comis'] += dolya * comis*2

					self.pos[sym]['type'] = 'close'
					self.pos[sym]['price'] = price
					self.pos[sym]['dolya'] = dolya



	def getequity(self,symspis):
		'''
		 формирует эквити на основе списка инструментов по результатам словаря pos
		:param symspis:  [symbol,ask,bid]   - аск бид -текущие
		:return: эквити,comis,гарузка депозита (без реинвеста)
		'''
		eq=0
		comis=0
		zag=0
		for spis in symspis:
			sym =spis[0]
			Ask=spis[1]
			Bid=spis[2]
			if Ask!=None and Bid!= None and sym in self.pos:
				#  не так как выше, ибо тут поза текущая
				comis+=self.pos[sym]['comis']
				if self.pos[sym]['type'] == 'sell':
					zag+= self.pos[sym]['dolya']
					eq+=self.pos[sym]['rez']+ self.pos[sym]['dolya'] * 100 * (self.pos[sym]['price'] - Ask) / self.pos[sym]['price']
				elif self.pos[sym]['type'] == 'buy':
					zag += self.pos[sym]['dolya']
					eq+= self.pos[sym]['rez']+ self.pos[sym]['dolya'] * 100 * (Bid - self.pos[sym]['price']) / self.pos[sym]['price']
				elif self.pos[sym]['type'] == 'close':
					eq += self.pos[sym]['rez']


		return eq,comis ,zag






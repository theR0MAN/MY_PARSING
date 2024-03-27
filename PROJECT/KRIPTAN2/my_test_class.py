class Testtrade():
	def __init__(self):
		self.pos = dict()

	def trade(self, sym, type, price, dolya):
		'''
		:param sym:
		:param type: 'buy' 'sell' or None -закрытие текущей позиции
		:param price: цена входа в позицию
		:param proc: доля капитала на символ
		:return:
		'''
		rz=0
		if sym not in self.pos:
			self.pos[sym] = dict()
			self.pos[sym]['type'] = type
			self.pos[sym]['price'] = price
			self.pos[sym]['dolya'] = dolya
			self.pos[sym]['rez'] = 0

		else:
			if type == 'sell':  # если запрос на продажу
				if self.pos[sym][type] == 'buy':  # если предыдущая - покупка
					rz=self.pos[sym]['dolya'] * 100 * (price - self.pos[sym]['price']) / self.pos[sym]['price']
					self.pos[sym]['rez'] += rz
				self.pos[sym][type] = 'sell'
				self.pos[sym]['price'] = price
				self.pos[sym]['dolya'] = dolya
			# if self.pos[sym][type] == 'buy'  and NONE  - игнорится автоматом

			elif type == 'buy':  # запрос  покупка
				if self.pos[sym][type] == 'sell':  # предыдущая  на продажу
					rz=self.pos[sym]['dolya'] * 100 * (self.pos[sym]['price'] - price) / self.pos[sym]['price']
					self.pos[sym]['rez'] += rz
				self.pos[sym][type] = 'buy'
				self.pos[sym]['price'] = price
				self.pos[sym]['dolya'] = dolya

			elif type == None:
				if self.pos[sym][type] == 'sell':
					rz = self.pos[sym]['dolya'] * 100 * (price - self.pos[sym]['price']) / self.pos[sym]['price']
					self.pos[sym]['rez'] += rz
				elif self.pos[sym][type] == 'buy':
					rz = self.pos[sym]['dolya'] * 100 * (self.pos[sym]['price'] - price) / self.pos[sym]['price']
					self.pos[sym]['rez'] += rz
				self.pos[sym][type] = None
				self.pos[sym]['price'] = price
				self.pos[sym]['dolya'] = dolya

			print(f' {sym}   {type} {price}  rez= {rz}')

	def getequity(self,symspis):
		'''
		 формирует эквити на основе списка инструментов по результатам словаря pos
		:param symspis:  [symbol,ask,bid]   - аск бид -текущие
		:return: эквити,гарузка депозита (без реинвеста)
		'''
		eq=0
		zag=0
		for spis in symspis:
			sym =spis[0]
			Ask=spis[1]
			Bid=spis[2]
			if sym in self.pos:
				#  не так как выше, ибо тут поза текущая
				if self.pos[sym][type] == 'sell':
					zag+= self.pos[sym]['dolya']
					eq+=self.pos[sym]['rez']+ self.pos[sym]['dolya'] * 100 * (self.pos[sym]['price'] - Ask) / self.pos[sym]['price']
				elif self.pos[sym][type] == 'buy':
					zag += self.pos[sym]['dolya']
					eq+= self.pos[sym]['rez']+ self.pos[sym]['dolya'] * 100 * (Bid - self.pos[sym]['price']) / self.pos[sym]['price']
				elif self.pos[sym][type] == None:
					eq += self.pos[sym]['rez']


		return eq ,zag






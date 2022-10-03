class Employee:
	def __init__(self,name,salary,bonus):
		self.name=name
		self.salary=salary
		self.bonus=bonus

	def calculae_total_bonus(self):
		return self.salary/100*self.bonus

	def __str__(self):
		return f'{self.__class__.__name__}  {self.name}, salary={self.salary}, bonus= {self.bonus}%,'\
			   f'total bonus = {self.calculae_total_bonus()} rub'


class Cleaner(Employee):
	def __init__(self,name):
		super().__init__(name,1500,1)
		print(self.salary)

print(Cleaner('vasya') )


class CEO(Employee):
	def __init__(self,name):
		super().__init__(name,1100,1)
		print(self.salary)

	def calculae_total_bonus(self):
		return 200000

print(CEO('Dima') )




#######################################

class Mylist(list):
	def __str__(self):
		return super().__str__().replace(',',',\n')


my_list=Mylist([1,2,3])
print(my_list)
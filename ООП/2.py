class Person:
	def __init__(self,first_name,last_name,age):
		self._first_name = first_name
		self._last_name = last_name
		self.__age = age

	def set_age(self,age):
		if age<1 or age>120:
			raise  ValueError ('age must be in range 1-120')
		self.__age=age

	def describe(self):
		print(f' i am {self._first_name}  {self._last_name} i am {self.__age} years old')


ivan = Person('Ivan', 'Ivanov', 300)
ivan.age=1000
ivan.describe()

ivan._age=1000
ivan.describe()

# ivan.set_age(0)
print(dir(ivan))



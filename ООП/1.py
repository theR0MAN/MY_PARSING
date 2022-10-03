class Cat:

	def __init__(self,name,age):
		self.name=name
		self.age=age



	def meow(self):

		print(f' {self.name} says meu')


if __name__ == '__main__':
	tom = Cat('tom',2)
	angella= Cat('angella',1)

	print(tom)
	print(angella)
	tom.meow()
	angella.meow()

	print(tom.name)
	print(tom.age)


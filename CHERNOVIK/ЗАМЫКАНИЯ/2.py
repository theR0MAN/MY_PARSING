def create_counter():
	i = 0
	def func():
		nonlocal i
		i += 1
		return i
	return func

counter = create_counter()
print(counter())  # 1
print(counter())  # 2
print(counter())  # 3
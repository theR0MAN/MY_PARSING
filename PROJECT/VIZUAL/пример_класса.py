class Team:

	def __init__(self, rating):
		"Initialize team with rating"
		self.rating = rating


a= {'q':6,'e':9,'y':11,'t':60,'qp':11}
b=dict()
for key in a:
	b[key]=Team(a[key])

for key in a:
	print(b[key].rating)
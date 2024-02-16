from collections import  deque
import itertools
# persr = 2000 # период средней
# kperso = 3 # период СКО = persr *kperso
# ksovh = 1
# # ksovih = 1

# sym1='SiM4*FRTS2'
# sym2='USD000UTSTOM*CUR'
# identifikator=sym1+'@'+sym2+'@'+str(persr)+'@' +str(kperso )+'@'+str(ksovh)
# print(identifikator)

#
# colors = ['red', 'green', 'blue']
# sizes = ['S', 'M', 'L']
# for color, size in itertools.product(colors, sizes):
# 	print(color, size)


# persrs = [500,1000,2000,4000,8000,16000]
# kpersos = [1,2,4] # период СКО = persr *kperso
# ksovhs = 1,1.3,1.7,2
#
# sym1='SiM4*FRTS2'
# sym2='USD000UTSTOM*CUR'
# for persr,kperso,ksovh in itertools.product(persrs, kpersos,ksovhs ):
# 	identifikator = sym1 + '@' + sym2 + '@' + str(persr) + '@' + str(kperso) + '@' + str(ksovh)
# 	print(identifikator)

dats0 = {'Si': ['SiM4*FRTS2', 'USD000UTSTOM*CUR', 'SiU4*FRTS2']}
dats = ['SiM4*FRTS2', 'USD000UTSTOM*CUR', 'SiU4*FRTS2']

# countd=0
# for i in dats:
# 	countd+=1
# 	for j in dats[countd:]:
# 		print(i,j)



persrs = [500]
kpersos = [1,2] # период СКО = persr *kperso
ksovhs = [1,1.3]

#
onetwomas=[]
countd=0
for i in dats0['Si']:
	countd+=1
	for j in dats0['Si'][countd:]:
		onetwomas.append([i,j])
for onetwo,persr,kperso,ksovh in itertools.product(onetwomas,persrs, kpersos,ksovhs ):
	sym1 = onetwo[0]
	sym2 = onetwo[1]
	identifikator = sym1 + '@' + sym2+ '@' + str(persr) + '@' + str(kperso) + '@' + str(ksovh)

	print(identifikator)

for onetwo in onetwomas:
	sym1 = onetwo[0]
	sym2 = onetwo[1]
	print(sym1,sym2)



from numba import njit
import time
# st1=dict()
# st2=dict()
# st3=dict()
# st4=dict()
# st5=dict()
#
# st1['asks']=[[13,2],[14,2],[15,2],[16,2],[17,2],[18,2],[19,2],[20,2],[21,2],[22,2],[23,2],[24,2],[25,2]]
# st1['bids']=[[11,2],[10,2],[9,2],[8,2],[7,2]]
#
# st2['asks']=[[9,3],[10,3],[11,3],[12,3],[13,3],[14,2],[15,2],[16,2],[17,2],[18,2],[19,2],[20,2],[21,2],[22,2],[23,2],[24,2],[25,2]]
# st2['bids']=[[7,3],[6,3],[5,3],[4,3],[3,3]]
#
# st3['asks']=[[9,1],[10,1],[11,1],[12,3],[13,1]]
# st3['bids']=[[7,1],[6,1],[5,3],[4,1],[3,1]]
#
#
#




# та же функция но с отсечкой - противоположный банд продавливается на  объем входа, расширяя спред
def punchvolS2(stk,rs,vol0,comis,fora,kspreads):
	# comis - комис в проц
	# fora - фора к комис
	# kspreads- к-во спредов
	Ask0=stk['asks'][0][0]
	Bid0= stk['bids'][0][0]
	spread0=100*(Ask0-Bid0)/Ask0

	vol=vol0
	masva = []
	sumvol=0
	sumproizv=0
	vzcen=0
	count=0
	mas = stk['bids'].copy()
	cen = Bid0
	ln=len(stk['asks'])
	for i in stk['asks']:
		if vol>= i[1]:
			vol -= i[1]

			if rs:
				vvl = i[1]
				while vvl > 0:
					if mas == []:
						break
					elif vvl > mas[0][1]:
						vvl -= mas[0][1]
						cen = mas[0][0]
						mas.pop(0)
					elif vvl < mas[0][1]:
						mas[0][1] -= vvl
						vvl = 0
					elif vvl == mas[0][1]:
						vvl = 0
						cen = mas[0][0]
						mas.pop(0)
				spread = 100 * (Ask0 - cen) / Ask0
				print('spread2=', spread)
			else:
				spread =spread0

			sumproizv+=i[1]*i[0]
			sumvol+= i[1]
			if count<ln-1:
				count += 1
				vzcen= sumproizv/sumvol
				endcen=stk['asks'][count][0]
				procprofit=100*(endcen-vzcen)/vzcen-comis-fora-spread*kspreads
				totalprofit=(100*(endcen-vzcen)/vzcen-comis-fora-spread*kspreads)*sumvol
				masva.append([sumvol,vzcen,endcen,procprofit,totalprofit])
			else:
				break
		else:
			break

	masvb = []
	vol = vol0
	sumvol=0
	sumproizv=0
	vzcen=0
	count=0
	mas = stk['asks'].copy()
	cen = Ask0
	ln=len(stk['bids'])
	for i in stk['bids']:
		if vol>= i[1]:
			vol -= i[1]
			if rs:
				vvl=i[1]
				while vvl > 0:
					if mas == []:
						break
					elif vvl > mas[0][1]:
						vvl -= mas[0][1]
						cen = mas[0][0]
						mas.pop(0)
					elif vvl < mas[0][1]:
						mas[0][1] -= vvl
						vvl = 0
					elif vvl == mas[0][1]:
						vvl = 0
						cen = mas[0][0]
						mas.pop(0)
				spread = 100 * (cen - Bid0) / cen
				print('spread1=',spread)
			else:
				spread =spread0
			sumproizv+=i[1]*i[0]
			sumvol+= i[1]
			if count<ln-1:
				count += 1
				vzcen= sumproizv/sumvol
				endcen=stk['bids'][count][0]
				procprofit=100*(vzcen-endcen)/vzcen-comis-fora-spread*kspreads
				totalprofit=(100*(vzcen-endcen)/vzcen-comis-fora-spread*kspreads)*sumvol
				masvb.append([sumvol,vzcen,endcen,procprofit,totalprofit])
			else:
				break
		else:
			break

	maxbuy=[]
	profit=-99999999999999
	for i in masva:
		if i[4]>profit:
			profit=i[4]
			maxbuy=i
	maxsell=[]
	profit=-99999999999999
	for i in masvb:
		if i[4]>profit:
			profit=i[4]
			maxsell=i

	print(masva)
	print(masvb)
	print(maxbuy)
	print(maxsell)
	return maxbuy,maxsell




st4=dict()
st4['asks']=[[90,5],[100,8],[110,2],[120,30],[130,11]]
st4['bids']=[[70,8],[60,2],[50,30],[40,10],[30,10]]

punchvolS2(st4,True,50,0.01,0.01,1)






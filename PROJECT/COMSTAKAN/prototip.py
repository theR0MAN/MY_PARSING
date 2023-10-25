from numba import njit
import time
st1=dict()
st2=dict()
st3=dict()
st4=dict()

st1['asks']=[[13,2],[14,2],[15,2],[16,2],[17,2],[18,2],[19,2],[20,2],[21,2],[22,2],[23,2],[24,2],[25,2]]
st1['bids']=[[11,2],[10,2],[9,2],[8,2],[7,2]]

st2['asks']=[[9,3],[10,3],[11,3],[12,3],[13,3],[14,2],[15,2],[16,2],[17,2],[18,2],[19,2],[20,2],[21,2],[22,2],[23,2],[24,2],[25,2]]
st2['bids']=[[7,3],[6,3],[5,3],[4,3],[3,3]]

st3['asks']=[[9,1],[10,1],[11,1],[12,3],[13,1]]
st3['bids']=[[7,1],[6,1],[5,3],[4,1],[3,1]]

st4['asks']=[[90,10],[100,10],[110,10],[120,30],[130,10]]
st4['bids']=[[70,10],[60,10],[50,30],[40,10],[30,10]]




def megamerge_stakan(spis):
	def mergestakan (asks1,bids1,asks2,bids2):
		def askmerge(a1,a2):
			rez = []
			la1 = len(a1)
			la2 = len(a2)
			cnt1 = 0
			cnt2 = 0
			fcnt1 = True
			fcnt2 = True
			while True:
				if cnt1==la1:
					fcnt1=False
				if cnt2==la2:
					fcnt2=False
				if not fcnt1 and not fcnt2 :
					break

				if  fcnt1 and fcnt2:
					if(a1[cnt1][0]<a2[cnt2][0]):
						rez.append(a1[cnt1])
						cnt1+=1
					elif (a1[cnt1][0] > a2[cnt2][0]):
						rez.append(a2[cnt2])
						cnt2 += 1
					else:
						rez.append([a1[cnt1][0],a1[cnt1][1]+a2[cnt2][1]])
						cnt1 += 1
						cnt2 += 1
				elif fcnt1:
					rez.append(a1[cnt1])
					cnt1 += 1
				elif fcnt2:
					rez.append(a2[cnt2])
					cnt2 += 1
			return rez

		def bidmerge(b1,b2):
			rez = []
			lb1 = len(b1)
			lb2 = len(b2)
			cnt1 = 0
			cnt2 = 0
			fcnt1 = True
			fcnt2 = True
			while True:
				if cnt1==lb1:
					fcnt1=False
				if cnt2==lb2:
					fcnt2=False

				if not fcnt1 and not fcnt2 :
					break

				if  fcnt1 and fcnt2:
					if(b1[cnt1][0]>b2[cnt2][0]):
						rez.append(b1[cnt1])
						cnt1+=1
					elif (b1[cnt1][0] < b2[cnt2][0]):
						rez.append(b2[cnt2])
						cnt2 += 1
					else:
						rez.append([b1[cnt1][0],b1[cnt1][1]+b2[cnt2][1]])
						cnt1 += 1
						cnt2 += 1
				elif fcnt1:
					rez.append(b1[cnt1])
					cnt1 += 1
				elif fcnt2:
					rez.append(b2[cnt2])
					cnt2 += 1
			return rez


		def funreb(asks, bids):
			while asks[0][0] <= bids[0][0]:
				minus = min(asks[0][1], bids[0][1])
				asks[0][1] = asks[0][1] - minus
				bids[0][1] = bids[0][1] - minus
				if asks[0][1] == 0:
					asks.pop(0)
				if bids[0][1] == 0:
					bids.pop(0)

				if len(asks) == 0 or len(bids) == 0:
					break
			return asks, bids
		return funreb (askmerge(asks1,asks2),bidmerge(bids1,bids2))

	startasks=[]
	startbids=[]
	for st in spis:
		asks=st['asks']
		bids=st['bids']
		startasks,startbids=mergestakan(startasks, startbids, asks, bids)
	rz=dict()
	rz['asks']=startasks
	rz['bids']=startbids
	return rz

timer=time.time()

for i in range (20000):
	megamerge_stakan([st1, st2, st3, st4])
print(time.time()-timer)

print(megamerge_stakan([st1,st2,st3]))
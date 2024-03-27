from PROJECT.TEST.Test_lib import *
from PROJECT.VIZUAL.Viz_lib import get_color
from PROJECT.SCIENTIC.sc_sredn_lib import *
from platform import system
import plotly.express as px
from collections import deque
import datetime, time  # timer=time.time()
import traceback
import statistics
import pandas as pd
from PROJECT.SBOR.my_lib import *
# from IPython.display import display

zadpol=3
zadtmsmp=2

pth='G:\\NEWKRIPT'

# markets = os.listdir(pth)
markets = ['binance&swap', ]  #'poloniex',24 1  7-10
print(markets)

# markets = ['FRTS2']  # ,'MOEX'
instdict = dict()

minutki = 123
onlymerge = 0

hardsync=False
# hardsync True - жесткая синхронизация, когда все инструменты одновременно вписываются в задержки
# hardsync False - просто когда присутствуют все инструменры
start_year, start_month, start_day, start_hour = 2024, 3, 20, 15
stop_year, stop_month, stop_day, stop_hour = 2024, 3, 20, 16

content = getdata_merge(onlymerge, minutki, markets, pth, start_year, start_month, start_day, start_hour, stop_year,
						stop_month, stop_day, stop_hour)
print(content)

if content==[]:
	print(' нет данных за этот период' )
	quit()

exem = Getl2(content, 200, 0.95, 10)
# scie = Mysredn()
z = exem.get_l2NEW()  # получает словарь котиров
day0 = -1
count = 0
ct = 0

razrez = 0
countrr = 0

obryv = dict()
paintdict = {}
# подготовка словаря отрисовки
ixes = []


first=False
instset=set()

data = next(z)
# готовим итоговый массив
rezdict = dict()
cordat = dict()
for sym in data:
	cordat[sym]=[]
	rezdict[sym] = dict()
	rezdict[sym]['asks'] = []
	rezdict[sym]['bids'] = []
kcnt=0

easy=False


print(' START WHILE')
while True:

	try:
		# timer=time.time()
		data = next(z)  # это якобы на серваке - к нему нужен доступ


		timestamps=[]
		medtmamp =0
		for inst in data:
			if data[inst]['dat'] != None:
				tmst=data[inst]['dat']['timestamp']
				timestamps.append(tmst)
		if timestamps!=[]:
			medtmamp=statistics.median(timestamps)



		wrt=True
		if  not easy:
			if hardsync:
				for inst in data:
					if data [inst]['dat'] != None:
						if not (data [inst]['tmstp'][1]<zadpol and medtmamp-data [inst]['dat']['timestamp']<zadtmsmp):
							wrt = False
					else:
						wrt= False
			else:
				for inst in data:
					if data [inst]['dat'] == None:
						wrt = False


		if wrt:
			if not hardsync: # чтобы избежать лишних итераций далее
				easy=True

			for inst in data:
				rezdict[inst]['asks'].append(data[inst]['dat']['asks'][0])
				rezdict[inst]['bids'].append(data[inst]['dat']['bids'][0])
				cordat[inst].append((data[inst]['dat']['asks'][0]+data[inst]['dat']['bids'][0])/2)


			ixes.append(count)
			count += 1

	except Exception:
		print(traceback.format_exc())
		print('error')
		# quit()
		break

print('нормализация словаря')


for  inst in rezdict :
	sm=0
	cnt=0
	ind=-1
	for ask in rezdict  [inst]['asks']:
		ind+=1
		if ask != None :
			bid=rezdict  [inst]['bids'][ind]
			sm+=(ask+bid)/2
			cnt+=1
	if cnt !=0:
		sredn =sm/cnt
		ind = -1
		for ask in rezdict  [inst]['asks']:
			ind += 1
			if ask != None:
				rezdict  [inst]['bids'][ind]=100*rezdict  [inst]['bids'][ind]/ sredn
				rezdict  [inst]['asks'][ind] = 100 * rezdict  [inst]['asks'][ind] / sredn
				cordat[inst][ind]=((rezdict[inst]['bids'][ind] + rezdict[inst]['asks'][ind])/2)


print('распилим на снапшоты')
ixes2=[]
cordat2=dict()

firstkey= next(iter(cordat))
ln=len(cordat[firstkey])

for inst in cordat:
	cordat2[inst]=cordat[inst][0:ln:2]

firstkey= next(iter(cordat2))
ln=len(cordat2[firstkey])
for i in range(ln):
	ixes2.append(i)


timer=time.time()
kolonki=list(cordat2)
# print(kolonki)
df = pd.DataFrame(cordat2, columns=kolonki)
z= df.corr()
a=z.to_dict()
skorost = time.time()-timer
# quit()
# z.to_csv("output.csv",sep=';', index=False)
for key in a:
	print(key,mysortdict(a[key]))
print('skorost расчета корреляций= ',skorost)


#
# color = get_color()
# fig = px.line(title=' без резки - аск/бид')
# for  inst in rezdict:
# 	clr = color()
# 	fig.add_scatter(x=ixes, y=rezdict [inst]['asks'], line_color=clr, name= inst + ' ask')
# 	fig.add_scatter(x=ixes, y=rezdict[inst]['bids'], line_color=clr, name= inst+ ' bid')
# fig.show()

# color = get_color()
# fig = px.line(title='графип по которому строилась матрица кореляцй без резки ')
# for  inst in cordat:
# 	clr = color()
# 	fig.add_scatter(x=ixes, y=cordat [inst], line_color=clr, name= inst + ' ask')
# fig.show()
#

color = get_color()
fig = px.line(title='графип по которому строилась матрица кореляцй с резкой ')
for  inst in cordat2:
	clr = color()
	fig.add_scatter(x=ixes2, y=cordat2 [inst], line_color=clr, name= inst + ' ask')
fig.show()
# WIF/USDT:USDT*binance&swap {'WIF/USDT:USDT*binance&swap': 1.0, 'PYTH/USDT:USDT*binance&swap': 0.9471562493640133, 'GRT/USDT:USDT*binance&swap': 0.9462015844484409, 'BCH/USDT:USDT*binance&swap': 0.9450480929930042, 'AVAX/USDT:USDT*binance&swap': 0.9411180450840052, '1INCH/USDT:USDT*binance&swap': 0.9362276445944748, 'SOL/USDT:USDT*binance&swap': 0.9352326973477914, 'JUP/USDT:USDT*binance&swap': 0.933563466742379, 'WLD/USDT:USDT*binance&swap': 0.9307119685492636, 'BTC/USDT:USDT*binance&swap': 0.9268566104538982, 'CVX/USDT:USDT*binance&swap': 0.9257672726172226, 'ORDI/USDT:USDT*binance&swap': 0.9249428370040778, 'EOS/USDT:USDT*binance&swap': 0.9227755072580339, 'IMX/USDT:USDT*binance&swap': 0.9227044835464978, 'NEAR/USDT:USDT*binance&swap': 0.9208739539032206, 'MASK/USDT:USDT*binance&swap': 0.9206780318547676, 'UNI/USDT:USDT*binance&swap': 0.9200410198252411, 'ACH/USDT:USDT*binance&swap': 0.9173022342338876, 'ETC/USDT:USDT*binance&swap': 0.915732435001953, 'LINA/USDT:USDT*binance&swap': 0.9150776489048118, 'SLP/USDT:USDT*binance&swap': 0.9143754989238985, 'OXT/USDT:USDT*binance&swap': 0.913509836958843, 'CKB/USDT:USDT*binance&swap': 0.91337051222677, 'HFT/USDT:USDT*binance&swap': 0.9116942962443926, 'BNB/USDT:USDT*binance&swap': 0.9112033063642414, 'ENS/USDT:USDT*binance&swap': 0.9103526135678535, 'SKL/USDT:USDT*binance&swap': 0.9070305011367518, 'PENDLE/USDT:USDT*binance&swap': 0.9067700088253019, 'POWR/USDT:USDT*binance&swap': 0.9065919655519298, 'ZEC/USDT:USDT*binance&swap': 0.9053704380164186, 'JASMY/USDT:USDT*binance&swap': 0.9052533836292499, 'NKN/USDT:USDT*binance&swap': 0.9044038477194483, 'ETH/USDT:USDT*binance&swap': 0.9041346981679579, 'CTSI/USDT:USDT*binance&swap': 0.9032942615501736, 'CAKE/USDT:USDT*binance&swap': 0.9029160092600955, 'OCEAN/USDT:USDT*binance&swap': 0.9021262284973074, 'WAXP/USDT:USDT*binance&swap': 0.9015392460752876, 'BNT/USDT:USDT*binance&swap': 0.900597373912709, 'CELR/USDT:USDT*binance&swap': 0.9000479606223627, 'ADA/USDT:USDT*binance&swap': 0.9000236638482063, 'TRU/USDT:USDT*binance&swap': 0.899720033436303, 'ROSE/USDT:USDT*binance&swap': 0.8983802674682474, 'CRV/USDT:USDT*binance&swap': 0.898142235427294, 'DOGE/USDT:USDT*binance&swap': 0.8970738257841543, 'ASTR/USDT:USDT*binance&swap': 0.8969159497595013, 'ILV/USDT:USDT*binance&swap': 0.8968277435135851, 'OP/USDT:USDT*binance&swap': 0.8967766837892998, 'GMX/USDT:USDT*binance&swap': 0.896588600458571, 'BICO/USDT:USDT*binance&swap': 0.8962575482580432, 'QNT/USDT:USDT*binance&swap': 0.8957321021067546, 'T/USDT:USDT*binance&swap': 0.8949683464917486, 'STG/USDT:USDT*binance&swap': 0.8947803547077372, 'KSM/USDT:USDT*binance&swap': 0.8946052976735199, 'SUPER/USDT:USDT*binance&swap': 0.8945346776384241, 'CHZ/USDT:USDT*binance&swap': 0.8939639686888874, 'BAND/USDT:USDT*binance&swap': 0.893488736498576, 'AGLD/USDT:USDT*binance&swap': 0.8930448930873147, 'RDNT/USDT:USDT*binance&swap': 0.8926874536723726, 'XAI/USDT:USDT*binance&swap': 0.8905604612604913, 'STORJ/USDT:USDT*binance&swap': 0.8904354773002894, 'ZRX/USDT:USDT*binance&swap': 0.8901383979058942, 'AXS/USDT:USDT*binance&swap': 0.889588817729828, 'GLM/USDT:USDT*binance&swap': 0.8885704735116571, 'UMA/USDT:USDT*binance&swap': 0.8870398574896229, 'NMR/USDT:USDT*binance&swap': 0.8866531751403934, 'FLOW/USDT:USDT*binance&swap': 0.8865631744885193, 'DASH/USDT:USDT*binance&swap': 0.8862165658989677, 'LTC/USDT:USDT*binance&swap': 0.8857876977232352, 'BAT/USDT:USDT*binance&swap': 0.8849917045355555, 'LSK/USDT:USDT*binance&swap': 0.8833874540719607, 'SEI/USDT:USDT*binance&swap': 0.8825029905212658, 'QTUM/USDT:USDT*binance&swap': 0.8819825117443382, 'XTZ/USDT:USDT*binance&swap': 0.8819295929353892, 'ARPA/USDT:USDT*binance&swap': 0.8817758720726554, 'MDT/USDT:USDT*binance&swap': 0.8813679352280577, 'KNC/USDT:USDT*binance&swap': 0.8798272396098533, 'RUNE/USDT:USDT*binance&swap': 0.8797896696508364, 'LINK/USDT:USDT*binance&swap': 0.879284568316374, 'DYDX/USDT:USDT*binance&swap': 0.8790971454331545, 'FIL/USDT:USDT*binance&swap': 0.8788716056403628, 'COMP/USDT:USDT*binance&swap': 0.8769363497973521, 'MAGIC/USDT:USDT*binance&swap': 0.8767632870326446, 'ICX/USDT:USDT*binance&swap': 0.8767392407306825, 'REN/USDT:USDT*binance&swap': 0.8758260127359001, 'EGLD/USDT:USDT*binance&swap': 0.8755741954786203, 'HBAR/USDT:USDT*binance&swap': 0.8752943309023203, 'RNDR/USDT:USDT*binance&swap': 0.8749295558789687, 'REEF/USDT:USDT*binance&swap': 0.8744189742950446, 'ORBS/USDT:USDT*binance&swap': 0.8743463774500198, 'BAL/USDT:USDT*binance&swap': 0.8738719161662793, 'LOOM/USDT:USDT*binance&swap': 0.8733474581029899, 'STRK/USDT:USDT*binance&swap': 0.8732508324057281, 'ALPHA/USDT:USDT*binance&swap': 0.8722178757221128, 'RSR/USDT:USDT*binance&swap': 0.8710622483497079, 'TLM/USDT:USDT*binance&swap': 0.8696735705822389, 'YGG/USDT:USDT*binance&swap': 0.8693334890020806, 'TIA/USDT:USDT*binance&swap': 0.8692900011404343, 'BSV/USDT:USDT*binance&swap': 0.868545338529137, 'THETA/USDT:USDT*binance&swap': 0.8683635211076384, 'MEME/USDT:USDT*binance&swap': 0.8683212947125913, 'MINA/USDT:USDT*binance&swap': 0.8683010580061903, 'ONT/USDT:USDT*binance&swap': 0.8678851818384284, 'LPT/USDT:USDT*binance&swap': 0.8672211158363804, 'SSV/USDT:USDT*binance&swap': 0.8665083432405253, 'MANTA/USDT:USDT*binance&swap': 0.8660133678557352, 'SNX/USDT:USDT*binance&swap': 0.8659561015879941, 'XLM/USDT:USDT*binance&swap': 0.8659382908000143, 'AUDIO/USDT:USDT*binance&swap': 0.8657868837730781, 'WOO/USDT:USDT*binance&swap': 0.8655471850077542, 'ENJ/USDT:USDT*binance&swap': 0.8649950328564653, 'DOT/USDT:USDT*binance&swap': 0.8647435012050496, 'IOTA/USDT:USDT*binance&swap': 0.8642485063298789, 'ACE/USDT:USDT*binance&swap': 0.8642378283018879, 'ANKR/USDT:USDT*binance&swap': 0.8639377159956773, 'ONE/USDT:USDT*binance&swap': 0.8638591721208286, 'SUSHI/USDT:USDT*binance&swap': 0.861116420825674, 'RLC/USDT:USDT*binance&swap': 0.8605958419961681, 'NEO/USDT:USDT*binance&swap': 0.8603698589719961, 'ALGO/USDT:USDT*binance&swap': 0.8586984206808767, 'XRP/USDT:USDT*binance&swap': 0.8578028805313834, 'KAVA/USDT:USDT*binance&swap': 0.8576772040580017, 'IOST/USDT:USDT*binance&swap': 0.857511591257687, 'AUCTION/USDT:USDT*binance&swap': 0.8568809017055511, 'XEM/USDT:USDT*binance&swap': 0.8553808499058065, 'ETHFI/USDT:USDT*binance&swap': 0.8534283626624272, 'OGN/USDT:USDT*binance&swap': 0.8531726928146605, 'JTO/USDT:USDT*binance&swap': 0.8525057317761471, 'GAL/USDT:USDT*binance&swap': 0.8523739136211552, 'ATOM/USDT:USDT*binance&swap': 0.8518170315655995, 'DAR/USDT:USDT*binance&swap': 0.8516410569604944, 'PORTAL/USDT:USDT*binance&swap': 0.8515848201184979, 'OMG/USDT:USDT*binance&swap': 0.8515379939419983, 'RVN/USDT:USDT*binance&swap': 0.8508139130132963, 'METIS/USDT:USDT*binance&swap': 0.850720536500283, 'C98/USDT:USDT*binance&swap': 0.8505148166054116, 'ICP/USDT:USDT*binance&swap': 0.8502862984408345, 'SUI/USDT:USDT*binance&swap': 0.8499920875690982, 'GAS/USDT:USDT*binance&swap': 0.8487430212534934, 'FXS/USDT:USDT*binance&swap': 0.8484732347270689, 'COTI/USDT:USDT*binance&swap': 0.8469093280817868, 'YFI/USDT:USDT*binance&swap': 0.846047303026302, 'IOTX/USDT:USDT*binance&swap': 0.8458016015651297, 'TRB/USDT:USDT*binance&swap': 0.8445028893055753, 'SNT/USDT:USDT*binance&swap': 0.8435685362774055, 'CHR/USDT:USDT*binance&swap': 0.8427117802699314, 'KLAY/USDT:USDT*binance&swap': 0.8426107698080992, 'ALICE/USDT:USDT*binance&swap': 0.8424408132891795, 'MOVR/USDT:USDT*binance&swap': 0.8419552049000361, 'BIGTIME/USDT:USDT*binance&swap': 0.8415846981568019, 'SPELL/USDT:USDT*binance&swap': 0.8412903847967381, 'BLUR/USDT:USDT*binance&swap': 0.8409152625959254, 'DGB/USDT:USDT*binance&swap': 0.8403565476807249, 'AAVE/USDT:USDT*binance&swap': 0.8386203819812934, 'SXP/USDT:USDT*binance&swap': 0.8379923719235753, 'PEOPLE/USDT:USDT*binance&swap': 0.8377411304392789, 'USTC/USDT:USDT*binance&swap': 0.8371665143517532, 'API3/USDT:USDT*binance&swap': 0.8370969593843487, 'TWT/USDT:USDT*binance&swap': 0.836782578791844, 'PERP/USDT:USDT*binance&swap': 0.8366619906102961, 'VET/USDT:USDT*binance&swap': 0.8358712789566789, 'RAD/USDT:USDT*binance&swap': 0.8358313154993666, 'WAVES/USDT:USDT*binance&swap': 0.8322917260895059, 'ALT/USDT:USDT*binance&swap': 0.8318691043386093, 'LRC/USDT:USDT*binance&swap': 0.831777304627007, 'AEVO/USDT:USDT*binance&swap': 0.8298380250798193, 'APE/USDT:USDT*binance&swap': 0.8273139983120693, 'CELO/USDT:USDT*binance&swap': 0.8259432115235125, 'DYM/USDT:USDT*binance&swap': 0.8222969993207959, 'MANA/USDT:USDT*binance&swap': 0.816789158563622, 'LDO/USDT:USDT*binance&swap': 0.8151040075196003, 'SAND/USDT:USDT*binance&swap': 0.8139570956882822, 'STX/USDT:USDT*binance&swap': 0.8128554628508539, 'GMT/USDT:USDT*binance&swap': 0.8118810413181711, 'HOT/USDT:USDT*binance&swap': 0.8082744204893979, 'ARB/USDT:USDT*binance&swap': 0.8054584835489114, 'GLMR/USDT:USDT*binance&swap': 0.8032874040614065, 'ZIL/USDT:USDT*binance&swap': 0.7985503999090662, 'TRX/USDT:USDT*binance&swap': 0.7900257843751827, 'AGIX/USDT:USDT*binance&swap': 0.7567498439754392, 'ETHW/USDT:USDT*binance&swap': 0.7358427567143775, 'ID/USDT:USDT*binance&swap': 0.7354993305202732, 'INJ/USDT:USDT*binance&swap': 0.729833871205434, 'ZETA/USDT:USDT*binance&swap': 0.7245075462796076, 'FET/USDT:USDT*binance&swap': 0.724158194213912, 'CFX/USDT:USDT*binance&swap': 0.7192228336390856, 'FTM/USDT:USDT*binance&swap': 0.7022474306303695, 'MATIC/USDT:USDT*binance&swap': 0.6993077061709054, 'XMR/USDT:USDT*binance&swap': 0.6842027835854145, 'PIXEL/USDT:USDT*binance&swap': 0.6697442083875644, 'BLZ/USDT:USDT*binance&swap': 0.6499591386792173, 'AR/USDT:USDT*binance&swap': 0.6471955525103626, 'APT/USDT:USDT*binance&swap': 0.6110699501230875, 'GALA/USDT:USDT*binance&swap': 0.6037153910036583, 'CYBER/USDT:USDT*binance&swap': 0.5941781196055889, 'FRONT/USDT:USDT*binance&swap': 0.5047091276444459, 'MKR/USDT:USDT*binance&swap': 0.48447148906571835, 'TON/USDT:USDT*binance&swap': 0.40153419913938443, 'MTL/USDT:USDT*binance&swap': 0.07836396529852521, 'USDC/USDT:USDT*binance&swap': -0.020551697500684165, 'BOME/USDT:USDT*binance&swap': -0.1451227043650543}

# WIF/USDT:USDT*binance&swap {'WIF/USDT:USDT*binance&swap': 1.0, 'GRT/USDT:USDT*binance&swap': 0.9472862398378481, 'PYTH/USDT:USDT*binance&swap': 0.9470320671016252, 'BCH/USDT:USDT*binance&swap': 0.9438569900705661, 'AVAX/USDT:USDT*binance&swap': 0.9415830224161972, '1INCH/USDT:USDT*binance&swap': 0.9351236989196416, 'SOL/USDT:USDT*binance&swap': 0.9347456668161047, 'JUP/USDT:USDT*binance&swap': 0.9343764591706827, 'WLD/USDT:USDT*binance&swap': 0.9329246010574674, 'BTC/USDT:USDT*binance&swap': 0.9290128477771049, 'CVX/USDT:USDT*binance&swap': 0.9275946763956151, 'ORDI/USDT:USDT*binance&swap': 0.9236555866576606, 'IMX/USDT:USDT*binance&swap': 0.9233481650899417, 'EOS/USDT:USDT*binance&swap': 0.9227778530218957, 'NEAR/USDT:USDT*binance&swap': 0.9225104532554458, 'MASK/USDT:USDT*binance&swap': 0.921401111484999, 'UNI/USDT:USDT*binance&swap': 0.9213991908984551, 'ACH/USDT:USDT*binance&swap': 0.9187054239949556, 'SLP/USDT:USDT*binance&swap': 0.9148500535537812, 'LINA/USDT:USDT*binance&swap': 0.914515067082312, 'ETC/USDT:USDT*binance&swap': 0.9144428044659738, 'CKB/USDT:USDT*binance&swap': 0.9139524016645246, 'OXT/USDT:USDT*binance&swap': 0.9131620523212539, 'HFT/USDT:USDT*binance&swap': 0.9120366927343907, 'BNB/USDT:USDT*binance&swap': 0.911163099301619, 'ENS/USDT:USDT*binance&swap': 0.9105971135344392, 'PENDLE/USDT:USDT*binance&swap': 0.9074444279418173, 'POWR/USDT:USDT*binance&swap': 0.9072601771480997, 'ETH/USDT:USDT*binance&swap': 0.9068984720179943, 'OCEAN/USDT:USDT*binance&swap': 0.9063215712999015, 'ZEC/USDT:USDT*binance&swap': 0.9055787070015396, 'CAKE/USDT:USDT*binance&swap': 0.9052426748626358, 'SKL/USDT:USDT*binance&swap': 0.9049162880637206, 'JASMY/USDT:USDT*binance&swap': 0.9048076716191408, 'NKN/USDT:USDT*binance&swap': 0.9047919736536187, 'CTSI/USDT:USDT*binance&swap': 0.9020986444312686, 'BNT/USDT:USDT*binance&swap': 0.9015549383403433, 'ADA/USDT:USDT*binance&swap': 0.9007297779982097, 'CELR/USDT:USDT*binance&swap': 0.900619182756559, 'ROSE/USDT:USDT*binance&swap': 0.9003763089905017, 'WAXP/USDT:USDT*binance&swap': 0.8996866182354367, 'GMX/USDT:USDT*binance&swap': 0.8989273578855558, 'ASTR/USDT:USDT*binance&swap': 0.8986367508415861, 'OP/USDT:USDT*binance&swap': 0.8984943216734684, 'TRU/USDT:USDT*binance&swap': 0.8983658496574132, 'DOGE/USDT:USDT*binance&swap': 0.8980051463279395, 'ILV/USDT:USDT*binance&swap': 0.8975547651179743, 'CRV/USDT:USDT*binance&swap': 0.8974302378295864, 'BICO/USDT:USDT*binance&swap': 0.8962038012976355, 'T/USDT:USDT*binance&swap': 0.895669861137662, 'QNT/USDT:USDT*binance&swap': 0.8948979982459777, 'CHZ/USDT:USDT*binance&swap': 0.8945905963963642, 'SUPER/USDT:USDT*binance&swap': 0.8942073905890094, 'STG/USDT:USDT*binance&swap': 0.8935674819666216, 'RDNT/USDT:USDT*binance&swap': 0.8933963699980161, 'KSM/USDT:USDT*binance&swap': 0.8931800252674388, 'BAND/USDT:USDT*binance&swap': 0.8929711760981313, 'AGLD/USDT:USDT*binance&swap': 0.8923751650610412, 'GLM/USDT:USDT*binance&swap': 0.8903006674435101, 'STORJ/USDT:USDT*binance&swap': 0.8900696943700384, 'AXS/USDT:USDT*binance&swap': 0.8898054100530468, 'XAI/USDT:USDT*binance&swap': 0.88961248705295, 'FLOW/USDT:USDT*binance&swap': 0.8885104157573988, 'UMA/USDT:USDT*binance&swap': 0.8876196787935474, 'LTC/USDT:USDT*binance&swap': 0.8861009780564973, 'NMR/USDT:USDT*binance&swap': 0.8860546404393498, 'BAT/USDT:USDT*binance&swap': 0.8859517717888177, 'DASH/USDT:USDT*binance&swap': 0.885881930323102, 'LSK/USDT:USDT*binance&swap': 0.8847804989109656, 'SEI/USDT:USDT*binance&swap': 0.8844652238813733, 'ZRX/USDT:USDT*binance&swap': 0.8842696514749832, 'QTUM/USDT:USDT*binance&swap': 0.8832812041115911, 'ARPA/USDT:USDT*binance&swap': 0.8814074771305024, 'LINK/USDT:USDT*binance&swap': 0.8805847333373522, 'KNC/USDT:USDT*binance&swap': 0.8800868783039236, 'MDT/USDT:USDT*binance&swap': 0.8798330371741103, 'RUNE/USDT:USDT*binance&swap': 0.879536775573531, 'XTZ/USDT:USDT*binance&swap': 0.8785800976840198, 'DYDX/USDT:USDT*binance&swap': 0.8785298495833089, 'ICX/USDT:USDT*binance&swap': 0.8775769447778511, 'MAGIC/USDT:USDT*binance&swap': 0.8773903902135306, 'FIL/USDT:USDT*binance&swap': 0.8773841530339352, 'COMP/USDT:USDT*binance&swap': 0.8771731778100617, 'RNDR/USDT:USDT*binance&swap': 0.8768075912830073, 'EGLD/USDT:USDT*binance&swap': 0.8760612694579155, 'REN/USDT:USDT*binance&swap': 0.8758738628350374, 'HBAR/USDT:USDT*binance&swap': 0.8758507967686165, 'BAL/USDT:USDT*binance&swap': 0.8751474889416447, 'REEF/USDT:USDT*binance&swap': 0.874994409865983, 'LOOM/USDT:USDT*binance&swap': 0.8740210728540327, 'STRK/USDT:USDT*binance&swap': 0.8734962517415151, 'ORBS/USDT:USDT*binance&swap': 0.8732440152754036, 'ALPHA/USDT:USDT*binance&swap': 0.8714278517748595, 'MINA/USDT:USDT*binance&swap': 0.8709086094103019, 'TIA/USDT:USDT*binance&swap': 0.8701329790408842, 'RSR/USDT:USDT*binance&swap': 0.8701088245087663, 'YGG/USDT:USDT*binance&swap': 0.8693160194784297, 'TLM/USDT:USDT*binance&swap': 0.8690577681860774, 'THETA/USDT:USDT*binance&swap': 0.8689052522896957, 'ONT/USDT:USDT*binance&swap': 0.8687326110750632, 'BSV/USDT:USDT*binance&swap': 0.8686196177624917, 'LPT/USDT:USDT*binance&swap': 0.8681477041640949, 'MEME/USDT:USDT*binance&swap': 0.867997687157532, 'XLM/USDT:USDT*binance&swap': 0.8676179139362789, 'SSV/USDT:USDT*binance&swap': 0.8669029904438081, 'SNX/USDT:USDT*binance&swap': 0.8662619808729867, 'MANTA/USDT:USDT*binance&swap': 0.8661930377559545, 'AUDIO/USDT:USDT*binance&swap': 0.8658314302410981, 'ENJ/USDT:USDT*binance&swap': 0.8657615353292186, 'DOT/USDT:USDT*binance&swap': 0.8651006156655556, 'WOO/USDT:USDT*binance&swap': 0.8650165641290416, 'ANKR/USDT:USDT*binance&swap': 0.8648397120282442, 'IOTA/USDT:USDT*binance&swap': 0.8642612637543586, 'ONE/USDT:USDT*binance&swap': 0.8633856722128787, 'ACE/USDT:USDT*binance&swap': 0.863289592483028, 'NEO/USDT:USDT*binance&swap': 0.8621015699825978, 'RLC/USDT:USDT*binance&swap': 0.8612785815424203, 'SUSHI/USDT:USDT*binance&swap': 0.8603258150694835, 'ALGO/USDT:USDT*binance&swap': 0.859180631862473, 'XEM/USDT:USDT*binance&swap': 0.8584711423904242, 'IOST/USDT:USDT*binance&swap': 0.85810969010792, 'ETHFI/USDT:USDT*binance&swap': 0.8572598651811115, 'XRP/USDT:USDT*binance&swap': 0.8571595912477177, 'KAVA/USDT:USDT*binance&swap': 0.8565610753165122, 'AUCTION/USDT:USDT*binance&swap': 0.8562233676359865, 'OGN/USDT:USDT*binance&swap': 0.8544737851181406, 'JTO/USDT:USDT*binance&swap': 0.852986821935097, 'ATOM/USDT:USDT*binance&swap': 0.8527001369131633, 'PORTAL/USDT:USDT*binance&swap': 0.8525649207622413, 'METIS/USDT:USDT*binance&swap': 0.8524431236103499, 'GAL/USDT:USDT*binance&swap': 0.8515395666213958, 'RVN/USDT:USDT*binance&swap': 0.851493272158598, 'C98/USDT:USDT*binance&swap': 0.8509732832711249, 'OMG/USDT:USDT*binance&swap': 0.8509518983395109, 'SUI/USDT:USDT*binance&swap': 0.8508259238682445, 'ICP/USDT:USDT*binance&swap': 0.8504372253836936, 'DAR/USDT:USDT*binance&swap': 0.849941216102778, 'FXS/USDT:USDT*binance&swap': 0.8494566218236719, 'COTI/USDT:USDT*binance&swap': 0.8489709751199505, 'GAS/USDT:USDT*binance&swap': 0.8485337692519394, 'YFI/USDT:USDT*binance&swap': 0.8466377565724175, 'IOTX/USDT:USDT*binance&swap': 0.8457709900995936, 'TRB/USDT:USDT*binance&swap': 0.8457159802315966, 'MOVR/USDT:USDT*binance&swap': 0.8434925019355322, 'SNT/USDT:USDT*binance&swap': 0.8429759401332192, 'DGB/USDT:USDT*binance&swap': 0.842946807882361, 'BLUR/USDT:USDT*binance&swap': 0.8424554124733087, 'ALICE/USDT:USDT*binance&swap': 0.8423485706328507, 'SPELL/USDT:USDT*binance&swap': 0.8413302793771652, 'BIGTIME/USDT:USDT*binance&swap': 0.8413277980605011, 'CHR/USDT:USDT*binance&swap': 0.840983171674854, 'KLAY/USDT:USDT*binance&swap': 0.8406439927915494, 'TWT/USDT:USDT*binance&swap': 0.8388551782824533, 'SXP/USDT:USDT*binance&swap': 0.8382938854634973, 'AAVE/USDT:USDT*binance&swap': 0.8381030944788862, 'PEOPLE/USDT:USDT*binance&swap': 0.8377011861529265, 'API3/USDT:USDT*binance&swap': 0.8373135127275558, 'USTC/USDT:USDT*binance&swap': 0.837269530980068, 'PERP/USDT:USDT*binance&swap': 0.8367959738575816, 'VET/USDT:USDT*binance&swap': 0.8367450687912019, 'RAD/USDT:USDT*binance&swap': 0.8364203084369606, 'WAVES/USDT:USDT*binance&swap': 0.8320255892587762, 'AEVO/USDT:USDT*binance&swap': 0.831665280071575, 'LRC/USDT:USDT*binance&swap': 0.831641848317795, 'ALT/USDT:USDT*binance&swap': 0.8307347179717577, 'APE/USDT:USDT*binance&swap': 0.828049986656613, 'CELO/USDT:USDT*binance&swap': 0.8274403092708775, 'DYM/USDT:USDT*binance&swap': 0.8228714978811807, 'LDO/USDT:USDT*binance&swap': 0.81829084651805, 'MANA/USDT:USDT*binance&swap': 0.8181560841449028, 'SAND/USDT:USDT*binance&swap': 0.8143149497922924, 'GMT/USDT:USDT*binance&swap': 0.812485819435642, 'STX/USDT:USDT*binance&swap': 0.8108843536581299, 'HOT/USDT:USDT*binance&swap': 0.810230065009098, 'ARB/USDT:USDT*binance&swap': 0.8091074175329613, 'GLMR/USDT:USDT*binance&swap': 0.8055935424782084, 'ZIL/USDT:USDT*binance&swap': 0.7989615069032978, 'TRX/USDT:USDT*binance&swap': 0.7894889276759605, 'AGIX/USDT:USDT*binance&swap': 0.7514496422612582, 'ETHW/USDT:USDT*binance&swap': 0.7356053222682022, 'FET/USDT:USDT*binance&swap': 0.7316759853324185, 'INJ/USDT:USDT*binance&swap': 0.7302026589886326, 'ID/USDT:USDT*binance&swap': 0.7249281806758944, 'ZETA/USDT:USDT*binance&swap': 0.7241469206233533, 'CFX/USDT:USDT*binance&swap': 0.7206825617699241, 'FTM/USDT:USDT*binance&swap': 0.7115222752099258, 'MATIC/USDT:USDT*binance&swap': 0.7006927616961751, 'XMR/USDT:USDT*binance&swap': 0.6876065800966094, 'PIXEL/USDT:USDT*binance&swap': 0.6786455254767081, 'AR/USDT:USDT*binance&swap': 0.657609900436668, 'BLZ/USDT:USDT*binance&swap': 0.6527228217546679, 'APT/USDT:USDT*binance&swap': 0.6161919968676312, 'GALA/USDT:USDT*binance&swap': 0.6102774297010558, 'CYBER/USDT:USDT*binance&swap': 0.5917140120557426, 'FRONT/USDT:USDT*binance&swap': 0.4991079503907106, 'MKR/USDT:USDT*binance&swap': 0.48805701970719084, 'TON/USDT:USDT*binance&swap': 0.4102554366484039, 'MTL/USDT:USDT*binance&swap': 0.09651121142654191, 'USDC/USDT:USDT*binance&swap': -0.01373485254717815, 'BOME/USDT:USDT*binance&swap': -0.12705303341750135}


# WIF/USDT:USDT*binance&swap {'WIF/USDT:USDT*binance&swap': 1.0, 'PYTH/USDT:USDT*binance&swap': 0.9472901627284437, 'GRT/USDT:USDT*binance&swap': 0.9462204003325217, 'BCH/USDT:USDT*binance&swap': 0.9444582802297763, 'AVAX/USDT:USDT*binance&swap': 0.9409589520209632, '1INCH/USDT:USDT*binance&swap': 0.9361406714126463, 'SOL/USDT:USDT*binance&swap': 0.9354388554296621, 'JUP/USDT:USDT*binance&swap': 0.9334761033459038, 'WLD/USDT:USDT*binance&swap': 0.9308414881744866, 'BTC/USDT:USDT*binance&swap': 0.9268000200997909, 'CVX/USDT:USDT*binance&swap': 0.925843073581588, 'ORDI/USDT:USDT*binance&swap': 0.9249302326485831, 'EOS/USDT:USDT*binance&swap': 0.9228040138195154, 'IMX/USDT:USDT*binance&swap': 0.922686298256834, 'MASK/USDT:USDT*binance&swap': 0.9209906180202546, 'NEAR/USDT:USDT*binance&swap': 0.9208038115760249, 'UNI/USDT:USDT*binance&swap': 0.9201325997354827, 'ACH/USDT:USDT*binance&swap': 0.9172931876575009, 'ETC/USDT:USDT*binance&swap': 0.9159310895485703, 'LINA/USDT:USDT*binance&swap': 0.9151072686791739, 'SLP/USDT:USDT*binance&swap': 0.9142923356068903, 'CKB/USDT:USDT*binance&swap': 0.9136502489876771, 'OXT/USDT:USDT*binance&swap': 0.9135225589902664, 'HFT/USDT:USDT*binance&swap': 0.911614772559694, 'BNB/USDT:USDT*binance&swap': 0.9112605280449122, 'ENS/USDT:USDT*binance&swap': 0.9106995011958211, 'PENDLE/USDT:USDT*binance&swap': 0.9068608609776012, 'SKL/USDT:USDT*binance&swap': 0.9068251770493054, 'POWR/USDT:USDT*binance&swap': 0.9067887795571113, 'JASMY/USDT:USDT*binance&swap': 0.9054420504260562, 'ZEC/USDT:USDT*binance&swap': 0.905166230970902, 'NKN/USDT:USDT*binance&swap': 0.904243115734441, 'ETH/USDT:USDT*binance&swap': 0.904205645177235, 'CTSI/USDT:USDT*binance&swap': 0.9031641924050541, 'CAKE/USDT:USDT*binance&swap': 0.902818490170584, 'OCEAN/USDT:USDT*binance&swap': 0.9024319722025551, 'WAXP/USDT:USDT*binance&swap': 0.9017244680899409, 'BNT/USDT:USDT*binance&swap': 0.9005224546464662, 'ADA/USDT:USDT*binance&swap': 0.9002037954918345, 'CELR/USDT:USDT*binance&swap': 0.8999760535897742, 'TRU/USDT:USDT*binance&swap': 0.8998921682665907, 'ROSE/USDT:USDT*binance&swap': 0.8981906584625362, 'CRV/USDT:USDT*binance&swap': 0.8975488681765674, 'OP/USDT:USDT*binance&swap': 0.897288640323324, 'DOGE/USDT:USDT*binance&swap': 0.8971273889454149, 'ASTR/USDT:USDT*binance&swap': 0.8970150765511441, 'GMX/USDT:USDT*binance&swap': 0.8969105399760804, 'ILV/USDT:USDT*binance&swap': 0.8968073609072079, 'BICO/USDT:USDT*binance&swap': 0.8962984993935238, 'QNT/USDT:USDT*binance&swap': 0.8954855323180454, 'T/USDT:USDT*binance&swap': 0.8949447017739112, 'STG/USDT:USDT*binance&swap': 0.8948484831596409, 'SUPER/USDT:USDT*binance&swap': 0.8946250620594224, 'KSM/USDT:USDT*binance&swap': 0.8944372550871791, 'CHZ/USDT:USDT*binance&swap': 0.8942346834111009, 'BAND/USDT:USDT*binance&swap': 0.8934161765741607, 'AGLD/USDT:USDT*binance&swap': 0.8929662186915348, 'RDNT/USDT:USDT*binance&swap': 0.8925643782961192, 'XAI/USDT:USDT*binance&swap': 0.8906398082133377, 'STORJ/USDT:USDT*binance&swap': 0.8904053288945747, 'ZRX/USDT:USDT*binance&swap': 0.8899350533757758, 'AXS/USDT:USDT*binance&swap': 0.8894304622212966, 'GLM/USDT:USDT*binance&swap': 0.8889323221456266, 'UMA/USDT:USDT*binance&swap': 0.8872046314380296, 'FLOW/USDT:USDT*binance&swap': 0.8867571584077324, 'NMR/USDT:USDT*binance&swap': 0.8867165978804115, 'DASH/USDT:USDT*binance&swap': 0.8864585139336805, 'LTC/USDT:USDT*binance&swap': 0.8858803887355946, 'BAT/USDT:USDT*binance&swap': 0.8850360796640091, 'LSK/USDT:USDT*binance&swap': 0.8834993274430757, 'SEI/USDT:USDT*binance&swap': 0.8823343715678282, 'XTZ/USDT:USDT*binance&swap': 0.8819942786567642, 'QTUM/USDT:USDT*binance&swap': 0.8819802272654589, 'ARPA/USDT:USDT*binance&swap': 0.8818943484330434, 'MDT/USDT:USDT*binance&swap': 0.8813224113350004, 'KNC/USDT:USDT*binance&swap': 0.879814293387045, 'RUNE/USDT:USDT*binance&swap': 0.8796038212114067, 'DYDX/USDT:USDT*binance&swap': 0.8793179944151238, 'LINK/USDT:USDT*binance&swap': 0.8791533235453219, 'FIL/USDT:USDT*binance&swap': 0.8789621924782626, 'COMP/USDT:USDT*binance&swap': 0.8769684414238031, 'ICX/USDT:USDT*binance&swap': 0.8769282932685012, 'MAGIC/USDT:USDT*binance&swap': 0.8768461221438927, 'EGLD/USDT:USDT*binance&swap': 0.8756833748732153, 'REN/USDT:USDT*binance&swap': 0.8754746046690545, 'HBAR/USDT:USDT*binance&swap': 0.8753576229566333, 'ORBS/USDT:USDT*binance&swap': 0.8743243362379793, 'RNDR/USDT:USDT*binance&swap': 0.8743206372704622, 'REEF/USDT:USDT*binance&swap': 0.8741880152623046, 'BAL/USDT:USDT*binance&swap': 0.873989192608017, 'STRK/USDT:USDT*binance&swap': 0.8736174933386186, 'LOOM/USDT:USDT*binance&swap': 0.8734783421192958, 'ALPHA/USDT:USDT*binance&swap': 0.8720464765506015, 'RSR/USDT:USDT*binance&swap': 0.8709385470256336, 'TLM/USDT:USDT*binance&swap': 0.8695375938049986, 'TIA/USDT:USDT*binance&swap': 0.8693730189782747, 'YGG/USDT:USDT*binance&swap': 0.8692002267752464, 'BSV/USDT:USDT*binance&swap': 0.8684935003296261, 'MINA/USDT:USDT*binance&swap': 0.8684376075448637, 'THETA/USDT:USDT*binance&swap': 0.8683584113937848, 'MEME/USDT:USDT*binance&swap': 0.8682924231130602, 'ONT/USDT:USDT*binance&swap': 0.8682161469756329, 'LPT/USDT:USDT*binance&swap': 0.867139405992777, 'SSV/USDT:USDT*binance&swap': 0.8665269057953243, 'SNX/USDT:USDT*binance&swap': 0.8662656260061941, 'MANTA/USDT:USDT*binance&swap': 0.8661208445175972, 'XLM/USDT:USDT*binance&swap': 0.8660533529878107, 'AUDIO/USDT:USDT*binance&swap': 0.8656612400843305, 'WOO/USDT:USDT*binance&swap': 0.8656307433013979, 'ENJ/USDT:USDT*binance&swap': 0.8651421880186234, 'DOT/USDT:USDT*binance&swap': 0.8648671593015371, 'IOTA/USDT:USDT*binance&swap': 0.864484900621799, 'ACE/USDT:USDT*binance&swap': 0.8640131642287493, 'ONE/USDT:USDT*binance&swap': 0.8639713241895814, 'ANKR/USDT:USDT*binance&swap': 0.8638321962932657, 'SUSHI/USDT:USDT*binance&swap': 0.8608766294117309, 'NEO/USDT:USDT*binance&swap': 0.8604596427425675, 'RLC/USDT:USDT*binance&swap': 0.8597005772959428, 'ALGO/USDT:USDT*binance&swap': 0.8588115322334918, 'XRP/USDT:USDT*binance&swap': 0.8583255862987196, 'IOST/USDT:USDT*binance&swap': 0.8579014950915651, 'KAVA/USDT:USDT*binance&swap': 0.8578582010668729, 'AUCTION/USDT:USDT*binance&swap': 0.8565412931967031, 'XEM/USDT:USDT*binance&swap': 0.8558273800222015, 'ETHFI/USDT:USDT*binance&swap': 0.8541813014972564, 'OGN/USDT:USDT*binance&swap': 0.8533914068131031, 'GAL/USDT:USDT*binance&swap': 0.8525688304949852, 'JTO/USDT:USDT*binance&swap': 0.852272124691442, 'PORTAL/USDT:USDT*binance&swap': 0.8521815188732063, 'ATOM/USDT:USDT*binance&swap': 0.8517536125999298, 'OMG/USDT:USDT*binance&swap': 0.8516196651123502, 'DAR/USDT:USDT*binance&swap': 0.8511273594401768, 'METIS/USDT:USDT*binance&swap': 0.8509574069809316, 'RVN/USDT:USDT*binance&swap': 0.8506965416373101, 'ICP/USDT:USDT*binance&swap': 0.8504944269119489, 'C98/USDT:USDT*binance&swap': 0.8503447256005456, 'SUI/USDT:USDT*binance&swap': 0.8499414067440622, 'GAS/USDT:USDT*binance&swap': 0.8487351100901834, 'FXS/USDT:USDT*binance&swap': 0.848701291173181, 'COTI/USDT:USDT*binance&swap': 0.8465569950174351, 'YFI/USDT:USDT*binance&swap': 0.8461628355596728, 'IOTX/USDT:USDT*binance&swap': 0.8455397255834294, 'TRB/USDT:USDT*binance&swap': 0.8445552012676647, 'SNT/USDT:USDT*binance&swap': 0.8435190365781089, 'KLAY/USDT:USDT*binance&swap': 0.8428290026702371, 'CHR/USDT:USDT*binance&swap': 0.8426663069695622, 'ALICE/USDT:USDT*binance&swap': 0.8423623097925212, 'MOVR/USDT:USDT*binance&swap': 0.8419811880160987, 'SPELL/USDT:USDT*binance&swap': 0.8416840050660586, 'BIGTIME/USDT:USDT*binance&swap': 0.8415604052083927, 'BLUR/USDT:USDT*binance&swap': 0.8409036972291304, 'DGB/USDT:USDT*binance&swap': 0.8407234184730153, 'AAVE/USDT:USDT*binance&swap': 0.8385768343689809, 'SXP/USDT:USDT*binance&swap': 0.8381089953652453, 'API3/USDT:USDT*binance&swap': 0.837303988151371, 'PEOPLE/USDT:USDT*binance&swap': 0.8373031781127004, 'TWT/USDT:USDT*binance&swap': 0.8368782250754015, 'USTC/USDT:USDT*binance&swap': 0.8368538398617631, 'PERP/USDT:USDT*binance&swap': 0.8365628274138114, 'RAD/USDT:USDT*binance&swap': 0.8360378061669479, 'VET/USDT:USDT*binance&swap': 0.8360166224632148, 'WAVES/USDT:USDT*binance&swap': 0.8323367613056644, 'ALT/USDT:USDT*binance&swap': 0.8318118512988477, 'LRC/USDT:USDT*binance&swap': 0.8317356652384537, 'AEVO/USDT:USDT*binance&swap': 0.8294846347380531, 'APE/USDT:USDT*binance&swap': 0.8274770730549126, 'CELO/USDT:USDT*binance&swap': 0.8259386096021282, 'DYM/USDT:USDT*binance&swap': 0.82235013073409, 'MANA/USDT:USDT*binance&swap': 0.8165602545923739, 'LDO/USDT:USDT*binance&swap': 0.8156575677637538, 'SAND/USDT:USDT*binance&swap': 0.8140359034301696, 'STX/USDT:USDT*binance&swap': 0.8131448702483824, 'GMT/USDT:USDT*binance&swap': 0.8119238389132337, 'HOT/USDT:USDT*binance&swap': 0.8084600987647607, 'ARB/USDT:USDT*binance&swap': 0.8060540770976001, 'GLMR/USDT:USDT*binance&swap': 0.8037352415715644, 'ZIL/USDT:USDT*binance&swap': 0.7986369453008094, 'TRX/USDT:USDT*binance&swap': 0.7900293001580367, 'AGIX/USDT:USDT*binance&swap': 0.7563266415445629, 'ETHW/USDT:USDT*binance&swap': 0.7357173577520967, 'ID/USDT:USDT*binance&swap': 0.7346551154449983, 'INJ/USDT:USDT*binance&swap': 0.7299231293796629, 'FET/USDT:USDT*binance&swap': 0.7258091110701627, 'ZETA/USDT:USDT*binance&swap': 0.7245048348627532, 'CFX/USDT:USDT*binance&swap': 0.7192381808374368, 'FTM/USDT:USDT*binance&swap': 0.7033150053798318, 'MATIC/USDT:USDT*binance&swap': 0.6991743746652735, 'XMR/USDT:USDT*binance&swap': 0.684558836147987, 'PIXEL/USDT:USDT*binance&swap': 0.6710758639458204, 'BLZ/USDT:USDT*binance&swap': 0.6502280946661027, 'AR/USDT:USDT*binance&swap': 0.6464355598689804, 'APT/USDT:USDT*binance&swap': 0.6102860936121037, 'GALA/USDT:USDT*binance&swap': 0.6034961876062704, 'CYBER/USDT:USDT*binance&swap': 0.5937267269358886, 'FRONT/USDT:USDT*binance&swap': 0.5049951498856471, 'MKR/USDT:USDT*binance&swap': 0.4844165559629146, 'TON/USDT:USDT*binance&swap': 0.40236965059214835, 'MTL/USDT:USDT*binance&swap': 0.07869289357337665, 'USDC/USDT:USDT*binance&swap': -0.022691201368258383, 'BOME/USDT:USDT*binance&swap': -0.1424069077328805}

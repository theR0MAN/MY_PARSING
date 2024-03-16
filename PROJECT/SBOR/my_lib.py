from numpy import argsort
import lzma as lz
import  json
import redis
import pickle
#  сортирует словарь по значениям
def mysortdict(dict) :
	keys = list(dict.keys())
	values = list(dict.values())
	sorted_value_index = argsort(values)
	dict_1={keys[i]: values[i] for i in sorted_value_index}
	dict_2 = {}
	for key in reversed(dict_1):
		dict_2[key] = dict_1[key]
	return dict_2

def mysortspis (data,rev=False):
	res = sorted(data, reverse=rev, key=lambda x: x[1])
	return res


def myput(name,data):
	with lz.open(name, "w") as f:
		f.write(lz.compress(json.dumps(data).encode('utf-8')))

def myload(name):
	with lz.open(name) as f:
		data = json.loads(lz.decompress(f.read()).decode('utf-8'))
	return data


r = redis.Redis(db=1)
pipeline = r.pipeline()



def myredput(key, data):
	r.set(key, pickle.dumps(data))

def myredget(key):
	if r.exists(key):
		return pickle.loads(r.get(key))
	else:
		return None

def myreddel(key):
	r.delete(key)

def myreddelall():
	r.flushdb()


def mycontget(dct):
	# получать данные по крипте из редиса в виде снапшота словарей
	# dct словарь списков  в формате A[биржа].append(символ)  - нуен тобы не делать перебор по ключам в редис
	rez=dict()
	symspis = []
	for ex in dct:
		rez[ex]=dict()
		for sym in dct[ex]:
			rez[ex][sym]=dict()
			symspis.append(sym + '*' + ex)
	for sym in symspis:
		pipeline.get(sym)
	results = pipeline.execute()

	count=0
	for sym in symspis:
		z = sym.partition('*')
		instr=z[0]
		ex=z[2]
		if results[count]!=None:
			rez[ex][instr]= pickle.loads(results[count])
		else:
			rez[ex][instr] =None
		count+=1
	return rez


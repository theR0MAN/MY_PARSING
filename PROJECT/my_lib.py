from numpy import argsort
import lzma as lz
import  json

#  сортирует словарь по значениям
def mysortdict(dict) :
	keys = list(dict.keys())
	values = list(dict.values())
	sorted_value_index = argsort(values)
	d={keys[i]: values[i] for i in sorted_value_index}
	return d

def myput(name,data):
	with lz.open(name, "w") as f:
		f.write(lz.compress(json.dumps(data).encode('utf-8')))



def myload(name):
	with lz.open(name) as f:
		data = json.loads(lz.decompress(f.read()).decode('utf-8'))
	return data
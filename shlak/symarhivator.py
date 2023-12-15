import lzma
import os
import json

putpath = 'G:\\DATA_SBOR\\ASYMBOLS_INFO\\2023\\12\\'

files = []

for x in os.listdir(putpath):
	if x.endswith(".json"):
		files.append(putpath+x)
print(files)

lz = lzma
for namefile in files:
	nname = namefile.replace(".json", ".roman")
	with open(namefile, "r") as read_file:
		print(namefile)
		data = json.load(read_file)
	with lz.open(nname, "w") as f:
		print("   СТАРТ ЗАПИСИ  ", namefile)
		f.write(lz.compress(json.dumps(data).encode('utf-8')))
		print("   ЗАПИСАНО   ", namefile)



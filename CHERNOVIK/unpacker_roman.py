import lzma
import json

name='/media/roman/J/rOLDHIST/FONDA/2019/1/3/14.roman'

with lzma.open(name) as f:
    a=dict(json.loads(lzma.decompress(f.read()).decode('utf-8')))


print(a["1546524000"])

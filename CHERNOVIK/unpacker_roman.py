import lzma
import json

name='/media/roman/J/rOLDHIST/FONDA/2020/5/5/10.roman'
lz=lzma
with lz.open(name) as f:
    a=dict(json.loads(lz.decompress(f.read()).decode('utf-8')))

print(a["1588672803"])

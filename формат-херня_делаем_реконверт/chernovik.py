
import json

import lzma as lz

with lz.open('100.roman') as f:
    a=dict(json.loads(lz.decompress(f.read()).decode('utf-8')))

print(a)
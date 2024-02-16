from PROJECT.SBOR.my_lib import *
import plotly.express as px
from PROJECT.VIZUAL.Viz_lib import get_color
import time


a= myload('mystruct')
for id in a:
	print(id,a[id])
	for sym in a[id]:
		print(sym)
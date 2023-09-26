# from chernovik9 import *
from threading import Thread
from multiprocessing import Process
import time
from One_inst_class import Myinst
 


from plotly.subplots import make_subplots
import plotly.graph_objects as go

fig = make_subplots(rows=3, cols=2)

fig.add_trace(go.Scatter( x=[3, 4, 5],     y=[1000, 1100, 1200],), row=1, col=1)

fig.add_trace(go.Scatter(  x=[2, 3, 4], y=[100, 110, 120],), row=2, col=2)

fig.add_trace(go.Scatter( x=[0, 1, 2], y=[10, 11, 12]), row=3, col=1)


# fig.update_layout(height=1000, width=1000, title_text="Stacked Subplots")
# fig.update_layout(height=1000, width=1000, title_text="Stacked Subplots")
fig.show()
#
#
# def proc():
# 	if __name__ == '__main__':
# 		Process(target=count, args=('first1',)).start()
# 		Process(target=count, args=('first2',)).start()
# 		Process(target=count, args=('first4',)).start()
# 		Process(target=count, args=('first5',)).start()
# 		Process(target=count, args=('first6',)).start()
# 		Process(target=count, args=('first7',)).start()
# 		Process(target=count, args=('first8',)).start()
# 		Process(target=count, args=('first9',)).start()
# 		Process(target=count, args=('first10',)).start()
#
#
# def thr():
# 	if __name__ == '__main__':
# 		Thread(target=count, args=('first1',)).start()
# 		Thread(target=count, args=('first2',)).start()
# 		Thread(target=count, args=('first4',)).start()
# 		Thread(target=count, args=('first5',)).start()
# 		Thread(target=count, args=('first6',)).start()
# 		Thread(target=count, args=('first7',)).start()
# 		Thread(target=count, args=('first8',)).start()
# 		Thread(target=count, args=('first9',)).start()
# 		Thread(target=count, args=('first10',)).start()
#
#
# thr()

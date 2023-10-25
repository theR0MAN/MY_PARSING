from PROJECT.VIZUAL.Viz_lib import get_color
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
xmas=[]
ymas=[]
ymas2=[]

for x in range(100):
	xmas.append(x)
	ymas.append(x**2)
	ymas2.append(x )
#
#
# color = get_color()
# fig = px.line()
#
# clr = color()
# fig.add_scatter(x=xmas, y=ymas, line_color=clr, name=' Y')
# fig.show()
color = get_color()
clr = color()
fig = make_subplots(rows=2, cols=1)
fig.add_trace(go.Scatter( x=xmas,     y=ymas, line_color=clr), row=1, col=1)
fig.add_trace(go.Scatter(  x=xmas, y=ymas2, line_color=clr), row=2, col=1)



# fig.update_layout(height=1000, width=1000, title_text="Stacked Subplots")
# fig.update_layout(height=1000, width=1000, title_text="Stacked Subplots")
fig.show()

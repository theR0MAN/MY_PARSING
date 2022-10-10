import plotly.express as px
# https://plotly.com/python/line-charts/
# https://python-school.ru/blog/plotly-plotting/
# https://translated.turbopages.org/proxy_u/en-ru.ru.74167578-634222ec-21563749-74722d776562/https/www.geeksforgeeks.org/using-plotly-for-interactive-data-visualization-in-python/



# import plotly.express as px
# import pandas as pd
#
# df = pd.DataFrame(dict(
#     x = [1, 3, 2, 4],
#     y = [1, 2, 3, 4]
# ))
# fig = px.line(df, x="x", y="y", title="Unsorted Input")
# fig.show()
#
import plotly.graph_objects as go
from plotly.offline import init_notebook_mode, iplot

x_link = [[125, 257, None], [125, 787, None]]
y_link = [[383, 588, None], [383, 212, None]]
z_link = [[65, 85, None], [65, 526, None]]

# figure formatting
colors=['red', 'green']
link_size = [2,12]

# make multiple traces
traces={}
for i in range(0, len(x_link)):
    traces['trace_' + str(i)]=go.Scatter3d(x = x_link[i],
                                           y = y_link[i],
                                           z = z_link[i],
                                           line=dict(
                                                color=colors[i],
                                                width=link_size[i]))
data=list(traces.values())

# build and plot figure
fig=go.Figure(data)
fig.show()
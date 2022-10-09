import plotly.express as px
# https://plotly.com/python/line-charts/
# https://python-school.ru/blog/plotly-plotting/
# https://translated.turbopages.org/proxy_u/en-ru.ru.74167578-634222ec-21563749-74722d776562/https/www.geeksforgeeks.org/using-plotly-for-interactive-data-visualization-in-python/



import plotly.express as px
import pandas as pd

df = pd.DataFrame(dict(
    x = [1, 3, 2, 4],
    y = [1, 2, 3, 4]
))
fig = px.line(df, x="x", y="y", title="Unsorted Input")
fig.show()

df = df.sort_values(by="x")
fig = px.line(df, x="x", y="y", title="Sorted Input")
fig.show()
import plotly.express as px

df = px.data.iris()
fig = px.scatter(df,
                 x="sepal_width", y="sepal_length",
                 color="species",
                 title="A Plotly Express Figure")
      # width=3840*4,height=2160*2

print(df)
fig.show()
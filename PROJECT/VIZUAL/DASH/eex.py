import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly
import random
import plotly.graph_objs as go

def muyY():
	X = list()
	X.append(1)

	Y = []
	Y.append(1)

	app = dash.Dash(__name__)

	app.layout = html.Div(
		[
			dcc.Graph(id = 'live-graph', animate = True),
			dcc.Interval(
				id = 'graph-update',
				interval = 500,
				n_intervals = 0
			),
		]
	)

	@app.callback(
		Output('live-graph', 'figure'),
		[ Input('graph-update', 'n_intervals') ]
	)

	def update(n):
		X.append(X[-1]+1)
		Y.append(Y[-1]+1)

		data = plotly.graph_objs.Scatter(x=X,y=Y,name='Scatter',mode= 'lines')

		return {'data': [data],
				'layout' : go.Layout(xaxis=dict(range=[min(X),max(X)]),yaxis = dict(range = [min(Y),max(Y)]),)}


	app.run_server()


# muyY()
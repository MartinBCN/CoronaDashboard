import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.offline as pyo
import plotly.graph_objects as go

import pandas as pd
pd.options.display.width = 0

# df = pd.read_csv('data/owid-covid-data.csv')
# print(df.head())
# print(df['location'])
#
#
# # Use a for loop (or list comprehension to create traces for the data list)
#
# data = [go.Scatter(x=df[df['location'] == location]['date'],
#                    y=df[df['location'] == location]['new_cases'],
#                    mode='lines',
#                    name=location) for location in ['Germany']]
#
# pyo.plot(data)


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Tabs(id='tabs-example', value='tab-1', children=[
        dcc.Tab(label='Tab one', value='tab-1'),
        dcc.Tab(label='Tab two', value='tab-2'),
    ]),
    html.Div(id='tabs-example-content')
])

@app.callback(Output('tabs-example-content', 'children'),
              Input('tabs-example', 'value'))
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            html.H3('Tab content 1')
        ])
    elif tab == 'tab-2':
        return html.Div([
            html.H3('Tab content 2')
        ])


if __name__ == '__main__':
    app.run_server(debug=True)
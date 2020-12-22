import dash
import dash_html_components as html
import dash_core_components as dcc
import flask
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from corona.cases import plot_cases
from corona.data import get_data
from corona.scatter_plots import plot_scatter

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', dbc.themes.BOOTSTRAP]

df = get_data()

server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config.suppress_callback_exceptions = True


app.layout = html.Div([
    dcc.Tabs(id='tabs-corona', value='time_series', children=[
        dcc.Tab(label='Time Series',
                children=html.Div([
                    plot_cases(app, df)
                ])),
        dcc.Tab(label='Scatter Plots',
                children=html.Div([
                    plot_scatter(app, df)
                ])),
    ]),
    html.Div(id='main')
])


if __name__ == "__main__":
    import os

    # debug = False if os.environ.get("DASH_DEBUG_MODE", 'False') == "False" else True
    app.run_server(host="0.0.0.0", port=8050, debug=False)

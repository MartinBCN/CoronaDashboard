import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from cases import plot_cases
from data import get_data
from scatter_plots import plot_scatter

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', dbc.themes.BOOTSTRAP]

df = get_data()

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Tabs(id='tabs-corona', value='time_series', children=[
        dcc.Tab(label='Time Series', value='time_series'),
        dcc.Tab(label='Scatter Plots', value='scatter'),
    ]),
    html.Div(id='main')
])


@app.callback(Output('main', 'children'),
              Input('tabs-corona', 'value'))
def render_content(tab):
    if tab == 'time_series':
        return html.Div([
            plot_cases(app, df)
        ])

    elif tab == 'scatter':
        return html.Div([
            plot_scatter(app, df)
        ])


if __name__ == '__main__':
    app.run_server(debug=False)

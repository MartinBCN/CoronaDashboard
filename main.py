import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from cases import plot_cases
from data import get_data
from scatter_plots import plot_scatter

external_stylesheets = ['style.css', dbc.themes.BOOTSTRAP]

df = get_data()

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
        return plot_cases(app, df)

    elif tab == 'tab-2':
        return html.Div([
            plot_scatter(app, df)
        ])


if __name__ == '__main__':
    app.run_server(debug=True)

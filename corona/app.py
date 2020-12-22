import dash
import dash_html_components as html
import dash_core_components as dcc
import flask
import dash_bootstrap_components as dbc

from corona.tabs.cases import plot_cases
from corona.tabs.data import get_data
from corona.tabs.scatter_plots import plot_scatter

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', dbc.themes.BOOTSTRAP]

df = get_data()

server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config.suppress_callback_exceptions = True


def build_banner():
    return html.Div(
        id="banner",
        className="banner",
        children=[
            html.Div(
                id="banner-text",
                children=[
                    html.H5("Corona Dashboard"),
                    html.H6("Process Control and Exception Reporting"),
                ],
            ),
            html.Div(
                id="banner-logo",
                children=[
                    html.Button(
                        id="learn-more-button", children="LEARN MORE", n_clicks=0
                    ),
                    html.Img(id="logo", src=app.get_asset_url("dash-logo-new.png")),
                ],
            ),
        ],
    )


app.layout = html.Div([
    build_banner(),
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
    # debug = False if os.environ.get("DASH_DEBUG_MODE", 'False') == "False" else True
    app.run_server(host="0.0.0.0", port=8050, debug=False)

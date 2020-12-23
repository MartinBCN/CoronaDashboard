import dash
import dash_html_components as html
import dash_core_components as dcc
import flask
import dash_bootstrap_components as dbc

from corona.tabs.cases import plot_cases
from corona.tabs.data import get_data
from corona.tabs.scatter_plots import plot_scatter

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', dbc.themes.BOOTSTRAP]

df = get_data()

server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server
                , external_stylesheets=[dbc.themes.BOOTSTRAP]
                # ,meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}]
                )
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


def build_tabs():
    return html.Div(
        id="tabs",
        className="tabs",
        children=[
            dcc.Tabs(
                id="tabs-corona",
                value="time_series",
                className="custom-tabs",
                children=[
                    dcc.Tab(
                        id="Specs-tab",
                        label="Time Series",
                        value="tab_time_series",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                        children=html.Div([
                            plot_cases(app, df)
                        ])
                    ),
                    dcc.Tab(
                        id="Control-chart-tab",
                        label="Scatter Plots",
                        value="tab_scatter_plots",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                        children=html.Div([
                            plot_scatter(app, df)
                        ])
                    ),
                ],
            )
        ],
    )


app.layout = html.Div([
    build_banner(),
    build_tabs(),
    html.Div(id='main')
])


if __name__ == "__main__":
    # debug = False if os.environ.get("DASH_DEBUG_MODE", 'False') == "False" else True
    app.run_server(host="0.0.0.0", port=8050, debug=False)

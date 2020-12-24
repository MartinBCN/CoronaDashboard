import dash
import dash_html_components as html
import dash_core_components as dcc
import flask
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, ClientsideFunction

from tabs.cases import plot_cases
from tabs.data import get_data
from tabs.map import generate_map
from tabs.scatter_plots import plot_scatter


df = get_data()

server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config.suppress_callback_exceptions = True


def build_banner():
    return html.Div(
            [
                html.Div(
                    [
                        html.Img(
                            src=app.get_asset_url("dash-logo.png"),
                            id="plotly-image",
                            style={
                                "height": "60px",
                                "width": "auto",
                                "margin-bottom": "25px",
                            },
                        )
                    ],
                    className="one-third column",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H3(
                                    "Corona Dashboard",
                                    style={"margin-bottom": "0px"},
                                ),
                                html.H5(
                                    "Analysis", style={"margin-top": "0px"}
                                ),
                            ]
                        )
                    ],
                    className="one-third column",
                    id="title",
                ),
                html.Div(
                    [
                        html.A(
                            html.Button("Learn More", id="learn-more-button"),
                            href="https://github.com/MartinBCN/CoronaDashboard",
                        )
                    ],
                    className="one-third column",
                    id="button",
                ),
            ],
            id="header",
            className="row flex-display",
            style={"margin-bottom": "25px"},
        )


def build_tabs():
    return html.Div(
        id="tabs",
        className="tabs",
        children=[
            dcc.Tabs(
                id="tabs-corona",
                value="tab_time_series",
                className="custom-tabs",
                children=[
                    dcc.Tab(
                        id="tab-time-series",
                        label="Time Series",
                        value="tab_time_series",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                        children=html.Div([
                            plot_cases(app, df)
                        ])
                    ),
                    dcc.Tab(
                        id="tab-scatter-plot",
                        label="Scatter Plots",
                        value="tab_scatter_plots",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                        children=html.Div([
                            plot_scatter(app, df)
                        ])
                    ),
                    dcc.Tab(
                        id="tab-map",
                        label="Map",
                        value="tab_map",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                        children=html.Div([
                            generate_map(app, df)
                        ])
                    ),
                ],
            )
        ],
    )


app.layout = html.Div(children=[
    html.Div(id="output-clientside"),
    build_banner(),
    build_tabs()
],
    id="mainContainer",
    style={"display": "flex", "flex-direction": "column"})


if __name__ == "__main__":
    # debug = False if os.environ.get("DASH_DEBUG_MODE", 'False') == "False" else True
    app.run_server(host="0.0.0.0", port=8050, debug=False)

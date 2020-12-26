
import dash_html_components as html
import dash_core_components as dcc

from maindash import app
from utils.data import get_data
from tabs.map import generate_map

from tabs.cases import generate_cases
from tabs.scatter_plots import generate_scatter


df = get_data()


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
    tab_time_series = dcc.Tab(
                        id="tab-time-series",
                        label="Time Series",
                        value="tab_time_series",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                        children=generate_cases()
    )

    tab_scatter_plots = dcc.Tab(
                        id="tab-scatter-plot",
                        label="Scatter Plots",
                        value="tab_scatter_plots",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                        children=generate_scatter()
                    )

    tab_map = dcc.Tab(
                id="tab-map",
                label="Map",
                value="tab_map",
                className="custom-tab",
                selected_className="custom-tab--selected",
                children=generate_map()
    )

    tabs = html.Div(
        id="tabs",
        className="tabs",
        children=[
            dcc.Tabs(
                id="tabs-corona",
                value="tab_time_series",  # Default Choice
                className="custom-tabs",
                children=[tab_time_series, tab_scatter_plots, tab_map],
            )
        ],
    )

    return tabs


def main_layout():
    return html.Div(children=[
                html.Div(id="output-clientside"),
                build_banner(),
                build_tabs()
            ],
                id="mainContainer",
                style={"display": "flex", "flex-direction": "column"})

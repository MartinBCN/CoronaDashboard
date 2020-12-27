
import dash_html_components as html
import dash_core_components as dcc

from maindash import df
from tabs.cases import generate_cases


def build_banner():
    return html.Div(children=[
        html.H3("Corona Dashboard", style={"margin-bottom": "0px"}),
        html.H5("Analysis", style={"margin-top": "0px"})
    ])


def build_body():
    body = html.Div(children=[
        html.Div(
                dcc.Graph(id='cases',
                          config={'displayModeBar': False}),
                style={'width': '45%', 'display': 'inline-block'},
                        className = "pretty_container"
            ),

        html.Div(
            style={'width': '5%', 'display': 'inline-block'}
                ),

        html.Div(
            dcc.Graph(id='deaths',
                      config={'displayModeBar': False}),
            style={'width': '45%', 'display': 'inline-block'},
            className="pretty_container"
        )
    ]
    )

    return body


def build_controls():

    all_countries = [{'value': country, 'label': f'{country}'} for country in df['location'].unique()]

    controls = html.Div(
            [
                html.Div(children=' ', style={'width': '90%',   'min-height': '1.25em', 'line-height': '1.25'}),
                html.Div(
                    dcc.Dropdown(id='country_dropdown', options=all_countries, value=['Germany'], multi=True),
                    style={'width': '45%', 'display': 'inline-block', 'vertical-align': 'middle'}
                ),
                html.Div(style={'width': '9%', 'display': 'inline-block'}),
                html.Div(

                    [
                        html.Div(
                            html.Button('Toggle Cumulative', id='toggle-cumulative', n_clicks=1),
                            style={'width': '32%', 'display': 'inline-block', 'vertical-align': 'middle'}
                        ),
                        html.Div(
                            html.Button('Toggle Normalisation', id='toggle-normalise', n_clicks=1),
                            style={'width': '32%', 'display': 'inline-block', 'vertical-align': 'middle'}
                        ),
                        html.Div(
                            html.Button('Toggle Rolling', id='toggle-rolling', n_clicks=1),
                            style={'width': '32%', 'display': 'inline-block', 'vertical-align': 'middle'}
                        ),
                    ],
                    style={'width': '45%', 'display': 'inline-block'}
                )
            ]
    )

    return controls


def main_layout():
    return html.Div(children=[
                build_banner(),
                build_controls(),
                build_body()
            ],
                id="mainContainer",
                style={"display": "flex", "flex-direction": "column"})

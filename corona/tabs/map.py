import plotly.graph_objects as go
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
from maindash import df, app
import plotly.express as px
from dash.dependencies import Input, Output


def slice_data_frame(continent: str, cumulative: bool, normalise: bool, rolling: bool, type: str):

    df_continent = df[df['continent'] == continent].copy()

    if cumulative:
        prefix = 'total'
    else:
        prefix = 'new'

    if normalise:
        suffix = '_per_million'
    else:
        suffix = ''

    field = f'{prefix}_{type}{suffix}'

    df_continent = df_continent[['date', 'iso_code', 'location', 'continent', field]]

    if rolling:
        df_continent[field] = df_continent[field].rolling(7).mean(),

    df_continent = df_continent.dropna()

    idx = df_continent.groupby(['location'])['date'].transform(max) == df_continent['date']

    df_continent = df_continent[idx]

    return field, df_continent


def plot_map(continent: str, cumulative: bool, normalise: bool, rolling: bool, type: str):

    field, df_continent = slice_data_frame(continent, cumulative, normalise, rolling, type)

    # --------------------
    #  Chloropleth Map
    # --------------------

    fig = px.choropleth(df_continent, locations='iso_code', color=field,
                        color_continuous_scale="Bluered", scope=continent.lower())
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig.update_layout(
        title=field,
        font=dict(size=6),
        height=600
    )
    return fig


def plot_bar_chart(continent: str, cumulative: bool, normalise: bool, rolling: bool, type: str):

    field, df_continent = slice_data_frame(continent, cumulative, normalise, rolling, type)
    # --------------------
    #  Bar Chart
    # --------------------

    df_continent = df_continent.sort_values(by=field)

    fig = go.Figure(go.Bar(
        x=df_continent[field],
        y=df_continent['location'],
        orientation='h'))

    fig.update_layout(
        title=field,
        font=dict(size=6),
        height=600
    )

    return fig


@app.callback(
    Output('plot-map', 'figure'),
    [Input('continent-dropdown', 'value'),
     Input('toggle-normalise-continent', 'n_clicks'),
     Input('toggle-cumulative-continent', 'n_clicks'),
     Input('toggle-rolling-continent', 'n_clicks')]
)
def update_map(continent: str , normalise_clicks: int, cumulative_clicks: int, rolling_clicks: int) -> dict:

    return plot_map(continent=continent,
                    cumulative=(cumulative_clicks % 2) == 0,
                    normalise=(normalise_clicks % 2) == 0,
                    rolling=(rolling_clicks % 2) == 0,
                    type='deaths'
                    )


@app.callback(
    Output('plot-bar-chart', 'figure'),
    [Input('continent-dropdown', 'value'),
     Input('toggle-normalise-continent', 'n_clicks'),
     Input('toggle-cumulative-continent', 'n_clicks'),
     Input('toggle-rolling-continent', 'n_clicks')]
)
def update_bar(continent: str , normalise_clicks: int, cumulative_clicks: int, rolling_clicks: int) -> go.Figure:
    return plot_bar_chart(continent=continent,
                          cumulative=(cumulative_clicks % 2) == 0,
                          normalise=(normalise_clicks % 2) == 0,
                          rolling=(rolling_clicks % 2) == 0,
                          type='deaths')


def generate_selectors():
    all_continents = [{'value': country, 'label': f'{country}'} for country in df['continent'].dropna().unique()]

    selector = html.Div(
        children=[
            html.Div(children=' ', style={'width': '90%', 'min-height': '1.25em', 'line-height': '1.25'}),
            html.Div(
                dcc.Dropdown(id='continent-dropdown', options=all_continents, value='Europe', multi=False),
                style={'width': '45%', 'display': 'inline-block', 'vertical-align': 'middle'}
            ),
            html.Div(
                style={'width': '9%', 'display': 'inline-block'}
            ),
            html.Div(

                [
                    html.Div(
                        html.Button('Toggle Cumulative', id='toggle-cumulative-continent', n_clicks=1),
                        style={'width': '32%', 'display': 'inline-block', 'vertical-align': 'middle'}
                    ),
                    html.Div(
                        html.Button('Toggle Normalisation', id='toggle-normalise-continent', n_clicks=1),
                        style={'width': '32%', 'display': 'inline-block', 'vertical-align': 'middle'}
                    ),
                    html.Div(
                        html.Button('Toggle Rolling', id='toggle-rolling-continent', n_clicks=1),
                        style={'width': '32%', 'display': 'inline-block', 'vertical-align': 'middle'}
                    ),
                ],
                style={'width': '45%', 'display': 'inline-block'}
            )
        ]
    )

    return selector


def generate_map() -> html.Div:

    return html.Div(children=[
        generate_selectors(),

        html.Div(
            dcc.Graph(id='plot-map',
                      config={'displayModeBar': False}),
            style={'width': '45%', 'display': 'inline-block'},
            className="pretty_container"
        ),

        html.Div(
            style={'width': '5%', 'display': 'inline-block'}
        ),

        html.Div(
            dcc.Graph(id='plot-bar-chart',
                      config={'displayModeBar': False}),
            style={'width': '45%', 'display': 'inline-block'},
            className="pretty_container"
        )
    ])

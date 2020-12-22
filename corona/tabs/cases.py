import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_daq as daq
from corona.tabs.data import get_data

# total_cases  new_cases  total_cases_per_million  new_cases_per_million
FIELDS = {
    'cases': {
        'normalised': {'cumulative': 'total_cases_per_million', 'new': 'new_cases_per_million'},
        'absolute': {'cumulative': 'total_cases', 'new': 'new_cases'}
    },
    'deaths': {
        'normalised': {'cumulative': 'total_deaths_per_million', 'new': 'new_deaths_per_million'},
        'absolute': {'cumulative': 'total_deaths', 'new': 'new_deaths'}
    }
}


def plot_cases(app: dash.Dash, df: pd.DataFrame) -> html.Div:

    all_countries = [{'value': country, 'label': f'{country}'} for country in df['location'].unique()]

    plot = html.Div(
            [
                html.Div(
                    dcc.Dropdown(id='country_dropdown', options=all_countries, value=['Germany'],
                                 multi=True),
                    style={'width': '48%', 'display': 'inline-block'}
                ),
                html.Div(

                    [
                        html.Div(
                            daq.BooleanSwitch(
                                id='CumulativeSwitch',
                                on=False,
                                label="Cumulate",
                                labelPosition="left"
                            ),
                            style={'width': '32%', 'display': 'inline-block'}
                        ),
                        html.Div(
                            daq.BooleanSwitch(
                                id='NormaliseSwitch',
                                on=False,
                                label="Normalise by population",
                                labelPosition="left"
                            ),
                            style={'width': '32%', 'display': 'inline-block'}
                        ),
                        html.Div(
                            daq.BooleanSwitch(
                                id='RollingSwitch',
                                on=False,
                                label="Rolling Average",
                                labelPosition="left"
                            ),
                            style={'width': '32%', 'display': 'inline-block'}
                        ),
                    ],
                    style={'width': '48%', 'display': 'inline-block'}
                ),
                *[
                    html.Div(
                        dcc.Graph(id=col),
                        style={'width': '48%', 'display': 'inline-block'}
                    )
                    for col in ['cases', 'deaths']
                ],

            ]
        )

    def plot_single_column(countries: list, field: str, normalise: bool, cumulative: bool, rolling: bool) -> dict:
        cumulative = cumulative * 'cumulative' + (not cumulative) * 'new'
        normalise = normalise * 'normalised' + (not normalise) * 'absolute'
        opacity = rolling * 0.2 + (not rolling) * 0.7
        column = FIELDS[field][normalise][cumulative]
        traces = [
            go.Scatter(
                x=df[df['location'] == country]['date'],
                y=df[df['location'] == country][column],
                mode='lines',
                opacity=opacity,
                name=country
            ) for country in countries
        ]
        if rolling:
            traces += [
                go.Scatter(
                    x=df[df['location'] == country]['date'],
                    y=df[df['location'] == country][column].rolling(7).mean(),
                    mode='lines',
                    opacity=0.7,
                    name=country,
                    line={'color': px.colors.qualitative.Plotly[i]},
                    showlegend=False
                ) for (i, country) in enumerate(countries)
            ]

        return {'data': traces,
                'layout': go.Layout(
                                    xaxis={'title': 'date'},
                                    yaxis={'title': field.capitalize()}
                                    )}

    @app.callback(
        Output('cases', 'figure'),
        [Input('country_dropdown', 'value'),
         Input('NormaliseSwitch', 'on'),
         Input('CumulativeSwitch', 'on'),
         Input('RollingSwitch', 'on')]
    )
    def update_cases(countries: list, normalise: bool, cumulative: bool, rolling: bool) -> dict:
        return plot_single_column(countries=countries, field='cases', normalise=normalise,
                                  cumulative=cumulative, rolling=rolling)

    @app.callback(
        Output('deaths', 'figure'),
        [Input('country_dropdown', 'value'),
         Input('NormaliseSwitch', 'on'),
         Input('CumulativeSwitch', 'on'),
         Input('RollingSwitch', 'on')]
    )
    def update_deaths(countries: list, normalise: bool, cumulative: bool, rolling: bool) -> dict:
        return plot_single_column(countries=countries, field='deaths', normalise=normalise, cumulative=cumulative,
                                  rolling=rolling)

    return plot


if __name__ == '__main__':
    ddf = get_data()

    aapp = dash.Dash()

    aapp.layout = plot_cases(aapp, ddf)

    aapp.run_server()

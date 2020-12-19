from pathlib import Path
import plotly.graph_objects as go
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output

from data import get_data


def plot_cases(app: dash.Dash, df: pd.DataFrame) -> html.Div:

    countries = [{'value': country, 'label': f'{country}'} for country in df['location'].unique()]

    plot = html.Div(
            [
                html.Div(
                    dcc.Dropdown(id='country_dropdown', options=countries, value='Germany'),
                    style={'width': '48%', 'display': 'inline-block'}
                ),
                html.Div(
                    # dcc.Dropdown(id='feature2', options=features, value='weight'),
                    style={'width': '48%', 'display': 'inline-block'}
                ),
                *[
                    html.Div(
                        dcc.Graph(id=col),
                        style={'width': '48%', 'display': 'inline-block'}
                    )
                    for col in ['plot_total_cases', 'plot_new_cases', 'plot_new_deaths', 'plot_hosp_patients']
                ],

            ]
        )

    def plot_single_column(country: str, column: str) -> dict:
        traces = [
            go.Scatter(
                x=df[df['location'] == country]['date'],
                y=df[df['location'] == country][column],
                mode='lines',
                opacity=0.7,
                marker={'size': 15, 'opacity': 0.5, 'line': {'color': 'white', 'width': 0.5}}
            )
        ]
        return {'data': traces,
                'layout': go.Layout(title='Cars',
                                    xaxis={'title': 'date'},
                                    yaxis={'title': column}
                                    )}

    @app.callback(
        Output('plot_total_cases', 'figure'),
        [Input('country_dropdown', 'value')]
    )
    def update_total_cases(country: str) -> dict:
        return plot_single_column(country=country, column='total_cases')

    @app.callback(
        Output('plot_new_cases', 'figure'),
        [Input('country_dropdown', 'value')]
    )
    def update_new_cases(country: str) -> dict:
        return plot_single_column(country=country, column='new_cases')

    @app.callback(
        Output('plot_new_deaths', 'figure'),
        [Input('country_dropdown', 'value')]
    )
    def update_total_cases(country: str) -> dict:
        return plot_single_column(country=country, column='new_deaths')

    @app.callback(
        Output('plot_hosp_patients', 'figure'),
        [Input('country_dropdown', 'value')]
    )
    def update_new_cases(country: str) -> dict:
        return plot_single_column(country=country, column='hosp_patients')

    return plot


if __name__ == '__main__':
    ddf = get_data()

    aapp = dash.Dash()

    aapp.layout = plot_cases(aapp, ddf)

    aapp.run_server()

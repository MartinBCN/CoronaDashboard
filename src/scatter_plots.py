from pathlib import Path
import plotly.graph_objects as go
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output

from data import get_data


def plot_scatter(app: dash.Dash, df: pd.DataFrame) -> html.Div:

    def plot_population_total_deaths() -> dict:
        traces = []
        for continent in df['continent'].unique():
            df_pop_death = df[df['continent'] == continent][['date', 'location', 'total_deaths', 'population']].copy()

            idx = df.groupby(['location'])['date'].transform(max) == df['date']

            df_pop_death = df_pop_death[idx]

            traces.append(
                go.Scatter(
                    x=df_pop_death['population'],
                    y=df_pop_death['total_deaths'],
                    mode='markers',
                    opacity=0.7,
                    marker={'size': 15, 'opacity': 0.5, 'line': {'color': 'white', 'width': 0.5}},
                    name=continent
                )
            )
        return {'data': traces,
                'layout': go.Layout(title='Continents',
                                    xaxis={'title': 'GDP'},
                                    yaxis={'title': 'Total Deaths'}
                                    )}

    plot = html.Div(
            [
                html.Div(
                        dcc.Graph(id='scatter_continent', figure=plot_population_total_deaths()),
                        style={'width': '48%', 'display': 'inline-block'}
                    )
            ]
        )

    return plot


if __name__ == '__main__':
    ddf = get_data()

    aapp = dash.Dash()

    aapp.layout = plot_scatter(aapp, ddf)

    aapp.run_server()

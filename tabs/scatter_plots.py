import plotly.graph_objects as go
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc

from tabs.data import get_data


def plot_scatter(app: dash.Dash, df: pd.DataFrame) -> html.Div:

    def generic_scatter(x: str, y: str, x_name: str, y_name: str) -> dict:
        traces = []
        for continent in df['continent'].unique():
            df_continent = df[df['continent'] == continent]

            idx = df.groupby(['location'])['date'].transform(max) == df['date']

            df_continent = df_continent[idx]

            traces.append(
                go.Scatter(
                    x=df_continent[x],
                    y=df_continent[y],
                    mode='markers',
                    opacity=0.7,
                    marker={'size': 15, 'opacity': 0.8},
                    name=continent,
                    text=df_continent["location"],
                    hoverinfo='text'
                )
            )
        return {'data': traces,
                'layout': go.Layout(
                                    margin=dict(t=40),
                                    hovermode="closest",
                                    paper_bgcolor="rgba(0,0,0,0)",
                                    plot_bgcolor="rgba(0,0,0,0)",
                                    legend={"font": {"color": "darkgray"}, "orientation": "h", "x": 0, "y": 1.1},
                                    font={"color": "darkgray"},
                                    showlegend=True,
                                    xaxis={'title': x_name, },
                                    yaxis={'title': y_name, }
                                    )}

    def plot_population_total_deaths() -> dict:
        return generic_scatter('population', 'total_deaths', 'Population', 'Total Deaths')

    def plot_cases_vs_deaths() -> dict:
        return generic_scatter('total_cases_per_million', 'total_deaths_per_million',
                               'Cases per Million', 'Deaths per Million')

    def plot_gdp_vs_deaths() -> dict:
        return generic_scatter('gdp_per_capita', 'total_deaths_per_million',
                               'GDP per Capita', 'Deaths per Million')

    plot = html.Div(
        className="twelve columns", children=
            [
                html.Div(children=[
                    html.Div(
                        dcc.Graph(id='scatter_continent', figure=plot_population_total_deaths(),
                                  config={'displayModeBar': False})
                    )],
                              style={'width': '45%', 'display': 'inline-block'},
                              className="pretty_container"),

                html.Div(children=[
                    html.Div(
                        dcc.Graph(id='scatter_cases_deaths', figure=plot_gdp_vs_deaths(),
                                  config={'displayModeBar': False})
                    )],
                              style={'width': '45%', 'display': 'inline-block'},
                              className="pretty_container"),

                html.Div(children=[
                    html.Div(
                        dcc.Graph(id='scatter_gdp_deaths', figure=plot_cases_vs_deaths(),
                                  config={'displayModeBar': False})
                    )],
                              style={'width': '45%', 'display': 'inline-block'},
                              className="pretty_container"),

                html.Div(children=[
                    html.Div(
                        dcc.Graph(id='scatter_hospital_beds_deaths',
                                  figure=generic_scatter('hospital_beds_per_thousand', 'total_deaths_per_million',
                                                         'Hospital Beds per Thousand', 'Deaths per Million'),
                                  config={'displayModeBar': False},
                                  )
                    )],
                              style={'width': '45%', 'display': 'inline-block'},
                              className="pretty_container")

            ]
        )

    return plot


if __name__ == '__main__':
    ddf = get_data()

    aapp = dash.Dash()

    aapp.layout = plot_scatter(aapp, ddf)

    aapp.run_server()

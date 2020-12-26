import plotly.graph_objects as go
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
from maindash import df
import plotly.express as px


def plot_map(df_continent: pd.DataFrame):

    # --------------------
    #  Chloropleth Map
    # --------------------
    fig = px.choropleth(df_continent, locations='iso_code', color='total_deaths',
                        color_continuous_scale="Bluered",
                        # range_color=(0, 12),
                        scope="europe",
                        labels={'unemp': 'unemployment rate'}
                        )
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    chloropleth_map = dcc.Graph(id='chloropleth_map', figure=fig, config={'displayModeBar': False})

    return chloropleth_map


def plot_bar_chart(df_continent: pd.DataFrame):

    # --------------------
    #  Bar Chart
    # --------------------

    df_continent = df_continent.sort_values(by='total_deaths')

    fig = go.Figure(go.Bar(
        x=df_continent['total_deaths'],
        y=df_continent['location'],
        orientation='h'))

    fig.update_layout(height=800)
    bar_chart = dcc.Graph(id='bar_chart', figure=fig, config={'displayModeBar': False})

    return bar_chart


def generate_map_tab() -> html.Div:
    continent = 'Europe'
    df_continent = df[df['continent'] == continent].copy()

    idx = df_continent.groupby(['location'])['date'].transform(max) == df_continent['date']

    df_continent = df_continent[idx]
    df_continent = df_continent[['iso_code', 'location', 'continent', 'total_deaths']]

    df_continent = df_continent.dropna()

    return html.Div(children=[
        html.Div(plot_map(df_continent),
                 style={'display': 'inline-block'},
                 className="pretty_container"),
        html.Div(plot_bar_chart(df_continent),
                 style={'display': 'inline-block'},
                 className="pretty_container")
    ])

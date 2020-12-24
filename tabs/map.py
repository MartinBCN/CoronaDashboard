import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output


def generate_map(app: dash.Dash, df: pd.DataFrame) -> html.Div:

    idx = df.groupby(['location'])['date'].transform(max) == df['date']

    df = df[idx]
    df = df[['iso_code', 'location', 'continent', 'total_deaths']]

    df = df.dropna()

    # --------------------
    #  Bubble Map
    # --------------------

    fig = px.scatter_geo(df,
                         locations="iso_code",
                         color="continent",
                         hover_name="location",
                         size="total_deaths",
                         # projection="natural earth"
                         )

    fig.update_geos(
        visible=True, resolution=50, scope="europe")

    bubble_map = dcc.Graph(id='bubble_map', figure=fig, config={'displayModeBar': False})

    # --------------------
    #  Chloropleth Map
    # --------------------
    fig = px.choropleth(df, locations='iso_code', color='total_deaths',
                        color_continuous_scale="Viridis",
                        # range_color=(0, 12),
                        scope="europe",
                        labels={'unemp': 'unemployment rate'}
                        )
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    chloropleth_map = dcc.Graph(id='chloropleth_map', figure=fig, config={'displayModeBar': False})

    return html.Div(children=[
        html.Div(bubble_map, style={'display': 'inline-block'},
                 className="pretty_container"),
        html.Div(chloropleth_map, style={'display': 'inline-block'},
                 className="pretty_container")
    ])

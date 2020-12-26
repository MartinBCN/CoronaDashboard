import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output


def generate_map(app: dash.Dash, df: pd.DataFrame) -> html.Div:

    continent = 'Europe'

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
                        color_continuous_scale="Bluered",
                        # range_color=(0, 12),
                        scope="europe",
                        labels={'unemp': 'unemployment rate'}
                        )
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    chloropleth_map = dcc.Graph(id='chloropleth_map', figure=fig, config={'displayModeBar': False})

    # --------------------
    #  Bar Chart
    # --------------------

    df_continent = df[df['continent'] == continent]
    df_continent = df_continent.sort_values(by='total_deaths')

    # {'data': traces,
    #  'layout': go.Layout(
    #      margin=dict(t=40),
    #      hovermode="closest",
    #      paper_bgcolor="rgba(0,0,0,0)",
    #      plot_bgcolor="rgba(0,0,0,0)",
    #      legend={"font": {"color": "darkgray"}, "orientation": "h", "x": 0, "y": 1.1},
    #      font={"color": "darkgray"},
    #      showlegend=True,
    #      xaxis={'title': x_name, },
    #      yaxis={'title': y_name, }
    #  )}

    fig = go.Figure(go.Bar(
        x=df_continent['total_deaths'],
        y=df_continent['location'],
        orientation='h'))

    fig.update_layout(height=800)
    bar_chart = dcc.Graph(id='bar_chart', figure=fig, config={'displayModeBar': False})

    # "height": 700,  # px

    return html.Div(children=[
        # html.Div(bubble_map, style={'display': 'inline-block'},
        #          className="pretty_container"),
        html.Div(chloropleth_map,
                 style={'display': 'inline-block'},
                 className="pretty_container"),
        html.Div(bar_chart,
                 style={'display': 'inline-block'},
                 className="pretty_container")
    ])

import plotly.express as px
import plotly.graph_objects as go
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
from maindash import df, app

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


def plot_single_column(countries: list, field: str,
                       normalise_clicks: int, cumulative_clicks: int, rolling_clicks: int) -> dict:
    """
    Create a graph for case and death numbers

    Parameters
    ----------
    countries
    field
    normalise_clicks
    cumulative_clicks
    rolling_clicks

    Returns
    -------

    """

    # Create a local copy to avoid irreversible changes to the data
    df_cases = df.copy()

    if (cumulative_clicks % 2) == 0:
        prefix = 'total'
    else:
        prefix = 'new'

    if (normalise_clicks % 2) == 0:
        suffix = '_per_million'
        hover_template = f'{prefix.capitalize()} {field.capitalize()}: '"%{y:.1f} | %{x}"
    else:
        suffix = ''
        hover_template = f'{prefix.capitalize()} {field.capitalize()}: '"%{y} | %{x}"

    column = f'{prefix}_{field}{suffix}'

    rolling = (rolling_clicks % 2) == 0

    opacity = rolling * 0.2 + (not rolling) * 0.7
    traces = [
        go.Scatter(
            x=df_cases[df_cases['location'] == country]['date'],
            y=df_cases[df_cases['location'] == country][column].clip(0),
            hovertemplate=hover_template,
            opacity=opacity,
            name=country,
            line={'color': px.colors.qualitative.Plotly[i]},
            showlegend=(not rolling)
        ) for (i, country) in enumerate(countries)
    ]
    if rolling:
        traces += [
            go.Scatter(
                x=df[df['location'] == country]['date'],
                y=df[df['location'] == country][column].clip(0).rolling(7).mean(),
                mode='lines',
                opacity=0.7,
                name=country,
                line={'color': px.colors.qualitative.Plotly[i]}
            ) for (i, country) in enumerate(countries)
        ]

    return {'data': traces,
            'layout': go.Layout(
                                xaxis={},
                                yaxis={'title': field.capitalize()},
                                margin=dict(t=40),
                                hovermode="closest",
                                paper_bgcolor="rgba(0,0,0,0)",
                                plot_bgcolor="rgba(0,0,0,0)",
                                legend={"font": {"color": "darkgray"}, "orientation": "h", "x": 0, "y": 1.1},
                                font={"color": "darkgray"},
                                showlegend=True
            )}


@app.callback(
    Output('cases', 'figure'),
    [Input('country_dropdown', 'value'),
     Input('toggle-normalise', 'n_clicks'),
     Input('toggle-cumulative', 'n_clicks'),
     Input('toggle-rolling', 'n_clicks')]
)
def update_cases(countries: list, normalise_clicks: int, cumulative_clicks: int, rolling_clicks: int) -> dict:
    return plot_single_column(countries=countries, field='cases', normalise_clicks=normalise_clicks,
                              cumulative_clicks=cumulative_clicks, rolling_clicks=rolling_clicks)


@app.callback(
    Output('deaths', 'figure'),
    [Input('country_dropdown', 'value'),
     Input('toggle-normalise', 'n_clicks'),
     Input('toggle-cumulative', 'n_clicks'),
     Input('toggle-rolling', 'n_clicks')]
)
def update_deaths(countries: list, normalise_clicks: int, cumulative_clicks: int, rolling_clicks: int) -> dict:
    return plot_single_column(countries=countries, field='deaths', normalise_clicks=normalise_clicks,
                              cumulative_clicks=cumulative_clicks, rolling_clicks=rolling_clicks)


def generate_cases() -> html.Div:

    all_countries = [{'value': country, 'label': f'{country}'} for country in df['location'].unique()]

    plot = html.Div(
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
                ),

                html.Div(
                    dcc.Graph(id='cases',
                              config={'displayModeBar': False}),
                              style={'width': '45%', 'display': 'inline-block'},
                              className="pretty_container"
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

    return plot



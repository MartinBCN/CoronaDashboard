GRID_LINES = {'gridwidth': 0.01, 'gridcolor': 'darkgray'}

import dash_html_components as html


def generate_section_banner(title):
    return html.Div(className="section-banner", children=title)

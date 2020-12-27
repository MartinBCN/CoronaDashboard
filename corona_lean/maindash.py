import dash
import flask
from util import get_data
import dash_bootstrap_components as dbc


df = get_data()

server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config.suppress_callback_exceptions = True

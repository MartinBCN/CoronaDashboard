from main_view import main_layout
from maindash import app


if __name__ == '__main__':
    app.layout = main_layout()

    # debug = False if os.environ.get("DASH_DEBUG_MODE", 'False') == "False" else True
    app.run_server(host="0.0.0.0", port=8050, debug=False)

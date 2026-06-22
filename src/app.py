from dash import Dash
from dash_bootstrap_components.themes import BOOTSTRAP

from components._01_import_cdr import import_data
from components._02_layout import create_layout

data = import_data()
app = Dash(__name__, external_stylesheets=[BOOTSTRAP])
app.title = "Carbon Dioxide Removal - Certificate Market"
app.layout = create_layout(app, data)

# Exposed for the production WSGI server (gunicorn --chdir src app:server)
server = app.server

if __name__ == "__main__":
    app.run(debug=True, port=8051)
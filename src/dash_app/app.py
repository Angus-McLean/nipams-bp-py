print('\nnipams - ','app.py')
import dash
import dash_bootstrap_components as dbc
from dash import html
import os



print('\nnipams - ','Starting Dash!')
# app = dash.Dash('app')

## styles
# https://bootswatch.com/ and https://cdnjs.com/libraries/bootswatch 
# bootstrap_css = 'https://cdnjs.cloudflare.com/ajax/libs/bootswatch/4.6.1/flatly/bootstrap.min.css'

# meta_tags are required for the app layout to be mobile responsive
app = dash.Dash(__name__, suppress_callback_exceptions=True,
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}],
                # assets_url_path=os.getcwd() + 'src/dash_app/assets/',
                external_stylesheets=[
                    dbc.themes.BOOTSTRAP, 
                    # dbc.icons.BOOTSTRAP,
                    # dbc.icons.FONT_AWESOME,
                    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css",
                    # "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.3.0/font/bootstrap-icons.css"
                ]
            )
server = app.server
app.layout = html.Div([html.P("Dash App Running!")])

# if __name__ == '__main__':
#     app.run_server(port=8500, debug=True, host='0.0.0.0')
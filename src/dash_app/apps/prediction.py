print('\nnipams - ','prediction.py')
from dash import dcc, html
from dash.dependencies import Input, Output, State

import pandas as pd
import plotly.express as px

from app import app
# from apps.dash_global import dash_global


layout = html.Div([
    html.H1('Prediction', style={"textAlign": "center"}),
    # html.Div(
    #     id='table-paging-with-graph-container',
    # ),
])

print('data_overview.py')
from dash import dcc, html
from dash.dependencies import Input, Output

from app import app

from .data_table import layout as data_table_layout
from data import load_data
# import data_table


layout = html.Div([
    html.H1('Data Overview', style={"textAlign": "center"}),
    html.Div([
        # dcc.Input(id='input-1', type='text', persistence_type='local'),
        # html.Button(id='submit-button-state', n_clicks=0, children='Submit'),
        # html.Div(id='output-state')
    ]),
    # data_table.layout
    data_table_layout
])


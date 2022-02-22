print('modeling.py')
from dash import dcc, html
from dash.dependencies import Input, Output, State

import pandas as pd
import plotly.express as px

from app import app
from apps.dash_global import dash_global


layout = html.Div([
    html.H1('Modeling', style={"textAlign": "center"}),
    html.Div(
        id='table-paging-with-graph-container',
    ),
])

@app.callback(
    Output('table-paging-with-graph-container', "children"),
    Input('data-filtered', "data"))
def update_graph(rows):
    dff = pd.read_json(rows, orient='split')
    # dff = pd.DataFrame(rows)
    # return f"update_graph : dff.shape : {dff.shape}"
    return dcc.Graph(
        figure=px.scatter_3d(dff, 'sepal_length','petal_length','sepal_width', color='species')
    )
print('data_overview.py')
from dash import dcc, html
import dash
from dash.dependencies import Input, Output, State

from app import app

from data import load_data
# import data_table


layout = html.Div([
    html.H1('Data Loading', style={"textAlign": "center"}),
    html.Div([
        # dcc.Input(id='input-1', type='text', persistence=True, persistence_type='local'),
        html.Button(id='submit-button-state', n_clicks=0, children='Load Raw Data'),
        # html.Div(id='output-state')
    ]),
])

@app.callback(Output('data-raw', 'data'),
              [Input('submit-button-state', 'n_clicks')],
              [State('data-raw', 'data')]
            #   [Input('input-1', 'value')]
              )
def set_data_raw(n, existing_state):
    print('set_data_raw!!', n)
    
    if n == 0 :         # https://community.plotly.com/t/how-to-update-component-when-button-is-clicked/9122
        print('Returning from cache..')
        return existing_state;
    print('triggers', list(map(lambda x:x['prop_id'], dash.callback_context.triggered)))
    return load_data().to_dict('records')




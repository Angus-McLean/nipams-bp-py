print('\nnipams - ','data_splitting.py')
from dash import html, dcc, Input, Output, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
from dash_app.cache import redis_store

from dash_app.components.basic_comps import JsonInputAIO

from app import app

options_splitting = {
    "split_by_random" : """{
        "indices" : ["file", "heartbeat"], 
        "split_kwargs" : {"n_splits":4, "test_size":0.2, "random_state":0}
    }""",
    "split_by_group" : """{
        "group_col" : 'patient',
        "indices" : ["file", "heartbeat"], 
        "split_kwargs" : {"n_splits":4}
    }""",
    "split_by_query" : """{
        "trainQ" : None,
        "testQ" : None, 
        "indices" : ["file", "heartbeat"], 
        "split_kwargs" : {"n_splits":4, "random_state":0}
    }"""
}

json_input_split = JsonInputAIO('json_input_split', options_splitting)

layout = dbc.Col([
    html.H1('Data Splitting', style={"textAlign": "center"}), 
    dbc.Row([
        dbc.Card([dbc.CardBody([
                html.H4("Set up Experiment", className="card-title"),
                html.Div([json_input_split]),
            ]),
        ], className='col-4'),
        dbc.Card([dbc.CardBody([
            html.H4("Experiment Overview", className="card-title"),
            html.Div(id='experiment-overview',children=['Experiment Output Pending..'])
        ])], className='col-8'),
    ]),
    dbc.Row([
        dbc.CardBody([
            html.H4("Finalize", className="card-title", style={"textAlign": "center"}),
            dbc.Button(id='confirm_splitting', children=['Confirm Experiment Design'])
        ], style={'textAlign':'center'}),
    ]),
])

@app.callback(
    Output('experiment-overview','children'),
    Input(json_input_split.ids.store_out('json_input_split'), 'data'),
    State('page_data_load_output','data')
)
def from_empty_to_text(split_key, df_key):
    print('\nnipams - ',"page from_empty_to_text",split_key, df_key)
    df = redis_store.load(df_key)
    return "Experiment Output : " + str(split_key) + "\nLoaded Data Shape : \n" + str(df.shape)

@app.callback(Output('data_splitting_page_out','data'),
              Input('confirm_splitting', 'n_clicks'), State(json_input_split.ids.store_out('json_input_split'), 'data'))
def from_confirm_to_pageout(n_clicks, split_json):
    if n_clicks is None: raise PreventUpdate
    print('\nnipams - ',"page from_confirm_to_pageout", split_json)
    # df = redis_store.load(split_json)
    return str(split_json)

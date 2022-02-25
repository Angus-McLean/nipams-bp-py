print('\nnipams - ','data_splitting.py')
from dash import html, dcc, Input, Output, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
from dash_app.cache import redis_store
from dash_app.components.basic_comps import JsonInputAIO

from app import app

from utils.constants import *
import json
import plotly.express as px
from models import experiments

options_splitting_json = {
    "split_by_random" : """{"function":"split_by_random","kwargs": {
        "indices" : ["file", "heartbeat"], 
        "split_kwargs" : {"n_splits":4, "test_size":0.2, "random_state":0}
    }}""",
    "split_by_group" : """{"function":"split_by_group","kwargs": {
        "group_col" : "patient",
        "indices" : ["file", "heartbeat"], 
        "split_kwargs" : {"n_splits":4}
    }}""",
    "split_by_query" : """{"function":"split_by_query","kwargs": {
        "trainQ" : "heartbeat <= 20",
        "testQ" : "heartbeat > 20", 
        "indices" : ["file", "heartbeat"], 
        "split_kwargs" : {"n_splits":4, "random_state":0}
    }}"""
}

json_input_split = JsonInputAIO('json_input_split', options_splitting_json)

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
def from_json_to_overview(split_json, df_key):
    print('\nnipams - ',"page from_json_to_overview",split_json, df_key)
    dfAll = redis_store.load(df_key)

    # dfImu = dfAll[INDICIES + INFO_COLS + IMU_COLS]
    dfBp = dfAll[INDICIES + INFO_COLS + BP_COLS]

    # sampleRandTestInds = experiments.split_by_random(dfImu, dfBp)
    # splitting_config = json.loads(options_splitting_json['split_by_group'])
    try:
        # splitting_config = json.loads(options_splitting_json['split_by_group'])
        splitting_config = json.loads(split_json)
    except Exception as e:
        return "ERROR - Invalid JSON String Provided. Details : \n\n" + str(e)
    
    sampleRandTestInds = getattr(experiments, splitting_config['function'])(dfBp=dfBp, **splitting_config['kwargs'])
    # try:
    #     sampleRandTestInds = experiments.get_splits_from_json_and_df(split_json, dfAll)
    # except Exception as e:
    #     return "ERROR - Invalid JSON String Provided. Details : \n\n" + str(e)
    
    # sampleExpDfs = experiments.get_experiment(sampleRandTestInds[0], dfImu, dfBp)

    dfSplits = pd.concat([
        dfBp.groupby(INDICIES).last().merge(sampleRandTestInds[0]['train'], on=INDICIES, how='right').assign(split_type='train'),
        dfBp.groupby(INDICIES).last().merge(sampleRandTestInds[0]['test'], on=INDICIES, how='right').assign(split_type='test')
    ], axis=0)

    dfSplits['set_name'] = dfSplits.file + '-' + dfSplits.split_type
    dfSplits = dfSplits.sort_values(['set_name','heartbeat'])    

    return dbc.CardBody([
        html.P(["Timeline of Train and Test heartbeats per patient"]),
        dcc.Graph(figure=px.scatter(
            dfSplits, 
            y='sbp', x='heartbeat',
            color='file', 
            symbol = dfSplits['split_type'],
            symbol_sequence= ['circle-open', 'circle']
        ))
    ]) 


    # return "Experiment Output : " + str(split_json) + "\nLoaded Data Shape : \n" + str(df.shape)

@app.callback(Output('data_splitting_page_out','data'),
              Input('confirm_splitting', 'n_clicks'), State(json_input_split.ids.store_out('json_input_split'), 'data'))
def from_confirm_to_pageout(n_clicks, split_json):
    if n_clicks is None: raise PreventUpdate
    print('\nnipams - ',"page from_confirm_to_pageout", split_json)
    # df = redis_store.load(split_json)
    return str(split_json)

print('\nnipams - ','data_modeling.py')
from dash import html, dcc, Input, Output, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
from dash_app.components.basic_comps import JsonInputAIO
from dash_app.cache import redis_store

from app import app

from utils.constants import *
import json
import plotly.express as px



import models, features
from data import preprocess
import sklearn
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer


options_modeling = {
    'pipe_random' : """Pipeline([
            ('reshape_vcg', preprocess.Explode_3D_Transformer()),
            ('rand', models.baselines.RandomRegressor())
        ])""",
    'pipe_mean' : """Pipeline([
            ('reshape_vcg', preprocess.Explode_3D_Transformer()),
            ('rand', models.baselines.DummyRegressor())
        ])""",
    'pipe_mvd' : """Pipeline([
            ('reshape_vcg', preprocess.Explode_3D_Transformer(
                data_cols=['az','ax']
            )),
            ('rand', models.analytical_mvd.AnalyticalBPEstimator())
        ])""",    
    'pipe_randomforest' : """Pipeline([
            ('vectorize_vcg', sklearn.preprocessing.FunctionTransformer(
                features.simple.vectorize_mean_std
            )),
            ('rand', models.baselines.RandomRegressor())
        ])""",

}

json_input_model = JsonInputAIO('json_input_model', options_modeling)

layout = dbc.Col([
    html.H1('Modeling', style={"textAlign": "center"}), 
    dbc.Row([
        dbc.Card([dbc.CardBody([
                html.H4("Define Model Architecture", className="card-title"),
                html.Div([json_input_model]),
            ]),
        ], className='col-4'),
        dbc.Card([dbc.CardBody([
            html.H4("Model Overview", className="card-title"),
            html.Div(id='model-overview',children=['Model Output Pending..'])
        ])], className='col-8'),
    ]),
    dbc.Row([
        dbc.CardBody([
            html.H4("Finalize", className="card-title", style={"textAlign": "center"}),
            dbc.Button(id='confirm_modeling', children=['Confirm Model Design'])
        ], style={'textAlign':'center'}),
    ]),
])

@app.callback(
    Output('model-overview','children'),
    Input(json_input_model.ids.store_out('json_input_model'), 'data'),
    State('page_data_load_output','data'),
    State('data_splitting_page_out','data')
)
def from_empty_to_text(pipe_json, df_key, split_json):
    print('\nnipams - ',"page from_empty_to_text", pipe_json)
    # df = redis_store.load(pipe_json)

    dfAll = redis_store.load(df_key)

    dfImu = dfAll[INDICIES + INFO_COLS + IMU_COLS]
    dfBp = dfAll[INDICIES + INFO_COLS + BP_COLS]

    ### FINALIZE SPLIT
    try: splitting_config = json.loads(split_json)
    except Exception as e: return "ERROR - Invalid JSON String Provided. Details : \n\n" + str(e)
    
    sampleRandTestInds = getattr(models.experiments, splitting_config['function'])(dfBp=dfBp, **splitting_config['kwargs'])
    sampleExpDfs = models.experiments.get_experiment(sampleRandTestInds[0], dfImu, dfBp)

    try: pipe_config = eval(pipe_json)
    except Exception as e: return "ERROR - Invalid Python String Provided. Details : \n\n" + str(e)
    
    ### TRAIN MODEL HERE ###
    # pipe = pipe_mean

    train_y = sampleExpDfs['train_y'].groupby(INDICIES)['dbp'].last()
    test_y = sampleExpDfs['test_y'].groupby(INDICIES)['dbp'].last()

    pipe_config.fit(sampleExpDfs['train_x'], train_y)
    preds = pipe_config.predict(sampleExpDfs['test_x'])

    # score_mae = experiments.score(preds, test_y)
    dfResults = pd.concat([test_y.reset_index(), pd.Series(preds, name='preds')], axis=1)
    dfResults_ = dfResults.melt(INDICIES)

    ### RETURN TEST SET PREDICTIONS ### (likely need to write multiple things to State)
    return dbc.CardBody([
        dbc.CardBody([
            html.H4("Scatter Preds vs Actuals", style={'position':'relative','marginBottom':'-1em','zIndex':'1'}),
            dcc.Graph(figure=px.scatter(x=test_y, y=preds)),
            html.Div([
                html.B("Scatter of Test Heartbeats"),
                html.P("Plot the predicted Blood Pressure values for test set heartbeats."),
            ], style={'position':'relative','marginTop':'-2em'}),
        ]),

        
        dbc.CardBody([
            html.H4("Accuracy Over Time", style={'position':'relative','marginBottom':'-1em','zIndex':'1'}),
            dcc.Graph(figure=px.scatter(
                dfResults_,
                y='value',
                x='heartbeat',
                color='file',
                symbol = dfResults_['variable'],
                symbol_sequence= ['circle-open', 'circle']
            )),
            html.Div([
                html.B("Timeline of Predictions vs Actuals"),
                html.P("Plot the predicted Blood Pressure values for test set heartbeats."),
            ], style={'position':'relative','marginTop':'-2em'})
        ]),
        
        
        # dcc.Graph(figure=px.scatter(
        #     dfSplits, 
        #     y='sbp', x='heartbeat',
        #     color='file', 
        #     symbol = dfSplits['split_type'],
        #     symbol_sequence= ['circle-open', 'circle']
        # ))
    ]) 

    return ["Model Output : " , str(pipe_json) , '\n Data Frame : ',df_key , '\n Split Data : ',split_json]

@app.callback(Output('data_modeling_page_out','data'),
    Input('confirm_modeling', 'n_clicks'), 
    State(json_input_model.ids.store_out('json_input_model'), 'data'),
    State('page_data_load_output','data'),
    State('data_splitting_page_out','data')
)
def from_confirm_to_pageout(n_clicks, pipe_json, df_key, split_json):
    if n_clicks is None: raise PreventUpdate
    print('\nnipams - ',"modeling page from_confirm_to_pageout", pipe_json, df_key, split_json)
    
    return pipe_json

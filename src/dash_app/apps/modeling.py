print('\nnipams - ','data_modeling.py')
from dash import html, dcc, Input, Output, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
from dash_app.components.basic_comps import JsonInputAIO

from app import app

options_modeling = {
    'Modeling Pipeline 1' : '{"modeling":"config"}',
    'Modeling Pipeline 2' : '{"modeling":"config2"}'
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
def from_empty_to_text(model_key, df_key, split_json):
    print('\nnipams - ',"page from_empty_to_text", model_key)
    # df = redis_store.load(model_key)
    return ["Model Output : " , str(model_key) , '\n Data Frame : ',df_key , '\n Split Data : ',split_json]

@app.callback(Output('data_modeling_page_out','data'),
    Input('confirm_modeling', 'n_clicks'), 
    State(json_input_model.ids.store_out('json_input_model'), 'data'),
    State('page_data_load_output','data'),
    State('data_splitting_page_out','data')
)
def from_confirm_to_pageout(n_clicks, model_json, df_key, split_json):
    if n_clicks is None: raise PreventUpdate
    print('\nnipams - ',"modeling page from_confirm_to_pageout", model_json, df_key, split_json)
    # df = redis_store.load(df_key)

    ### FINALIZE SPLIT
    
    ### TRAIN MODEL HERE ###


    ### RETURN TEST SET PREDICTIONS ### (likely need to write multiple things to State)
    return {
        'model_json' :  model_json,
    }

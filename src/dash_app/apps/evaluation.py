print('\nnipams - ','evaluation.py')
from dash import html, dcc, Input, Output, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
from dash_app.components.basic_comps import JsonInputAIO

from app import app

options_evaluation = {
    'Evaluation Config1' : '{"evaluation":"config"}',
    'Evaluation Config2' : '{"evaluation":"config2"}'
}

json_input_evaluation = JsonInputAIO('json_input_evaluation', options_evaluation)

layout = dbc.Col([
    html.H1('Evaluation', style={"textAlign": "center"}), 
    dbc.Row([
        dbc.Card([dbc.CardBody([
                html.H4("Define Evaluation Architecture", className="card-title"),
                html.Div([json_input_evaluation]),
            ]),
        ], className='col-4'),
        dbc.Card([dbc.CardBody([
            html.H4("Evaluation Overview", className="card-title"),
            html.Div(id='evaluation-overview',children=['Evaluation Output Pending..'])
        ])], className='col-8'),
    ]),
    dbc.Row([
        dbc.CardBody([
            html.H4("Finalize", className="card-title", style={"textAlign": "center"}),
            dbc.Button(id='confirm_evaluation', children=['Confirm Evaluation Design'])
        ], style={'textAlign':'center'}),
    ]),
    
])

@app.callback(
    Output('evaluation-overview','children'),
    Input(json_input_evaluation.ids.store_out('json_input_evaluation'), 'data'),
    State('data_modeling_page_out','data'),
)
def from_json_to_evaluation(df_key, modeling_key):
    print('\nnipams - ',"page from_json_to_evaluation", df_key, modeling_key)
    # df = redis_store.load(df_key)
    return ["Evaluation Output : " , str(df_key),
    "Modeling Output : " , str(modeling_key),]

@app.callback(Output('evaluation_page_out','data'),
    Input('confirm_evaluation', 'n_clicks'), 
    State(json_input_evaluation.ids.store_out('json_input_evaluation'), 'data'),
)
def from_confirm_to_pageout(n_clicks, eval_key):
    if n_clicks is None: raise PreventUpdate
    print('\nnipams - ',"evaluation page from_confirm_to_pageout", eval_key)
    # df = redis_store.load(eval_key)
    return "Evaluation Output : " + str(eval_key)

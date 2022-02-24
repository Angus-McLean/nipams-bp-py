print('evaluation.py')
from dash import html, dcc, Input, Output, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
from dash_app.components.basic_comps import JsonInputAIO

from app import app

options_evaluation = {
    'Split By Random' : '{}'
}

json_input_evaluation = JsonInputAIO('json_input_evaluation', options_evaluation)

layout = dbc.Col([
    html.H1('Modeling', style={"textAlign": "center"}), 
    dbc.Row([
        dbc.Card([dbc.CardBody([
                html.H4("Define Model Architecture", className="card-title"),
                html.Div([json_input_evaluation]),
            ]),
        ], className='col-4'),
        dbc.Card([dbc.CardBody([
            html.H4("Model Overview", className="card-title"),
            html.Div(id='evaluation-overview',children=['Model Output Pending..'])
        ])], className='col-8'),
    ]),
    dbc.Row([
        dbc.CardBody([
            html.H4("Finalize", className="card-title", style={"textAlign": "center"}),
            dbc.Button(id='confirm_evaluation', children=['Confirm Model Design'])
        ], style={'textAlign':'center'}),
    ]),
    dcc.Store(id='evaluation_page_out')
])

@app.callback(
    Output('evaluation-overview','children'),
    Input(json_input_evaluation.ids.store_out('json_input_evaluation'), 'data')
)
def from_empty_to_text(df_key):
    print("page from_empty_to_text", df_key)
    # df = redis_store.load(df_key)
    return "Model Output : " + str(df_key)

@app.callback(Output('evaluation_page_out','data'),
              Input('confirm_evaluation', 'n_clicks'), State(json_input_evaluation.ids.store_out('json_input_evaluation'), 'data'))
def from_confirm_to_pageout(n_clicks, df_key):
    if n_clicks is None: raise PreventUpdate
    print("page from_confirm_to_pageout", df_key)
    # df = redis_store.load(df_key)
    return "Page Output : " + str(df_key)

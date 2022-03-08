print('\nnipams - ','data_overview.py')
import dash
from dash import callback, html, dcc, Input, Output, State, MATCH
import dash_bootstrap_components as dbc

from utils.constants import *
from dash_app.cache import redis_store

from app import app
# import data_table

from dash_app.components.datatable_comp import DataTableAIO
from dash_app.components.load_data_nipams_comp import PythonDataLoaderAIO
from dash_app.components.overview_data_nipams_comp import NipamsDataOverviewAIO


input_data_comp = PythonDataLoaderAIO(aio_id='input_data_comp')
filter_data_comp = DataTableAIO(df=pd.DataFrame(), aio_id='filter_data_comp')
overview_data_comp = NipamsDataOverviewAIO(aio_id='overview_data_comp')


layout = dbc.Col([
    html.H1('Data Loading', style={"textAlign": "center"}),
    input_data_comp, 
    dbc.CardBody([
        html.H4("Filter DataFrame", className="card-title"),
        dbc.Spinner([
            html.Div(id='filter_table')
        ], color='primary', spinner_style={'width':'5rem','height':'5rem'}),
    ]),
    # filter_data_comp,
    overview_data_comp,
    dbc.CardBody([
        html.H4("Finalize Selection", className="card-title", style={"textAlign": "center"}),
        dbc.Button(id='confirm_data_load_page', children=['Confirm Selection'])
        # dbc.Spinner([
        #     html.Div(id='filter_table')
        # ], color='primary', spinner_style={'width':'5rem','height':'5rem'}),
    ], style={'textAlign':'center'}),
    
])

@app.callback(
    # Output(filter_data_comp.ids.store('filter_data_comp'),'data'),
    Output('filter_table','children'),
    Input(input_data_comp.ids.store('input_data_comp'), 'data')
)
def from_input_to_filter(df_key):
    print('\nnipams - ','from_input_to_filter', df_key)
    df = redis_store.load(df_key)
    return DataTableAIO(df=df, aio_id='filter_data_comp')
    # return {"df":df_key}

@app.callback(
    Output(overview_data_comp.ids.store('overview_data_comp'),'data'),
    Input(filter_data_comp.ids.store_out('filter_data_comp'), 'data')
)
def from_filter_to_overview(df):
    print('\nnipams - ','from_filter_to_overview', df)
    return df

@app.callback(
    Output('page_data_load_output','data'),
    Input('confirm_data_load_page', 'n_clicks'), State(filter_data_comp.ids.store_out('filter_data_comp'), 'data')
)
def from_confirm_to_output(n_clicks, df_key):
    print('\nnipams - ','data_load page from_overview_to_output', n_clicks, df_key)
    if n_clicks is None:raise PreventUpdate
    return df_key
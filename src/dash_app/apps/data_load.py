print('data_overview.py')
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
        dbc.Button(id='', children=['Confirm Selection'])
        # dbc.Spinner([
        #     html.Div(id='filter_table')
        # ], color='primary', spinner_style={'width':'5rem','height':'5rem'}),
    ]),
    dcc.Store(id='page_data_load_output')
])

@app.callback(
    # Output(filter_data_comp.ids.store('filter_data_comp'),'data'),
    Output('filter_table','children'),
    Input(input_data_comp.ids.store('input_data_comp'), 'data')
)
def from_input_to_filter(df_key):
    print('from_input_to_filter', df_key)
    df = redis_store.load(df_key)
    return DataTableAIO(df=df, aio_id='filter_data_comp')
    # return {"df":df_key}

@app.callback(
    Output(overview_data_comp.ids.store('overview_data_comp'),'data'),
    Input(filter_data_comp.ids.store_out('filter_data_comp'), 'data')
)
def from_filter_to_overview(df):
    print('from_filter_to_overview', df)
    return df

@app.callback(
    Output('page_data_load_output','data'),
    Input(filter_data_comp.ids.store_out('filter_data_comp'), 'data')
)
def from_overview_to_output(df):
    print('from_overview_to_output', df)
    return df
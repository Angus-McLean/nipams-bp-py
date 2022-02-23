import json
import uuid
from utils.constants import *
from dash import callback, html, dcc, Input, Output, State, MATCH
import dash_bootstrap_components as dbc
import plotly.express as px

from dash_app.cache import redis_store
from dash_app.components import datatable_comp
DataTableAIO = datatable_comp.DataTableAIO

def summarize_vcg_data(df):
    if df.empty: return {'message':'Empty DataFrame'}
    try:
        return {
            'Number of Patients' : df.patient.nunique(),
            'Total Rows' : df.shape[0],
            'Total Columns' : df.shape[1],
            'Total Heartbeats' : df.groupby('file').heartbeat.nunique().sum(),
        }
    except Exception as ex:
        return {
            'message': 'Error in summarize_vcg_data', 'error': str(ex)
        }

def agg_vcg_data(df):
    if df.empty: print('agg_vcg_data', 'Empty DataFrame');return pd.DataFrame()
    df = pd.concat([
        df.agg(['nunique']),
        df.describe(),
    ], axis=0)
    return df.round(3).reset_index()

def build_sunburst(df):
    path_cols = ['test_type','patient','test_num']
    df_res = df.groupby(path_cols).agg({
        'heartbeat':'nunique',
        'sbp':'mean',
        'dbp':'mean',
    }).reset_index()
    return dcc.Graph(figure=px.sunburst(df_res, path=path_cols, values='heartbeat', color='sbp'))

def build_scatter(df):
    df_scat = df.groupby(['test_type','file'])['ax','ay','az'].std().round(3).reset_index()
    return dcc.Graph(figure=px.scatter_3d(df_scat, x='ax',y='ay',z='az', hover_name='file', color='test_type'))


def build_graphs(data):
    return dbc.CardBody([
        dbc.Row([
            dbc.Col(["Sunburst", 
                build_sunburst(data)
            ]),
            dbc.Col(["Numerics",
                build_scatter(data)
            ])
        ])
    ])

class NipamsDataOverviewAIO(html.Div):
    class ids:
        store = lambda aio_id: {'aio_id': aio_id,'component': 'NipamsDataOverviewAIO','subcomponent': 'store'}
        store_out = lambda aio_id: {'aio_id': aio_id,'component': 'NipamsDataOverviewAIO','subcomponent': 'store_out'}
        summary = lambda aio_id: {'aio_id': aio_id,'component': 'NipamsDataOverviewAIO','subcomponent': 'summary'}
        table = lambda aio_id: {'aio_id': aio_id,'component': 'NipamsDataOverviewAIO','subcomponent': 'table'}
        graphs = lambda aio_id: {'aio_id': aio_id,'component': 'NipamsDataOverviewAIO','subcomponent': 'graphs'}
        
    ids = ids
    
    def __init__(self, aio_id=None):
        if aio_id is None: aio_id = str(uuid.uuid4())
    
        layout_tabs = dbc.Tabs(
            [
                dbc.Tab(dbc.CardBody(id=self.ids.summary(aio_id)), label="Summaries"),
                dbc.Tab(dbc.CardBody(id=self.ids.table(aio_id)), label="Numerical Overview"),
                dbc.Tab(dbc.CardBody(id=self.ids.graphs(aio_id)), label="Visual Overview"),
                # dbc.Tab(dbc.CardBody(id=self.ids.table(aio_id)), label="Patients & Heartbeats"),
            ]
        )

        super().__init__([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Overview VCG Data", className="card-title"),
                    html.P("View Resulting Summaries",className="card-text"),
                    dbc.Spinner([
                        layout_tabs
                    ], color='primary', spinner_style={'width':'5rem','height':'5rem'}),
                    # html.Div(id=self.ids.graphs(aio_id))
                ]),
                dcc.Store(id=self.ids.store(aio_id)),
                dcc.Store(id=self.ids.store_out(aio_id))
            ])
        ])

    @callback([
            Output(ids.summary(MATCH),'children'),
            Output(ids.table(MATCH),'children'),
            Output(ids.graphs(MATCH),'children'),
        ], 
        # Output(ids.summary(MATCH),'children'),
        Input(ids.store(MATCH), 'data'))
    def render_overview_tabs(data):
        df = redis_store.load(data)
        df_summary = "Data Summary : " + str(summarize_vcg_data(df))
        df_describe = agg_vcg_data(df)
        return (
            html.P(df_summary),
            DataTableAIO(df_describe),
            build_graphs(df)
        )

    
    # @callback(Output(ids.table(MATCH),'data'), 'children')
    # def render_table(data):
    #     df = redis_store.load(df)
    #     return DataTableAIO(df=df.sample(50).describe().reset_index())
    

## TODO Add Tabs to DataOverview
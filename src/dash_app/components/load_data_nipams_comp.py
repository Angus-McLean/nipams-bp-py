import uuid
from dash import callback, html, dcc, Input, Output, State, MATCH
import dash_bootstrap_components as dbc
from dash_app.cache import redis_store
from data import load_data;

TEST_TYPES = ['HLV','LLV','rec','res','bre']

class PythonDataLoaderAIO(html.Div):
    class ids:
        dropdown = lambda aio_id: {'aio_id': aio_id,'component': 'PythonDataLoaderAIO','subcomponent': 'dropdown'}
        button = lambda aio_id: {'aio_id': aio_id,'component': 'PythonDataLoaderAIO','subcomponent': 'button'}
        store = lambda aio_id: {'aio_id': aio_id,'component': 'PythonDataLoaderAIO','subcomponent': 'store'}
        msg = lambda aio_id: {'aio_id': aio_id,'component': 'PythonDataLoaderAIO','subcomponent': 'msg'}
    ids = ids
    
    def __init__(self, title="", aio_id=None):
        if aio_id is None: aio_id = str(uuid.uuid4())
        print('\nnipams - ','PythonDataLoaderAIO.__init__', aio_id)
    
        super().__init__([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Load VCG Data", className="card-title"),
                    html.P(
                        "Select which types of VCG readings to work with. (Read preprocessed VCG data from local file system.)",
                        className="card-text"),
                    dbc.InputGroup([
                        dcc.Dropdown(id=self.ids.dropdown(aio_id), multi=True,
                                     options=[{'value':i,'label':i} for i in TEST_TYPES], value=TEST_TYPES[:2],
                                    style={'minWidth':'400px'}, persistence=True),
                        dbc.Button(id=self.ids.button(aio_id), children=['Load Data'], n_clicks=0, color="primary")
                    ]),
                    dbc.Spinner(html.Div(id=self.ids.msg(aio_id)), color='primary'),
                    # dbc.Alert(id=self.ids.msg(aio_id), children="Success! Your data loaded Successfully",dismissable=True,fade=True,duration=2000,is_open=False,),
                ]),
                dcc.Store(id=self.ids.store(aio_id))
            ])
        ])
    
    @callback(Output(ids.msg(MATCH),'children'), Input(ids.store(MATCH),'data'))
    def print_success_msg(data):
        print('\nnipams - ','print_success_msg', data)
        # if n== 0 : return '', False
        df = redis_store.load(data)
        return 'Success! Loaded DataFrame ({} rows x {} columns)'.format(*df.shape)

    @callback(
        Output(ids.store(MATCH),'data'),
        State(ids.dropdown(MATCH),'value'), Input(ids.button(MATCH),'n_clicks'))
    def load_data(types, n):
        print('\nnipams - ','input-file-pattern, button-load', types, n)
        # if n== 0 : return '', False
        dfAll = load_data.load_dataframe_from_pickle('data/interim', '|'.join(types or []))
        dfAll.ts = dfAll.ts.astype(int)
        df_key = redis_store.save(dfAll)
        print('\nnipams - ','input-file-pattern, button-load', df_key, str(dfAll.shape))
        return df_key
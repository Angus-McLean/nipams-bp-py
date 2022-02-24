from dash import callback, html, dash_table, dcc, Input, Output, State, MATCH
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import uuid, warnings
import pandas as pd
from dash_app.cache import redis_store

class EmptyStoreAIO(html.Div):
    
    COMP_NAME = "EmptyStoreAIO"
    class ids:
        store_in = lambda aio_id: {'aio_id': aio_id,'component': "EmptyStoreAIO",'subcomponent': 'store_in'}
        store_out = lambda aio_id: {'aio_id': aio_id,'component': "EmptyStoreAIO",'subcomponent': 'store_out'}
        text_state = lambda aio_id: {'aio_id': aio_id,'component': "EmptyStoreAIO",'subcomponent': 'text_state'}
    
    
    def __init__(self, aio_id=None, data_in=None, store_in=None, verbose=False):
        if aio_id is None: aio_id = str(uuid.uuid4())
        if verbose : print("EmptyStoreAIO.__init__", self.COMP_NAME, aio_id, data_in, store_in, '\n')
    
        if data_in is not None: store_in = redis_store.save(data_in)
    
        super().__init__([
            dcc.Store(id=self.ids.store_in(aio_id), data=store_in),
            dcc.Store(id=self.ids.store_out(aio_id)),
            html.Pre(id=self.ids.text_state(aio_id),
                     children=["EmptyStoreAIO.rendered", self.COMP_NAME, aio_id], 
                     style={'display':'' if verbose else 'none'}),
        ])
        
    @callback([Output(ids.store_out(MATCH),'data'),Output(ids.text_state(MATCH),'children'),], 
        Input(ids.store_in(MATCH), 'data'))
    def from_in_to_out(df_key):
        print("EmptyStoreAIO.from_in_to_out", df_key, '\n')
        df_key_out = df_key
        # df = redis_store.load(df_key); 
        # df_key_out = redis_store.save(df)
        return df_key, str({'store_in' : df_key, 'store_out' : df_key_out})


class JsonInputAIO(html.Div):
    
    COMP_NAME = "JsonInputAIO"
    class ids:
        store_in = lambda aio_id: {'aio_id': aio_id,'component': "JsonInputAIO",'subcomponent': 'store_in'}
        store_out = lambda aio_id: {'aio_id': aio_id,'component': "JsonInputAIO",'subcomponent': 'store_out'}
        text_state = lambda aio_id: {'aio_id': aio_id,'component': "JsonInputAIO",'subcomponent': 'text_state'}
        input_dropdown = lambda aio_id: {'aio_id': aio_id,'component': "JsonInputAIO",'subcomponent': 'input_dropdown'}
        input_textarea = lambda aio_id: {'aio_id': aio_id,'component': "JsonInputAIO",'subcomponent': 'input_textarea'}
        confirm_button = lambda aio_id: {'aio_id': aio_id,'component': "JsonInputAIO",'subcomponent': 'confirm_button'}
        
    
    
    def __init__(self, aio_id=None, options={}, store_in=None, verbose=False):
        if aio_id is None: aio_id = str(uuid.uuid4())
        if verbose : print("JsonInputAIO.__init__", self.COMP_NAME, aio_id, store_in)
    
        options_inv = {v: k for k, v in options.items()}
    
        super().__init__([
            dbc.CardBody([
                html.H1(['']),
                dbc.Row([dcc.Dropdown(id=self.ids.input_dropdown(aio_id), options=options_inv)]),
                html.H1(['']),
                dbc.Row([
                    dcc.Textarea(id=self.ids.input_textarea(aio_id), placeholder="Select Sample Input..", style={'height':'140px'})
                ]),
                html.H1(['']),html.H1(['']),
                dbc.Row([dbc.Button(["Confirm Text Input"],id=self.ids.confirm_button(aio_id))]),
            ]),
            dcc.Store(id=self.ids.store_in(aio_id), data=store_in),
            dcc.Store(id=self.ids.store_out(aio_id)),
            html.Pre(id=self.ids.text_state(aio_id),
                     children=["JsonInputAIO.rendered",' ', self.COMP_NAME,' ', aio_id], 
                     style={'display':'' if verbose else 'none'}),
        ])

    @callback(Output(ids.input_textarea(MATCH),'value'), 
        Input(ids.input_dropdown(MATCH), 'value'))
    def from_dropdown_to_textarea(value):
        print("JsonInputAIO.from_dropdown_to_textarea", value)
        # df_key_out = df_key
        # df = redis_store.load(df_key); 
        # df_key_out = redis_store.save(df)
        return value or ''

        
    @callback(Output(ids.store_out(MATCH),'data'), 
        Input(ids.confirm_button(MATCH), 'n_clicks'),
        State(ids.input_textarea(MATCH), 'value'),)
    def from_confirm_to_out(n_clicks, text_input=''):
        print("JsonInputAIO.from_confirm_to_out", text_input, n_clicks)
        if n_clicks is None:raise PreventUpdate
        return text_input

    ### TODO : Add JSON parse and error handling, display to client

print('\nnipams - ','index.py')
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

# Connect to main app.py file
from app import app, server
# from app import server

import os, sys; sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))

# Connect to your app pages
from apps.dash_global import dash_global
from data import load_data
# from ... import data
# print('\nnipams - ','Setting data_raw')

from apps import data_load, data_splitting, modeling, evaluation, prediction

sidenav = dbc.Col([
    html.Img(src='https://upload.wikimedia.org/wikipedia/en/thumb/2/29/McGill_University_CoA.svg/1200px-McGill_University_CoA.svg.png', style={"alignSelf": "center",'height':'20%', 'width':'20%'}),
    
    html.H1('Nipams VCG Analysis', className='pt-4', style={"textAlign": "center"}),

    dbc.ButtonGroup(    # https://dash-bootstrap-components.opensource.faculty.ai/docs/components/button_group/
        [
            dbc.Button(children=[dbc.NavItem([dbc.NavLink([' 1. Loading'], href='/apps/data_load')])], outline=True),
            dbc.Button(children=[dbc.NavItem([dbc.NavLink([' 2. Splitting'], href='/apps/data_splitting')])], outline=True),
            dbc.Button(children=[dbc.NavItem([dbc.NavLink([' 3. Modeling'], href='/apps/modeling')])], outline=True),
            dbc.Button(children=[dbc.NavItem([dbc.NavLink([' 4. Evaluation'], href='/apps/evaluation')])], outline=True),
            dbc.Button(children=[dbc.NavItem([dbc.NavLink([' 5. Prediction'], href='/apps/prediction')])], outline=True),
            # dbc.Button(children=[dbc.NavItem([html.I(className="fa-2x fa-thin fa-heart me-2"),dbc.NavLink([ '1. Loading'], href='/apps/data_load')])], outline=True),
            # dbc.Button(children=[dbc.NavItem([html.I(className="fa-2x fa-thin fa-bar-chart-steps me-2"),dbc.NavLink([ '2. Splitting'], href='/apps/data_splitting')])], outline=True),
            # dbc.Button(children=[dbc.NavItem([html.I(className="fa-2x fa-thin fa-activity me-2"),dbc.NavLink([ '3. Modeling'], href='/apps/modeling')])], outline=True),
            # dbc.Button(children=[dbc.NavItem([html.I(className="fa-2x fa-thin fa-body-text me-2"),dbc.NavLink([ '4. Evaluation'], href='/apps/evaluation')])], outline=True),
            # dbc.Button(children=[dbc.NavItem([html.I(className="fa-2x fa-thin fa-heart-pulse me-2"),dbc.NavLink([ '5. Prediction'], href='/apps/prediction')])], outline=True),
        ],
        vertical=True,)
], className="d-flex flex-column flex-shrink-0 p-2 m-2", style={'textAlign':'center'})

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dbc.Row([
        dbc.Col([
            sidenav
        ], width={'size':2}, style={'background':'#8080801a'}),
        dbc.Col([dbc.CardBody([
            dbc.CardBody(id='page-content', children=[]),
        ])], width={'size':9}),
    ], style={'height':'100vh'}),
    dcc.Store(id='data-raw'),   # https://dash.plotly.com/sharing-data-between-callbacks
    dcc.Store(id='data-filtered'),

    dcc.Store(id='page_data_load_output', storage_type='local'),
    dcc.Store(id='data_splitting_page_out', storage_type='local'),
    dcc.Store(id='data_modeling_page_out', storage_type='local'),
    dcc.Store(id='evaluation_page_out', storage_type='local'),
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    print('\nnipams - ','dash loading! asdf!', pathname)
    if pathname == '/apps/data_load':
        return data_load.layout
    if pathname == '/apps/data_splitting':
        return data_splitting.layout
    if pathname == '/apps/modeling':
        return modeling.layout
    if pathname == '/apps/evaluation':
        return evaluation.layout
    if pathname == '/apps/prediction':
        return prediction.layout
    else:
        return "404 Page Error! Please choose a link"


if __name__ == '__main__':
    app.run_server(port=8500, debug=True, host='0.0.0.0')
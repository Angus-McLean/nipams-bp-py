print('dash_table.py')
import json
import pandas as pd
import plotly.express as px
import dash
from dash import html, dash_table, dcc
from dash.dependencies import Input, Output, State

from app import app
from apps.dash_global import dash_global
DATA_TABLE_COLUMNS = dash_global['data_raw'].columns if 'data_raw' in dash_global else ['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'species',
       'species_id']

layout = html.Div(
    style={'display': 'flex', 'flex-direction': 'row'},
    children=[
        html.Div(
            dash_table.DataTable(
                id='table-paging',
                columns=[
                    {"name": i, "id": i} for i in sorted(DATA_TABLE_COLUMNS)
                ],
                page_current=0, page_size=20, page_action='custom', 
                persistence_type='session', persistence=True, #persisted_props=["table-paging.sort_by", "table-paging.filter_query"],
                filter_action='custom',
                filter_query='', sort_by=[],
                sort_action='custom', sort_mode='multi'
            ),
            style={'height': 750, 'overflowY': 'scroll', 'padding':10},
        ),
    ]
)

operators = [['ge ', '>='],
             ['le ', '<='],
             ['lt ', '<'],
             ['gt ', '>'],
             ['ne ', '!='],
             ['eq ', '='],
             ['contains '],
             ['datestartswith ']]


def split_filter_part(filter_part):
    for operator_type in operators:
        for operator in operator_type:
            if operator in filter_part:
                name_part, value_part = filter_part.split(operator, 1)
                name = name_part[name_part.find('{') + 1: name_part.rfind('}')]

                value_part = value_part.strip()
                v0 = value_part[0]
                if (v0 == value_part[-1] and v0 in ("'", '"', '`')):
                    value = value_part[1: -1].replace('\\' + v0, v0)
                else:
                    try:
                        value = float(value_part)
                    except ValueError:
                        value = value_part

                # word operators need spaces after them in the filter string,
                # but we don't want these later
                return name, operator_type[0].strip(), value

    return [None] * 3



@app.callback(
    Output('data-filtered', "data"),
    # Output('table-paging', "columns"),
    Input('data-raw', "data"),
    Input('table-paging', "sort_by"),
    Input('table-paging', "filter_query"))
def update_table(rows, sort_by, filter):
    # filter = filter or ''
    # sort_by = sort_by or []
    print('update_table', sort_by, filter)
    print('context', json.dumps({'triggered': list(map(lambda x:x['prop_id'], dash.callback_context.triggered))}))

    filtering_expressions = filter.split(' && ')
    dff = pd.DataFrame(rows)
    for filter_part in filtering_expressions:
        col_name, operator, filter_value = split_filter_part(filter_part)

        if operator in ('eq', 'ne', 'lt', 'le', 'gt', 'ge'):
            # these operators match pandas series operator method names
            dff = dff.loc[getattr(dff[col_name], operator)(filter_value)]
        elif operator == 'contains':
            dff = dff.loc[dff[col_name].str.contains(filter_value)]
        elif operator == 'datestartswith':
            # this is a simplification of the front-end filtering logic,
            # only works with complete fields in standard format
            dff = dff.loc[dff[col_name].str.startswith(filter_value)]

    if len(sort_by):
        dff = dff.sort_values(
            [col['column_id'] for col in sort_by],
            ascending=[
                col['direction'] == 'asc'
                for col in sort_by
            ],
            inplace=False
        )
    # cols = list({"name": i, "id": i} for i in sorted(dff.columns))
    return dff.to_json(orient='split')

# @app.callback(
#     Output('data-filtered', "data"),
#     Output('table-paging', "columns"),
#     Input('data-raw', "data"))
# def create_table(rows, page_current, page_size):
#   # dff = pd.DataFrame(rows)
#   dff = pd.read_json(rows, orient='split')
#   dfJson = dff.iloc[
#       page_current*page_size: (page_current + 1)*page_size
#   ].to_dict('records')
#   cols = ({"name": i, "id": i} for i in sorted(df.columns))
#   return cols

@app.callback(
    Output('table-paging', "data"),
    Input('data-filtered', "data"),
    Input('table-paging', "page_current"),
    Input('table-paging', "page_size"))
def update_table_paging(rows, page_current, page_size):
  print('update_table_paging',len(rows), page_current, page_size)
  dff = pd.read_json(rows, orient='split')
  return dff.iloc[
      page_current*page_size: (page_current + 1)*page_size
  ].to_dict('records')



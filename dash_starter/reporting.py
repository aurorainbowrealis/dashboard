from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
import pandas as pd


def make_datatable(df: pd.DataFrame, idx: str, title: str, width: int = 12):
    return dbc.Col(dbc.Card([
        dbc.CardHeader(title),
        dbc.CardBody([
            dash_table.DataTable(
                id=f'datatable-{idx}',
                columns=[{'name': i, 'id': i} for i in df.columns],
                data=df.to_dict('records'),
                style_table={'overflowX': 'scroll'},
                style_cell={'textAlign': 'left', 'minWidth': '0px',
                            'maxWidth': '180px', 'whiteSpace': 'normal'},
                style_header={'fontWeight': 'bold',
                              'backgroundColor': 'rgb(230, 230, 230)'},
                page_size=20,
                sort_action='native',
                filter_action='native',
                sort_mode='multi',
                editable=False,
                page_action='native',
            )
        ])
    ]),  md=width)

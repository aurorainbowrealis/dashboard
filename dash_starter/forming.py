import dash_bootstrap_components as dbc
from dash import dcc, html


def make_dropdown(idx:str, label: str, unique_values: list, value:str ='', disabled:bool = False) -> dbc.Row:
    return dbc.Row([
        dbc.Col(
            html.Label(label),
            width=4,
            style={'text-align': 'right', 'padding-top': '10px'}
        ),
        dbc.Col(
            dcc.Dropdown(
                id=f'dropdown-{idx}',
                options=[{'label': value, 'value': value}
                         for value in unique_values],
                value=value,
                disabled=disabled
            ),
            width=8
        )
    ])


def make_text_input(idx:str, label: str, value: str = '') -> dbc.Row:
    return dbc.Row([
        dbc.Col(
            html.Label(label),
            width=4,
            style={'text-align': 'right', 'padding-top': '10px'}
        ),
        dbc.Col(
            dcc.Input(
                id=f'text-input-{idx}',
                value=value,
                type='text'
            ),
            width=8
        )
    ])


def make_numerical_input(idx:str, label: str, min: int = 0, max: int = 100, step: int = 1, value: int = 0) -> dbc.Row:
    return dbc.Row([
        dbc.Col(
            html.Label(label),
            width=4,
            style={'text-align': 'right', 'padding-top': '10px'}
        ),
        dbc.Col(
            dcc.Input(
                id=f'numerical-input-{idx}',
                value=value,
                type='number',
                min=min,
                max=max,
                step=step
            ),
            width=8
        )
    ])

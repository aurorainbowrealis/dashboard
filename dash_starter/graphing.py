from ast import List
import dash_bootstrap_components as dbc
from dash import dcc, html, dash_table, ctx


def make_bar_graph(x: List, y: List, idx: str, width: int = 4, orientation: str = 'h', title: str = '') -> dbc.Col:
    # bar_mode = 'group' if orientation == 'h' else 'stack'
    return dbc.Col([
        dcc.Graph(
            id=f'bar-graph-{idx}',
            figure={
                'data': [
                    {'x': x, 'y': y,
                     'type': 'bar', 'orientation': orientation, 'text': x.values, 'textposition': 'inside'},
                ],
                'layout': {
                    'autosize': True,
                    # 'title': title,
                    # 'xaxis': {'automargin': True},
                    'yaxis': {
                        'automargin': True
                    }
                }
            },
            # config={
            #     'fillFrame': True,
            # }
        ),
    ], md=width)


def make_example_sankey(idx: str, width: int = 6):
    return dbc.Col([
        dcc.Graph(
            id=f'example-sankey-{idx}',
            figure={
                'data': [dict(
                    type='sankey',
                    node=dict(
                        pad=15,
                        thickness=20,
                        line=dict(color="black", width=0.5),
                        label=["A1", "A2", "B1", "B2", "C1", "C2"],
                        color=[
                            "blue", "blue", "blue", "blue", "blue", "blue"
                        ]
                    ),
                    link=dict(
                        source=[0, 1, 0, 2, 3, 3],
                        target=[2, 3, 3, 4, 4, 5],
                        value=[8, 4, 2, 8, 4, 2]
                    )
                )],
                'layout': dict(
                    title="Sankey Diagram Example",
                    font=dict(size=10),
                )
            }
        ),
    ], md=width)

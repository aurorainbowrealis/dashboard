import dash
from dash import dcc, html, dash_table, ctx, callback, Input, Output

import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
from database import DataHolder
from tabs.overview import OverviewTab
from tabs.month_over_month import MonthOverMonthTab
from tabs.post_study import PostStudyTab

data_holder = DataHolder()
overview_tab = OverviewTab()
month_over_month_tab = MonthOverMonthTab()
post_study_tab = PostStudyTab()

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = 'Dashboard'
server = app.server
np.random.seed(42)





app.layout = dbc.Container([
    html.H1('BAU'),
    html.Div('''Study dashboard'''),
    dbc.Tabs([
        dbc.Tab(overview_tab.get_layout(data_holder), label="Overview"),
        dbc.Tab(month_over_month_tab.get_layout(
            data_holder), label="Month over Month"),
        dbc.Tab(post_study_tab.get_layout(data_holder), label="Posterior Study"),
    ])
], fluid=True)


@dash.callback(
    [Output('bar-graph-overview-rt', 'figure'),
        Output('bar-graph-overview-rtwc', 'figure'),
        Output('bar-graph-overview-cttr', 'figure'), ],
    [Input('numerical-input-overview-top-n', 'value'),
     Input('text-input-overview-page-contains', 'value'),
     Input('dropdown-overview-segment', 'value'),
     Input('dropdown-overview-available-months', 'value'), ],)
def update_overview_layout(top_n, page_contains, segment, selected_month):
    trigger_id = ctx.triggered_id
    return overview_tab.update_layout(data_holder=data_holder, top_n=top_n, page_contains=page_contains, segment=segment, selected_month=selected_month, trigger_id=trigger_id)


@dash.callback(
    [Output('bar-graph-mom-rt', 'figure'),
     Output('bar-graph-mom-rtwc', 'figure'),
     Output('bar-graph-mom-cttr', 'figure'),
     Output('dropdown-mom-month-1', 'options'),
     Output('dropdown-mom-month-2', 'options'),
     ],
    [Input('dropdown-mom-month-1', 'value'),
     Input('dropdown-mom-month-2', 'value'),
     Input('dropdown-mom-segment', 'value'),
     Input('numerical-input-mom-top-n', 'value'),
     Input('text-input-mom-page-contains', 'value'),
     ],)
def update_mom_layout(month_1, month_2, segment, top_n, page_contains):
    trigger_id = ctx.triggered_id
    return month_over_month_tab.update_layout(data_holder=data_holder, month_1=month_1, month_2=month_2, segment=segment, top_n=top_n, page_contains=page_contains, trigger_id=trigger_id)

@dash.callback(
    [Output('dropdown-post-study-reference-period-start', 'options'),
     Output('dropdown-post-study-reference-period-end', 'options'),
     Output('dropdown-post-study-comparison-period-start', 'options'),
     Output('dropdown-post-study-comparison-period-end', 'options'),
     Output('datatable-post-study-reference', 'data'),
     Output('datatable-post-study-studied-page', 'data'),
     ],
     [
        Input('dropdown-post-study-reference-period-start', 'value'),
        Input('dropdown-post-study-reference-period-end', 'value'),
        Input('dropdown-post-study-comparison-period-start', 'value'),
        Input('dropdown-post-study-comparison-period-end', 'value'),
        Input('text-input-post-study-page-contains', 'value'),
     ]
)
def update_post_study_layout(reference_period_start, reference_period_end, comparison_period_start, comparison_period_end, page_contains):
    trigger_id = ctx.triggered_id
    return post_study_tab.update_layout(data_holder=data_holder, reference_period_start=reference_period_start, reference_period_end=reference_period_end, comparison_period_start=comparison_period_start, comparison_period_end=comparison_period_end, page_contains=page_contains, trigger_id=trigger_id)



if __name__ == '__main__':
    app.run_server(debug=True)

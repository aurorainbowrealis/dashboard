import dash_bootstrap_components as dbc
from database import DataHolder
from graphing import make_bar_graph
from forming import make_dropdown, make_text_input, make_numerical_input
from tabs.view import View


class MonthOverMonthTab(View):
    def __init__(self) -> None:
        super().__init__()
        self.name = "mom"

        self.col_titles = {"RAW_TRAFFIC": "Web Traffic Diff", 
                           "RAW_TRAFFIC_WITH_CALL": "Raw Traffic with Call Diff", 
                           "CALL_TO_TRAFFIC_RATIO": "Call to Traffic Ratio Diff"}

    def get_layout(self, data_holder: DataHolder):
        rt_df = data_holder.get_mom_diff("RAW_TRAFFIC")
        rtwc_df = data_holder.get_mom_diff("RAW_TRAFFIC_WITH_CALL")
        cttr_df = data_holder.get_mom_diff("CALL_TO_TRAFFIC_RATIO")

        return dbc.Row([
            dbc.Col([
                self._get_sidebar(data_holder, 12),
            ], md=2),
            dbc.Col([
                dbc.Row([make_bar_graph(rt_df.RAW_TRAFFIC,
                        rt_df.PAGE_NAME, f'{self.name}-rt', '6', 'h', 'Web Traffic Diff'),
                        make_bar_graph(rtwc_df.RAW_TRAFFIC_WITH_CALL,
                        rtwc_df.PAGE_NAME, f'{self.name}-rtwc', '6', 'h', 'Raw Traffic with Call Diff'),

                         ]),
                dbc.Row([make_bar_graph(cttr_df.CALL_TO_TRAFFIC_RATIO,
                        cttr_df.PAGE_NAME, f'{self.name}-cttr', '6', 'h', 'Call to Traffic Ratio Diff'),
                         ]),
            ], md=10),
        ])

    def _get_sidebar(self, data_holder: DataHolder, width: int = 4):
        months = data_holder.available_months

        return dbc.Col([
            make_dropdown(f'{self.name}-month-1', 'Month 1', list(filter(lambda x: x  < data_holder.selected_months["MONTH_2"], months)), value = data_holder.selected_months["MONTH_1"]),
            make_dropdown(f'{self.name}-month-2', 'Month 2', list(filter(lambda x: x  > data_holder.selected_months["MONTH_1"], months)), value = data_holder.selected_months["MONTH_2"]),
            make_dropdown(f'{self.name}-segment', 'Segment', ['OLB', 'MOB']),
            make_numerical_input(f'{self.name}-top-n', 'Top N',
                                 min=1, max=100, step=1, value=15),
            make_text_input(f'{self.name}-page-contains', 'Page Contains'),
        ], md=width)

    def update_layout(self, data_holder: DataHolder, *args, **kwargs):
        trigger_id = kwargs.get('trigger_id')
        print(f'triggered by {trigger_id}', flush=True)

        month_1 = kwargs.get('month_1')
        month_2 = kwargs.get('month_2')
        top_n = kwargs.get('top_n')
        page_contains = kwargs.get('page_contains')
        segment = kwargs.get('segment')

        if trigger_id is None:
            pass
        elif f'dropdown-{self.name}-month-1' in trigger_id:
            data_holder.selected_months["MONTH_1"] = "" if month_1 is None else month_1
        elif f'dropdown-{self.name}-month-2' in trigger_id:
            data_holder.selected_months["MONTH_2"] = "" if month_2 is None else month_2
        elif f'numerical-input-{self.name}-top-n' in trigger_id:
            data_holder.filters['TOP_N'] = top_n
        elif f'text-input-{self.name}-page-contains' in trigger_id:
            data_holder.filters['PAGE_NAME'] = page_contains
        elif f'dropdown-{self.name}-segment' in trigger_id:
            print(f"segment: {segment}", flush=True)
            data_holder.filters['SEGMENT'] = segment

        df_list = [data_holder.get_mom_diff(i) for i in self.col_titles.keys()]
        return tuple(
            [{
                'data': [
                    {
                        'x': df_list[i][list(self.col_titles.keys())[i]],
                        'y': df_list[i].PAGE_NAME,
                        'type': 'bar',
                        'orientation': 'h',
                        'bar_mode': 'group',
                        'text': df_list[i][list(self.col_titles.keys())[i]], 
                        'textposition': 'inside'
                    },
                ],
                'layout': {
                    'title': list(self.col_titles.values())[i],
                    'yaxis': {'automargin': True},
                    'xaxis': {'automargin': True},
                    # the line below is the equivalent of `auto_text = True` in plotly express
                },
            }
            for i in range(len(df_list))] +
            [list(
                filter(lambda x: x < data_holder.selected_months["MONTH_2"], data_holder.available_months))] +
            [list(
                filter(lambda x: x > data_holder.selected_months["MONTH_1"], data_holder.available_months))]
        )

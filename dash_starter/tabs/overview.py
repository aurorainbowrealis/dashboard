import dash_bootstrap_components as dbc
from database import DataHolder
from graphing import make_bar_graph
from forming import make_dropdown, make_text_input, make_numerical_input
from tabs.view import View


class OverviewTab(View):
    def __init__(self) -> None:
        super().__init__()
        self.name = "overview"

        self.col_titles = {"RAW_TRAFFIC": "Web Traffic Total",
                           "RAW_TRAFFIC_WITH_CALL": "Raw Traffic with Call Total",
                           "CALL_TO_TRAFFIC_RATIO": "Call to Traffic Ratio Total"}

    def get_layout(self, data_holder: DataHolder):
        rt_df = data_holder.get_filtered_df('RAW_TRAFFIC')
        rtwc_df = data_holder.get_filtered_df('RAW_TRAFFIC_WITH_CALL')
        cttr_df = data_holder.get_filtered_df('CALL_TO_TRAFFIC_RATIO')

        return dbc.Row([
            dbc.Col([
                self._get_sidebar(data_holder, 12),
            ], md=2),
            dbc.Col([
                dbc.Row([make_bar_graph(rt_df.RAW_TRAFFIC, rt_df.PAGE_NAME, f'{self.name}-rt', '6', 'h', 'Web Traffic'),
                        make_bar_graph(rtwc_df.RAW_TRAFFIC_WITH_CALL, rtwc_df.PAGE_NAME,
                                       f'{self.name}-rtwc', '6', 'h', 'Web Traffic with Call'),
                         ]
                        ),
                dbc.Row([make_bar_graph(cttr_df.CALL_TO_TRAFFIC_RATIO, cttr_df.PAGE_NAME,
                                        f'{self.name}-cttr', '6', 'h', 'Call to Traffic Ratio'), ]),
            ], md=10),
        ])

    def _get_sidebar(self, data_holder: DataHolder, width: int = 4):
        return dbc.Col([
            make_dropdown(f'{self.name}-available-months',
                          'Available Months', data_holder.available_months, data_holder.available_months[-1]),
            # make_dropdown('Sampling Method', ['RAW', 'TF-IDF'], True),
            make_dropdown(f'{self.name}-segment',
                          'Segment', ['OLB', 'MOB'], None),
            # make_dropdown('Measurement', ['Absolute', 'Ratio'], True),
            make_numerical_input(f'{self.name}-top-n', 'Top N',
                                 min=1, max=100, step=1, value=15),
            make_text_input(f'{self.name}-page-contains', 'Page Contains'),
        ], md=width)

    def update_layout(self, data_holder: DataHolder, *args, **kwargs):
        trigger_id = kwargs.get('trigger_id')
        print(f'triggered by {trigger_id}', flush=True)

        top_n = kwargs.get('top_n')
        page_contains = kwargs.get('page_contains')
        segment = kwargs.get('segment')
        selected_month = kwargs.get('selected_month')

        if trigger_id is None:
            pass
        elif f'numerical-input-{self.name}-top-n' in trigger_id:
            data_holder.filters['TOP_N'] = top_n
        elif f'text-input-{self.name}-page-contains' in trigger_id and page_contains != '':
            data_holder.filters['PAGE_NAME'] = page_contains
        elif f'dropdown-{self.name}-segment' in trigger_id:
            data_holder.filters['SEGMENT'] = "" if segment is None else segment
        elif f'dropdown-{self.name}-available-months' in trigger_id:
            data_holder.selected_months["MONTH_1"] = "" if selected_month is None else selected_month
            print(selected_month, data_holder.selected_months, flush=True)

        rt_df = data_holder.get_filtered_df('RAW_TRAFFIC')
        rtwc_df = data_holder.get_filtered_df('RAW_TRAFFIC_WITH_CALL')
        cttr_df = data_holder.get_filtered_df('CALL_TO_TRAFFIC_RATIO')

        df_list = [data_holder.get_filtered_df(
            i) for i in self.col_titles.keys()]

        return tuple(
            {
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
                    'autosize': True,
                    'title': list(self.col_titles.values())[i],
                    'yaxis': {'automargin': True},
                    # 'xaxis': {'automargin': True},
                    # the line below is the equivalent of `auto_text = True` in plotly express
                },

            }
            for i in range(len(df_list))
        )

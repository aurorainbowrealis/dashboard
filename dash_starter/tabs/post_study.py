import dash_bootstrap_components as dbc
from database import DataHolder
from graphing import make_bar_graph
from forming import make_dropdown, make_text_input, make_numerical_input
from tabs.view import View
from reporting import make_datatable


class PostStudyTab(View):
    def __init__(self) -> None:
        super().__init__()
        self.name = "post-study"

    def get_layout(self, data_holder: DataHolder):
        # print(data_holder.get_totals(
        #     ["RAW_TRAFFIC", "RAW_TRAFFIC_WITH_CALL", "CALL_TO_TRAFFIC_RATIO"]), flush=True)
        return dbc.Row([
            dbc.Col([
                self._get_sidebar(data_holder, 12),
            ], md=2),
            dbc.Col([
                dbc.Row([
                    dbc.Col([
                        make_datatable(data_holder.get_reference_dataframe(),
                                       f'{self.name}-reference',
                                       "All Digital Pages")],
                            md=6),
                    dbc.Col([
                        make_datatable(data_holder.get_comparison_dataframe(),
                                       f'{self.name}-studied-page',
                                       "Studied Pages")],
                            md=6),
                ]),
            ], md=10),
        ])

    def _get_sidebar(self, data_holder: DataHolder, width: int = 4):
        months = data_holder.available_months
        return dbc.Col([
            make_dropdown(f'{self.name}-reference-period-start',
                          'Reference Period Start', months, data_holder.selected_months["REF_START"]),
            make_dropdown(f'{self.name}-reference-period-end',
                          'Reference Period End', months, data_holder.selected_months["REF_END"]),
            make_dropdown(f'{self.name}-comparison-period-start',
                          'Comparison Period Start', months, data_holder.selected_months["COMP_START"]),
            make_dropdown(f'{self.name}-comparison-period-end',
                          'Comparison Period End', months, data_holder.selected_months["COMP_END"]),
            # make_dropdown(f'{self.name}-segment', 'Segment', ['OLB', 'MOB']),
            # make_numerical_input(f'{self.name}-top-n', 'Top N',
            #                      min=1, max=100, step=1, value=15),
            make_text_input(f'{self.name}-page-contains', 'Page Contains'),
        ], md=width)

    def update_layout(self, data_holder: DataHolder, *args, **kwargs):
        trigger_id = kwargs.get('trigger_id')
        print(f'triggered by {trigger_id}', flush=True)

        ref_start = kwargs.get('reference_period_start')
        ref_end = kwargs.get('reference_period_end')
        comp_start = kwargs.get('comparison_period_start')
        comp_end = kwargs.get('comparison_period_end')
        page_contains = kwargs.get('page_contains')

        # join all the reference series together and sum them

        if trigger_id is None:
            pass
        elif f'{self.name}-reference-period-start' in trigger_id:
            data_holder.selected_months["REF_START"] = ref_start
        elif f'{self.name}-reference-period-end' in trigger_id:
            data_holder.selected_months["REF_END"] = ref_end
        elif f'{self.name}-comparison-period-start' in trigger_id:
            data_holder.selected_months["COMP_START"] = comp_start
        elif f'{self.name}-comparison-period-end' in trigger_id:
            data_holder.selected_months["COMP_END"] = comp_end
        elif f'text-input-{self.name}-page-contains' in trigger_id and page_contains != '':
            data_holder.filters['PAGE_NAME'] = page_contains

        ref_df = data_holder.get_reference_dataframe()
        comp_df = data_holder.get_comparison_dataframe()

        # if trigger_id is None:
        #     pass
        # elif f'numerical-input-{self.name}-month-1' in trigger_id:
        #     data_holder.selected_months["MONTH_1"] = "" if month_1 is None else month_1
        # elif f'numerical-input-{self.name}-month-2' in trigger_id:
        #     data_holder.selected_months["MONTH_2"] = "" if month_2 is None else month_2
        # elif f'numerical-input-{self.name}-segment' in trigger_id:
        #     data_holder.selected_segment = "" if segment is None else segment
        # elif f'numerical-input-{self.name}-top-n' in trigger_id:
        #     data_holder.selected_top_n = "" if top_n is None else top_n

        return (
            list(
                filter(
                    lambda x: x < data_holder.selected_months["REF_END"],
                    data_holder.available_months,
                )
            ),
            list(
                filter(
                    lambda x: data_holder.selected_months["REF_START"]
                    < x
                    < data_holder.selected_months["COMP_START"],
                    data_holder.available_months,
                )
            ),
            list(
                filter(
                    lambda x: data_holder.selected_months["REF_END"]
                    < x
                    < data_holder.selected_months["COMP_END"],
                    data_holder.available_months,
                )
            ),
            list(
                filter(
                    lambda x: data_holder.selected_months["COMP_START"] < x,
                    data_holder.available_months,
                )
            ),
            ref_df.to_dict('records'),
            comp_df.to_dict('records')
        )

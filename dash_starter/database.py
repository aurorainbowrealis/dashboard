from ast import List
import pandas as pd
import numpy as np
import os


class DataHolder:
    def __init__(self, datapath: str = './dash_starter/data'):
        self._filters = {
            'PAGE_NAME': '',
            'SEGMENT': '',
            'MEASUREMENT': '',
            'SAMPLE_METHOD': '',
            'TOP_N': 15,
        }

        self._datapath = datapath
        self._available_months = self._load_available_months()
        self._selected_months = {
            'MONTH_1': self._available_months[-2],
            'MONTH_2': self._available_months[-1],
            'REF_START': self._available_months[0],
            'REF_END': self._available_months[1],
            'COMP_START': self._available_months[-2],
            'COMP_END': self._available_months[-1],
        }

        self._data = {i: pd.read_csv(f"{self._datapath}/traffic{i}.csv")
                      for i in self._available_months}

    def _load_available_months(self):
        file_list = os.listdir(self._datapath)
        return [f.split('.')[0].split('traffic')[1] for f in file_list]

    @property
    def selected_months(self):
        return self._selected_months

    @selected_months.setter
    def selected_months(self,  month: str, value: str):
        self._selected_months[month] = value

    @property
    def available_months(self):
        return self._available_months

    @available_months.setter
    def available_months(self, value: str):
        pass

    @property
    def filters(self):
        return self._filters

    @filters.setter
    def filters(self, key: str, value: object = ''):
        self._filters[key] = value

    @property
    def months(self):
        return self._data

    def get_mom_diff(self, column_name: str):
        df_1 = self._data[self._selected_months['MONTH_1']]
        df_2 = self._data[self._selected_months['MONTH_2']]
        df_2 = self._apply_segment_filter(df_2)
        df_2 = self._apply_page_name_filter(df_2)
        df_1 = self._apply_segment_filter(df_1)
        df_1 = self._apply_page_name_filter(df_1)

        df_1.set_index('PAGE_NAME', inplace=True)
        df_2.set_index('PAGE_NAME', inplace=True)

        df_diff = df_2[[column_name]] - df_1[[column_name]]
        df_diff = df_diff.dropna()

        df_2.reset_index(inplace=True)
        top_n_pages = df_2.sort_values(by=column_name, ascending=False)[
            :self._filters['TOP_N']]['PAGE_NAME']

        return df_diff.loc[top_n_pages].sort_values(by=column_name, ascending=False).reset_index()

    def _apply_page_name_filter(self, sdf: pd.DataFrame):
        if self._filters['PAGE_NAME'] != '' and self._filters['PAGE_NAME'] is not None:
            sdf = sdf[sdf.PAGE_NAME.str.contains(self._filters['PAGE_NAME'])]
        return sdf

    def _apply_segment_filter(self, sdf: pd.DataFrame):
        if self._filters['SEGMENT'] in ["MOB", "OLB"]:
            return sdf[sdf.IS_MOBILE == self._filters['SEGMENT']]
        sdf = sdf.groupby('PAGE_NAME').sum().reset_index()
        return sdf

    def _apply_top_n_filter(self, sdf: pd.DataFrame, column_name: str) -> pd.DataFrame:
        return sdf[["PAGE_NAME", column_name]].sort_values(by=column_name, ascending=False)[:self._filters['TOP_N']]

    def get_descriptive_stats(self) -> pd.DataFrame:
        sdf = self._data[self._selected_months['MONTH_1']]
        sdf = self._apply_page_name_filter(sdf)
        sdf = self._apply_segment_filter(sdf)
        return sdf.describe().reset_index()
    
    def get_total(self, column_name: str) -> pd.DataFrame:
        sdf = self._data[self._selected_months['MONTH_1']]
        sdf = self._apply_page_name_filter(sdf)
        sdf = self._apply_segment_filter(sdf)
        return sdf[column_name].sum()
    
    def get_totals(self, month_id:str, column_list: List, apply_filters:bool=False) -> pd.DataFrame:
        sdf = self._data[month_id]
        if apply_filters:
            sdf = self._apply_page_name_filter(sdf)
            sdf = self._apply_segment_filter(sdf)
        sdf = pd.DataFrame(sdf[column_list].sum())
        # convert columns to int
        sdf = sdf.astype(int)

        sdf.columns = [month_id]
        sdf = sdf.T.reset_index()
        sdf["CALL_TO_TRAFFIC_RATIO"] = np.round(sdf["RAW_TRAFFIC_WITH_CALL"] / sdf["RAW_TRAFFIC"], 4)
        return sdf
    
    def get_period_dataframe(self, start_month:str, end_month:str, apply_filters:bool = False) -> pd.DataFrame :
        reference = [
            self.get_totals(
                i,
                ["RAW_TRAFFIC", "RAW_TRAFFIC_WITH_CALL", "CALL_TO_TRAFFIC_RATIO"],
                apply_filters=apply_filters
            )
            for i in self.available_months
            if start_month <= i <= end_month
        ]
        sdf = pd.concat(reference)
        x = {"index": "TOTAL", "RAW_TRAFFIC": sdf["RAW_TRAFFIC"].sum(
        ), "RAW_TRAFFIC_WITH_CALL": sdf["RAW_TRAFFIC_WITH_CALL"].sum()}
        sdf = sdf.append(x, ignore_index=True)
        x = {"index": "AVERAGE", "RAW_TRAFFIC": int(sdf["RAW_TRAFFIC"].mean()),
                "RAW_TRAFFIC_WITH_CALL": int(sdf["RAW_TRAFFIC_WITH_CALL"].mean())}
        sdf = sdf.append(x, ignore_index=True)
        sdf["CALL_TO_TRAFFIC_RATIO"] = np.round(
            sdf["RAW_TRAFFIC_WITH_CALL"] / sdf["RAW_TRAFFIC"], 4)
        return sdf
    
    def get_reference_dataframe(self) -> pd.DataFrame:
        return self.get_period_dataframe(self.selected_months["REF_START"], self.selected_months["REF_END"], False)
    
    def get_comparison_dataframe(self) -> pd.DataFrame:
        return self.get_period_dataframe(self.selected_months["COMP_START"], self.selected_months["COMP_END"], True)

    
    def get_filtered_df(self, column_name: str, month: int = 1):
        sdf = self._data[self._selected_months[f'MONTH_{month}']]

        sdf = self._apply_page_name_filter(sdf)
        sdf = self._apply_segment_filter(sdf)
        sdf = self._apply_top_n_filter(sdf, column_name)
        return sdf

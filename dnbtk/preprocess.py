#!/usr/bin/env python3

import pandas as pd


def read_raw_excel(excel, sheet_number=0):
    return pd.read_excel(excel, sheet_name=sheet_number)\
             .dropna(how='all')\
             .rename(columns={"样品名称": "sample_name",
                              "子文库号": "sample_id",
                              "测序类型": "seq_type",
                              "芯片号": "clip",
                              "Lane": "lane",
                              "Barcode号": "barcode",
                              "二级路径": "path"})\
            .loc[:, ["sample_name", "sample_id", "seq_type",
                     "clip", "lane", "barcode", "path"]]

#!/usr/bin/env python3

import os
import pandas as pd


def read_raw_excel(excel, sheet_number=0):
    return (
        pd.read_excel(excel, sheet_name=sheet_number)
        .dropna(how="all")
        .rename(
            columns={
                "样品名称": "sample_name",
                "子文库号": "sample_id",
                "测序类型": "seq_type",
                "芯片号": "clip",
                "Lane": "lane",
                "Barcode号": "barcode",
                "二级路径": "path",
            }
        )
        .loc[
            :,
            ["sample_name", "sample_id", "seq_type", "clip", "lane", "barcode", "path"],
        ]
    )


def generate_pe_fqpath(raw_df, check_exists=True):
    """
    raw_df header need contain: id, clip, lane, barcode, path
    """
    samples_dict = {"id": [], "fq1": [], "fq2": []}

    for i in range(len(raw_df)):
        for barcode in str(raw_df.at[i, "barcode"]).split("~"):
            samples_dict["id"].append(raw_df.at[i, "id"])

            fq1 = os.path.join(
                str(raw_df.at[i, "path"]),
                "_".join(
                    [
                        str(raw_df.at[i, "clip"]),
                        str(raw_df.at[i, "lane"]),
                        barcode,
                        "1.fq.gz",
                    ]
                ),
            )
            fq2 = fq1.replace("1.fq.gz", "2.fq.gz")

            samples_dict["fq1"].append(fq1)
            samples_dict["fq2"].append(fq2)

            if check_exists:
                if not os.path.exists(fq1):
                    print("%s not exists" % fq1)
                if not os.path.exists(fq2):
                    print("%s not exists" % fq2)

    samples_df = pd.DataFrame(samples_dict).sort_values("id")
    return samples_df

import pandas as pd
import json
import re

# DXI Label and Metadata

fn = "DXI_Labels_v2021.1.xlsx"
df_dxi1 = pd.read_excel(fn, sheet_name="DXI_1_Labels", engine="openpyxl")
df_dxi2 = pd.read_excel(fn, sheet_name="DXI_2_Labels", engine="openpyxl")
df_dxi3 = pd.read_excel(fn, sheet_name="Continuous_Var_Labels", 
                        engine="openpyxl")
df_hier = pd.read_excel(fn, sheet_name="Hier_Labels", engine="openpyxl")


dxi = {}
for _, row in df_dxi1.iterrows():
    dxi[row["DXI_1"]] = {"label": row["DXI_LABEL_1"], 
                        "ch_abbrev": row["CH_ABBREV"],
                        "system": "DXI",
                        "level": 1}
for _, row in df_dxi2.iterrows():
    dxi[row["DXI_2"]] = {"label": row["DXI_LABEL_2"],
                        "ch_abbrev": row["CH_ABBREV"],
                        "system": "DXI",
                        "level": 2}
for _, row in df_dxi3.iterrows():
    dxi[row["CONTINUOUS_VAR"]] = {"label": row["CONTINUOUS_VAR_LABEL"],
                            "cont_value": row["CONTINUOUS_VAR_VALUE"],
                            "cont_format": row["CONTINUOUS_VAR_FORMAT"],
                            "ch_abbrev": row["CH_ABBREV"],
                            "system": "DXI",
                            "level": 3}
for _, row in df_hier.iterrows():
    dxi[row["HIER"]] = {"label": row["HIER_LABEL"],
                        "ch_abbrev": row["CH_ABBREV"],
                        "level": 0}

fn = "DXCCSR-Reference-File-v2023-1.xlsx"
df_ccsr = pd.read_excel(fn, sheet_name="CCSR_Categories", skiprows=1,
                        engine="openpyxl")
for _, row in df_ccsr.iterrows():
    dxi["CCSR_"+row["CCSR Category"]] = {
                            "label": row["CCSR Category Description"],
                            "ch_abbrev": "CCSR",
                            "system": "CCSR",
                            "level": 1}

fn = "Z_DXI_Model1_P_AnnTotalSpend_250K.sas"
with open(fn, "r") as fp:
    for line in fp.readlines():
        pattern = "(\w+)\s+\*\s+([\-\d.]+)\s+\+"
        res = re.findall(pattern, line)
        if len(res) > 0 and res[0][0] in dxi:
            dxi[res[0][0]]["has_default_coeff"] = True
            dxi[res[0][0]]["score"] = float(res[0][1])

with open("dxi_metadata.json", "w") as fp:
    json.dump(dxi, fp=fp, indent=2)




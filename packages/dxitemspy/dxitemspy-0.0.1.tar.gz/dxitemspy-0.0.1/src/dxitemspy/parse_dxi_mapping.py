import pandas as pd
import json
import re

# DXI Label and Metadata

dxi_map = {}

fn = "ICD_10_CM_to_DXI_Mapping_v2021.1.xlsx"
df_dxi = pd.read_excel(fn, sheet_name="ICD_10_CM_to_DXI_Mapping", 
                        engine="openpyxl")
for _, row in df_dxi.iterrows():
    dx = row["ICD10CM"]
    if dx not in dxi_map:
        dxi_map[dx] = {"labels": []}

    label_keys = ["CH_ABBREV", 
                "DXI_1", "DXI_2", "DXI_3", "DXI_4", 
                "DXI_5", "DXI_6", "DXI_7", 
                "Continuous_Var", 
                "HIER_1", "HIER_2", "HIER_3", 
                "HIER_4", "HIER_5", "HIER_6"]
    dxi_map[dx]["labels"] = [row[label_key].strip() 
                                for label_key in label_keys
                                if (not pd.isna(row[label_key]) and 
                                    row[label_key].strip() != "")]
    dxi_map[dx]["dxi_valid_dx"] = row["ICD10CM_VALID"]
    if not pd.isna(row["Continuous_Var_Value"]):
        dxi_map[dx]["cont_value"] = row["Continuous_Var_Value"]


fn = "DXCCSR-Reference-File-v2023-1.xlsx"
df_ccsr = pd.read_excel(fn, sheet_name="DX_to_CCSR_Mapping", skiprows=1,
                        engine="openpyxl")
for _, row in df_ccsr.iterrows():
    dx = row["ICD-10-CM Code"]
    if dx not in dxi_map:
        dxi_map[dx] = {"labels": []}
    dxi_map[dx]["labels"].append("CCSR_" + row["CCSR Category"])
    dxi_map[dx]["ccsr_ip_ynx"] = row["Inpatient Default CCSR (Y/N/X)"]
    dxi_map[dx]["ccsr_op_ynx"] = row["Outpatient Default CCSR (Y/N/X)"]

with open("dxi_mapping.json", "w") as fp:
    json.dump(dxi_map, fp=fp, indent=2)




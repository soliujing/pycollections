# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# -*- coding: utf-8 -*-
# %%
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu
import warnings
warnings.simplefilter(action='ignore', category=DeprecationWarning)
warnings.simplefilter(action='ignore', category=FutureWarning)
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings
disable_warnings(InsecureRequestWarning)

# Read recipe inputs
UMS_input = dataiku.Dataset("UMS_input")
iRecon_historical = dataiku.Dataset("iRecon_historical")
# iRecon_historical_df = iRecon_historical.get_dataframe()

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# import pkg_resources
# installed_packages = pkg_resources.working_set
# installed_packages_list = sorted(["%s==%s" % (i.key, i.version)
#    for i in installed_packages])
# print(installed_packages_list)

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# %%
# UMS_input.read_schema()

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# %%
UMS_input_df = UMS_input.get_dataframe(infer_with_pandas=False).fillna("")
# UMS_input_df = UMS_input.get_dataframe()
# UMS_input_df

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# %%
# UMS_input_df.小票号
# UMS_input_df.loc[UMS_input_df.小票号 != ""]
# using dictionary to convert specific columns
# convert_dict = {'参考号': str,
#                 '商户号': str
#                 }
# UMS_input_df = UMS_input_df.loc[UMS_input_df.小票号 != ""].astype(convert_dict)
UMS_input_df = UMS_input_df.loc[UMS_input_df.小票号 != ""]
UMS_input_df.head(10)

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# %%
iRecon_historical_df = iRecon_historical.get_dataframe(infer_with_pandas=False).fillna("")
iRecon_historical_df.head(10)

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# %%
# iRecon_historical_df = iRecon_historical_df.fillna("")
# iRecon_historical_df.head(10)
final_df = pd.merge(UMS_input_df, iRecon_historical_df[['Slip Number','Document Date','Card Type','Card #', 'Acquirer Ref Number']], how="left", left_on=['小票号'], right_on=['Slip Number']);

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# %%
# Compute recipe outputs
# TODO: Write here your actual code that computes the outputs
# NB: DSS supports several kinds of APIs for reading and writing data. Please see doc.

upload_ums_df = final_df # Compute a Pandas dataframe to write into upload_ums

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# %%
# Write recipe outputs
upload_ums = dataiku.Dataset("upload_ums")
upload_ums.write_with_schema(upload_ums_df)
# %%
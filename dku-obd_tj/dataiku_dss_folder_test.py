# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# -*- coding: utf-8 -*-
# %%
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu
import io,re
import warnings
warnings.simplefilter(action='ignore')

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# %%
handle = dataiku.Folder("box_files")


# %%
# LIST all files
paths = handle.list_paths_in_partition()
paths


# %%
# download file as stream, then parse by pandas
with handle.get_download_stream("/bcd/UT3-VBRP.xlsx") as f:
    print(f.info())
    dfd=pd.read_excel(f.read())
    dfd.head(10)


# %%
# delete file and then write back via pandas binary output
handle.delete_path("/def/abc.csv")
# handle.upload_stream("/abc.csv", b"test again")
handle.upload_stream("/def/abc.csv", dfd.to_csv(index=False))


# %%
# do sth of each file matching pattern
for fn in paths:
    if re.match( "/def/.*\.csv", fn):
        print(fn)
        handle.delete_path(fn)
# handle.delete_path("/def/*.csv")

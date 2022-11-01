# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# -*- coding: utf-8 -*-
# %%
from importlib.resources import read_binary
import dataiku, tabula, re, io
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu
import warnings
warnings.simplefilter(action='ignore')

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# %%
handle = dataiku.Folder("box_input")

# %%
f = handle.get_download_stream("/PDF/tabula.py")

# %%
##### StringIO
fw = ""
for line in f.readlines():
    new_line = re.sub('\spip\s',' pip3 ',line.decode('utf-8'))
    fw = fw + new_line + "\n"
df = pd.read_csv(io.StringIO(fw))

# %%
##### BytesIO
fw = io.BytesIO()
# print(fw.getbuffer().nbytes)
for line in f.readlines():
    new_line = re.sub('\spip\s',' pip3 ',line.decode('utf-8'))
    fw.write((new_line + '\n').encode(encoding='utf-8'))
fw.seek(0)
df = pd.read_csv(fw)

# aa = f.read()
# fw.write(aa)

# %%
handle.delete_path("/PDF/tabula_RE.py")
handle.upload_stream("/PDF/tabula_RE.py", df.to_csv())
# %%


# with handle.get_download_stream("/PDF/tabula.py") as f:
#     fw = ""
#     for line in f.readlines():
#         new_line = re.sub('\spip\s',' pip3 ',line)
#         fw = fw + new_line + "\n"
#     handle.upload_stream("/PDF/tabula_RE2.py", fw)
# %%

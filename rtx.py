# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pandas as pd
fn = "~/Downloads/out.rtx"
ns = {"doc": "http://schema.redwood.com/report/rtx.xsd"}
# print(pd.options)


# %%

## xpath to read column names
df_cols = pd.read_xml(fn, namespaces = ns, xpath="//doc:columns/doc:column")

#create additional blank index column at beginning
cols = list(df_cols["name"])
cols.insert(0, "Index")


# %%

### use dtype to define data type for columns
# rtx_dtype="string"
rtx_dtype={"CCAr":"string"}

## xpath to read column names
rtx_df = pd.read_xml(fn, namespaces = ns, dtype=rtx_dtype, names=cols, xpath="//doc:data/doc:r")


# %%

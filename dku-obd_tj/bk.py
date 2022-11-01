# myapp.py

from bokeh.layouts import *
from bokeh.models import *
from bokeh.plotting import curdoc

import dataiku, datetime
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu
import warnings
warnings.simplefilter(action='ignore')

## load .env file when running locally
from dotenv import load_dotenv
load_dotenv()


def load_data(nrows):
    ### read from DSS data set, convert to DF
    dst = dataiku.Dataset("py_test_comments")
    df = dst.get_dataframe(infer_with_pandas=False, limit=nrows)
    return df

def get_userid(): 
    ### extract user ID by dku client
    client = dataiku.api_client()
    auth_info = client.get_auth_info()
    return auth_info["authIdentifier"]

# create a callback that adds a number in a random location
def update_call():
    global update_click
    if update_click == False:
        update_click = True
        btn_y = Button(label="YES")
        btn_y.on_click(btn_y_call)
        btn_n = Button(label="NO!")
        btn_n.on_click(btn_n_call)
        doc.add_root(row([btn_y, btn_n]))
    
def btn_y_call():
    global update_click
    update_click = False
    user = get_userid()

    df_n = pd.DataFrame()
    for j in source_dt.column_names:
        # print(source_dt.data[j][source_dt.selected.indices])
        df_n[j]=source_dt.data[j][source_dt.selected.indices]
    df_n['USER'] = user
    df_n['CHANGED_ON'] = datetime.datetime.now()
    print(df_n.head(5))
    
    doc_init()

def btn_n_call():
    global update_click
    update_click = False
    print("btn_no clicked")
    doc_init()
    # print("hahaha clicked")
    
def doc_init():
    doc.clear()
    global doc, source_dt
    source_dt = ColumnDataSource(data)
    columns = [
        TableColumn(field=col, title=col) for col in data.columns
        ]

    data_table = DataTable(source=source_dt, columns=columns,
                        selectable="checkbox",
                        editable=True)

    # add a button widget and configure with the call back
    button = Button(label="Press Me to update DB")
    button.on_click(update_call)

    # put the button and plot in a layout and add to the document
    doc.add_root(widgetbox(button, data_table))
    
doc = curdoc()
data = load_data(100)
source_dt = ColumnDataSource(data)
update_click = False
doc_init()
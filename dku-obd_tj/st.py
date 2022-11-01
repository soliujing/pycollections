# ${dip.home}/local/static/streamlit-starter-app.py

import streamlit as st
import pandas as pd
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
import dataiku,datetime,time

import warnings
warnings.simplefilter(action='ignore')

## load .env file when running locally
from dotenv import load_dotenv
load_dotenv()

# set fonts and basics
st.set_page_config(page_title="FDT | Home | JING_TEST_APP", page_icon="🦈", layout="wide")
st.write("""
<style>
@import url("https://fonts.googleapis.com/css2?family=Inter");
html, body, [class*="css"]  {
   font-family: 'Inter', normal;
}i
</style>
""", unsafe_allow_html=True)

## START BOILERPLATE APP
st.title(' JING_TEST_APP')


@st.cache(allow_output_mutation=True)
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

def update_dku(sel_row_df):
    ### write if not empty
    if not sel_row_df.empty:
        ## user & timestamp
        now = datetime.datetime.now()
        sel_row_df['USER'] = get_userid()
        sel_row_df['CHANGED_ON'] = now
        ## ignore node info as 1st column
        df_new = sel_row_df.iloc[:,1:]
        
        st.session_state.dku_update = True
        st.write(df_new)
        st.warning("be sure to update DB per above?")
        col1, col2 = st.columns([2,2])
        btn_y = col1.button("yes")
        btn_n = col2.button("no")
        if btn_y:
            st.session_state.dku_update = False
            msg = st.warning("yes clicked")
            time.sleep(1)
            dst = dataiku.Dataset("py_test_comments")
            #### allows for appending
            dst.spec_item["appendMode"] = True
            dst.write_dataframe(df_new)
            for i in range(3,0,-1):
                msg.success("write done - back in %d seconds" % (i))
                time.sleep(1)
            st.experimental_rerun()
        if btn_n:
            st.session_state.dku_update = False
            msg = st.warning("")
            for i in range(2,0,-1):
                msg.warning("action abort - back in %d seconds" % (i))
                time.sleep(1)
            st.experimental_rerun()

df_load_state = st.text('Loading data...')
df = load_data(20)
df_load_state.text("Done! (using st.cache)")

### build a grid
gd = GridOptionsBuilder.from_dataframe(df)
gd.configure_column("ORIGIN", headerCheckboxSelection = True)
gd.configure_pagination(enabled=True, paginationPageSize=20,paginationAutoPageSize=False)
gd.configure_default_column(editable=True, groupable=True)
gd.configure_selection(selection_mode="multiple", use_checkbox=True)
gridoptions = gd.build()
grid_table = AgGrid(
    df,
    gridOptions=gridoptions
)
sel_row = grid_table["selected_rows"]
sel_row_df = pd.DataFrame(sel_row)

if "dku_update" not in st.session_state:
    st.session_state.dku_update = False
if not sel_row_df.empty:
    st.write(sel_row_df)
    cbtn = st.button("Update Comments in DB")
    if cbtn or st.session_state.dku_update :
        update_dku(sel_row_df)
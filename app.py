# streamlit_app.py

import streamlit as st
from google.cloud import bigquery
import seaborn as sns
import pandas as pd
import pandas_gbq


from utils import credentials, SERVICE_KEY
client = bigquery.Client(credentials=credentials)

# Perform query.
# Uses st.experimental_memo to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def run_query(cols, name):
    st.write("Load DataFrame")
    sql = f"SELECT {cols} FROM streamlit-dashboard-369600.seoul.{name}"
    df = client.query(sql).to_dataframe()

    st.dataframe(df)

def main():
    tableNames = st.selectbox("테이블 선택", ("realestate", "iris"))
    if tableNames == "iris":
        run_query(cols="*", name="iris")
    else:
        sql = """
        SELECT STRING_AGG(column_name)
        FROM `streamlit-dashboard-369600.seoul.INFORMATION_SCHEMA.COLUMNS`
        where table_name = 'realestate'
        group by table_name
        """

        df = client.query(sql).to_dataframe()
        all_cols = df.values[0][0].split(",")
        columns = st.multiselect("컬럼명 선택", all_cols, default=all_cols)
        temp_Strings = ", ".join(columns)
        run_query(temp_Strings, tableNames)

if __name__ == "__main__":
    main()



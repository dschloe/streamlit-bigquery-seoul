# -*- coding:utf-8 -*-
import requests
import pandas as pd

# Google Cloud
from google.cloud import bigquery
import pandas_gbq

# API Key Settings
from utils import credentials, SERVICE_KEY
client = bigquery.Client(credentials=credentials)


def aptCrawling(SERVICE_KEY):
    data = None
    for j in range(1,2):
        url = f'http://openapi.seoul.go.kr:8088/{SERVICE_KEY}/json/tbLnOpendataRtmsV/{1+((j-1)*1000)}/{j*1000}'
        print(url)
        req = requests.get(url)
        content = req.json()
        con = content['tbLnOpendataRtmsV']['row']
        result = pd.DataFrame(con)
        data = pd.concat([data, result])
    data = data.reset_index(drop=True)
    data['DEAL_YMD'] = pd.to_datetime(data['DEAL_YMD'], format=("%Y%m%d"))

    return data

def save2BQ(data):
    table_name = "seoul.realestate"
    project_id = "streamlit-dashboard-369600"

    # Save the DataFrame to BigQuery
    pandas_gbq.to_gbq(data,
                      table_name,
                      project_id=project_id, if_exists='replace')

if __name__ == "__main__":
    data = aptCrawling(SERVICE_KEY)
    save2BQ(data)
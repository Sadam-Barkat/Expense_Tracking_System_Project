import streamlit as st
import requests
from datetime import datetime
import pandas as pd

API_URL = "http://localhost:8000"

def anlytics_months_tab():

    response = requests.get(f'{API_URL}/analytics_month')
    data = response.json()
    df = pd.DataFrame(data)
    st.bar_chart(df.set_index('Month')['Total'], use_container_width=True)

    df['Total'] = df['Total'].map("{:.2f}".format)
    st.table(df)




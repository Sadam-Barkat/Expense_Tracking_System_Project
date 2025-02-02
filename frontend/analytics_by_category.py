import streamlit as st
from datetime import datetime
import requests
import pandas as pd

API_URL = "http://localhost:8000"

def analytics_category_tab():
    col1, col2 = st.columns(2)

    with col1:
        start_date = st.date_input("Start_date", datetime(2024, 8, 1))
    with col2:
         end_date = st.date_input("End_date", datetime(2024, 8, 5))

    if st.button("Get Analytics"):
        payload = {
            "start_date":start_date.strftime("%Y-%m-%d"),
            "end_date":end_date.strftime("%Y-%m-%d")
        }   
        response = requests.post(f'{API_URL}/analytics_category', json=payload)
        response = response.json()
        
        data = {
            "category": list(response.keys()),
            "total":[response[category]['total'] for category in response],
            "percentage":[response[category]['percentage'] for category in response]
        }
        df = pd.DataFrame(data)
        df_sorted = df.sort_values(by='percentage', ascending=False)

        st.bar_chart(df_sorted.set_index('category')['percentage'], use_container_width=True)
        
        df_sorted['total'] = df_sorted['total'].map("{:.2f}".format)
        df_sorted['percentage'] = df_sorted['percentage'].map("{:.2f}".format)
        st.table(df_sorted)
 



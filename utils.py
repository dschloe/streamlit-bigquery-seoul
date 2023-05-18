import streamlit as st
from google.oauth2 import service_account

SERVICE_KEY = st.secrets.public_data_api.seoul_api_key

# Create API client.
credentials = service_account.Credentials.from_service_account_info(
    # Very Important Point
    st.secrets["gcp_service_account"]
)
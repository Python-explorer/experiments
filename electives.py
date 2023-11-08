import streamlit as st
import pandas as pd

# Function to load CSV data from a URL
@st.cache_resource
def load_data(url):

  data_url = 'https://github.com/Python-explorer/experiments/blob/main/ElectiveDataICB.csv'

# Load the data
data = load_data(data_url)
data.columns = [col.strip() for col in data.columns]

st.write(data.columns)


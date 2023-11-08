import streamlit as st
import pandas as pd

# The URL of the raw CSV file on GitHub
csv_url = "https://github.com/Python-explorer/experiments/blob/main/ElectiveDataICB.csv"

@st.cache
def load_data(url):
    try:
        # Attempt to load the CSV with default settings
        data = pd.read_csv(url)
    except pd.errors.ParserError:
        # If the ParserError is encountered, try reading the CSV with the following options:
        data = pd.read_csv(url, delimiter=',', on_bad_lines='skip')
    return data

# Load the data
df = load_data(csv_url)

# Display the DataFrame in Streamlit
st.write(df)

# List the column headers
st.write(list(df.columns))

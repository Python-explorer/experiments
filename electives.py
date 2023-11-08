import streamlit as st
import pandas as pd

# The URL of the raw CSV file on GitHub
csv_url = "https://github.com/Python-explorer/experiments/blob/main/ElectiveDataICB.csv"

@st.cache
def load_data(url):
    try:
        # Attempt to load the CSV with the default settings.
        data = pd.read_csv(url)
    except pd.errors.ParserError:
        # Attempt to load the CSV with a specified delimiter and error_bad_lines set to False.
        # Adjust the delimiter to match the CSV file's actual delimiter, e.g., ',', ';', '\t', etc.
        data = pd.read_csv(url, delimiter=',', error_bad_lines=False)
    return data

# Load the data
df = load_data(csv_url)

# Display the DataFrame in Streamlit
st.write(df)

# List the column headers
st.write(list(df.columns))

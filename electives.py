import streamlit as st
import pandas as pd

# The URL of the raw CSV file on GitHub
csv_url = "https://raw.githubusercontent.com/your-username/your-repo/main/your-file.csv"

@st.cache
def load_data(url):
    # Load the CSV data into a pandas DataFrame
    data = pd.read_csv(url)
    return data

# Load the data
df = load_data(csv_url)

# Display the DataFrame in Streamlit
st.write(df)

# List the column headers
st.write(list(df.columns))


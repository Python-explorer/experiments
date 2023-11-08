import streamlit as st
import pandas as pd

# Function to load CSV data from a URL
@st.cache_resource
def load_data(url):
    try:
        # The 'on_bad_lines' parameter is used to handle problematic lines.
        # Set it to 'warn' to issue a warning and skip them.
        data = pd.read_csv(url, on_bad_lines='warn')  # Make sure this line is correct
    except Exception as e:
        st.error(f"Failed to load data: {e}")
        return pd.DataFrame()  # Ensure this return statement is within the except block
    return data  # This should be outside the try-except block

# URL to the CSV file
data_url = 'https://github.com/Python-explorer/experiments/blob/main/ElectiveDataICB.csv'

# Load the data
data = load_data(data_url)
data.columns = [col.strip() for col in data.columns]

st.write(data.columns)

# Main app
def main():
    if not data.empty:
        st.write("Unique values in 'Treatment Function' column:")
        # Display the unique values in the column
        unique_values = data['Treatment Function'].unique()
        st.write(unique_values)
    else:
        st.write("No data received.")

if __name__ == "__main__":
    main()

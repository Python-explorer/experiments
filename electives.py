import streamlit as st
import pandas as pd

# Function to load CSV data from a URL
@st.cache_resource
def load_data(url):
    try:
        # Attempt to read a CSV file. The 'error_bad_lines' parameter will skip any problematic lines.
        # The 'warn_bad_lines' parameter will print a warning message for any lines that are skipped.
        # You might need to adjust the 'sep' parameter if a delimiter other than a comma is used.
        data = pd.read_csv(url, error_bad_lines=False, warn_bad_lines=True)
        return data
    except Exception as e:
        st.error(f"Failed to load data: {e}")
        return pd.DataFrame()

# URL to the CSV file
data_url = 'https://github.com/Python-explorer/experiments/blob/main/ElectiveDataICB.csv'

# Load the data
data = load_data(data_url)

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
